import json
from dateutil.parser import parse
from dateutil.relativedelta import *
from flask import request, jsonify, abort
from flask_api import FlaskAPI
from instance.config import app_config
from app import util

def create_app(config_name, data_path="data/user_actions"):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    data = util.load_file_json(data_path)

    @app.route("/v1/activity", methods=['GET'])
    def activity():
        patient_id = request.args.get("patient_id", None)
        start_date = parse(request.args.get("start_date", "2017-01-01T00:00:00"))
        end_date_default = start_date + relativedelta(days=+30)
        if request.args.get("end_date"):
            end_date = parse(request.args.get("end_date"))
        else:
            end_date = end_date_default

        total_messages = 0
        number_appointments_booked = 0
        last_login_time = None
        last_logout_time = None
        login_times = []

        for rec in data:
            date_rec = parse(rec.get("datetime"))
            start_delta = relativedelta(date_rec, start_date)
            end_delta = relativedelta(end_date, date_rec)

            """ only deal with records withing given start/end dates """

            if start_delta.days + start_delta.hours + start_delta.minutes + start_delta.seconds < 0:
                continue
            if end_delta.days + end_delta.hours + end_delta.minutes + end_delta.seconds < 0:
                continue

            """ if given a patient_id, accumulate total time logged out """

            if patient_id:
                if int(patient_id) == rec.get("patient_id"):
                    if rec.get("action") == "message":
                        total_messages += 1
                    if rec.get("action") == "book_appointment":
                        number_appointments_booked += 1
                    if rec.get("action") == "login":
                        last_login_time = date_rec
                    if last_login_time and rec.get("action") == "logout":
                        seconds_logged_in = int(date_rec.strftime("%s")) - int(last_login_time.strftime("%s"))
                        login_times.append(seconds_logged_in)
                        last_login_time = None
            else:
                if rec.get("action") == "message":
                    total_messages += 1
                if rec.get("action") == "book_appointment":
                    number_appointments_booked += 1

        """ calculate total time logged out """

        total_seconds_logged_in = 0
        for period_logged_in in login_times:
            total_seconds_logged_in += period_logged_in
        report_period_in_seconds = int(end_date.strftime("%s")) - int(start_date.strftime("%s"))
        total_seconds_logged_out = report_period_in_seconds - total_seconds_logged_in
        output = {
            "total_messages": total_messages,
            "number_appointments_booked": number_appointments_booked,
        }
        if patient_id:
            output["time_logged_out"] = total_seconds_logged_out
        return output

    return app
