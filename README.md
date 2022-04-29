#Fetch Rewards Exercise: Backend SWE
####Noah Backman

##Installing and Running the Code
1. Clone this repository to your machine.
2. Ensure Docker is installed on your machine.
3. Navigate to cloned repository and in the command line:
    `docker build --tag webapp .`
4. Run from the command line:
    `docker run --publish 8000:5000 webapp`
---
The app should now be running at *http://127.0.0.1:8000*, and is ready to serve requests.

## API Documentation
This microservice can be accessed through three endpoints.

- `GET /balance`: returns a summary of total points
  - request: None
  - response: `{str: int}`
- `POST /transactions`: submit transaction data to database
  - request:`{"payer": str, "points": int, "timestamp": datetime }`
  - response: None
- `PUT /spend`: cash out rewards points
  - request: `{"points": int}`
  - response: `[{"payer": str, "points": int}]`
