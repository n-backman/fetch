from flask import Flask

app = Flask(__name__)
db = []

# add routes in app
from routes import *


if __name__ == "__main__":
    app.run(debug=False)
