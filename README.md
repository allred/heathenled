# heathenled

API for aggregating activity data

The following instructions are for running the tests/app on Mac OS.  This is Python 3 Flask app.

To install on Mac OS:

* git clone https://github.com/allred/heathenled.git

* cd heathenled

* brew install pyenv pyenv-virtualenv

* pyenv install -v 3.6.2

* pyenv virtualenv 3.6.2 heathenled

* pyenv activate heathenled

* pip install -r requirements.txt

* ./run.py

That should start the Flask app, which should be available at http://127.0.0.1:5000/v1/activity

The endpoint receives a GET request with the following parameters:

* patient_id

* start_date

* end_date

Sample JSON response for http://localhost:5000/v1/activity?patient_id=6:

```
HTTP/1.0 200 OK
Content-Length: 83
Content-Type: application/json
Date: Thu, 21 Dec 2017 04:41:18 GMT
Server: Werkzeug/0.13 Python/3.6.2

{
    "number_appointments_booked": 0,
    "time_logged_out": 2592000,
    "total_messages": 40
}
```

... where time_logged_out is in seconds.
