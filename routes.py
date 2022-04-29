import datetime as dt

from webapp import app, db
from flask import request, make_response, jsonify


@app.route('/', methods=['GET'])
def index():
    return jsonify(db)


@app.route('/transactions', methods=['POST'])
def transactions():
    data = request.get_json()
    # verify all fields are present, if not, send a bad request error
    if len(data) != 3 or not data["payer"] or not data["points"] or not data["timestamp"]:
        return make_response("Invalid request body", 400)
    data['available'] = data['points']
    data['timestamp'] = dt.datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S%z")
    db.append(data)
    return make_response("Created", 201)


@app.route('/spend', methods=['PUT'])
def spend():
    # verify fields are present
    data = request.get_json()
    if len(data) != 1 or not data["points"]:
        return make_response("Invalid request body", 400)

    req_amt = int(data["points"])
    # query DB for total points and ensure total >= req_amt
    _, total = summarize(db)
    if total < req_amt:
        return make_response("Insufficient Points", 200)

    return_transactions = []
    curr_time = dt.datetime.now(tz=None)  # ideally these are all 'simultaneous'
    # working with the sorted db, check available points to remove.
    db.sort(key=lambda item: item['timestamp'])
    for x in db:
        available_points = x['available']
        transaction = {}
        # if there are more unused points from this transaction than we need
        if available_points > req_amt and req_amt:
            diff = available_points - req_amt
            x['available'] = diff
            transaction["points"] = -req_amt
            req_amt -= req_amt
        elif available_points and req_amt:
            # the total >= available, so take them all and reduce total
            req_amt -= available_points
            x['available'] = 0
            transaction["points"] = -available_points
        else:
            continue
        # append the transaction to the return list and add metadata
        transaction["payer"] = x['payer']
        transaction["timestamp"] = curr_time
        transaction["available"] = 0
        return_transactions.append(transaction)

        if req_amt == 0:
            # commit negative transactions and return
            db.extend(return_transactions)
            return jsonify([{"payer": t['payer'], "points": t['points']} for t in return_transactions])


@app.route('/balance', methods=['GET'])
def balance():
    # query db for transactions grouped by payer with a points sum
    return jsonify(summarize(db)[0])


def summarize(database: list) -> (dict, int):
    """
    Helper function to mimic a db query 'SELECT payer, sum(points) GROUP BY payer', along with a total sum

    :param database In-memory data store object
    :return summary Dict of form {payer: points}
    :return total A summary statistic of total available points
    """
    summary = {}
    total = 0
    for x in database:
        if x['payer'] not in summary:
            summary[x['payer']] = x['points']
        else:
            summary[x['payer']] += x['points']
        total += int(x['points'])
    return summary, total
