#!/usr/bin/env python
import unittest
import os
import json
from app import create_app
from app import util

class TestHeathenLed(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.util = util

    def test_load_file_json(self):
        f = self.util.load_file_json()
        self.assertIsInstance(f, list)

    def test_activity_patient_id_6(self):
        res = self.client().get('/v1/activity?patient_id=6')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, bytes)
        data = json.loads(res.data)
        self.assertEqual(data["total_messages"], 39)
        self.assertEqual(data["number_appointments_booked"], 0)

    def test_activity_patient_id_7(self):
        res = self.client().get('/v1/activity?patient_id=7')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, bytes)
        data = json.loads(res.data)
        self.assertEqual(data["total_messages"], 43)
        self.assertEqual(data["number_appointments_booked"], 0)

    def test_activity_no_patient_id(self):
        res = self.client().get('/v1/activity')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, bytes)
        data = json.loads(res.data)
        self.assertEqual(data["total_messages"], 240)
        self.assertEqual(data["number_appointments_booked"], 4)

    def test_activity_start_date(self):
        res = self.client().get('/v1/activity?start_date=2018-01-01T00:00:00')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, bytes)
        data = json.loads(res.data)
        self.assertEqual(data["total_messages"], 0)
        self.assertEqual(data["number_appointments_booked"], 0)

    def test_activity_end_date(self):
        res = self.client().get('/v1/activity?start_date=2017-01-01T00:00:00&end_date=2017-01-01T00:00:01')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, bytes)
        data = json.loads(res.data)
        self.assertEqual(data["total_messages"], 0)
        self.assertEqual(data["number_appointments_booked"], 0)

    def test_activity_all_records(self):
        res = self.client().get('/v1/activity?start_date=2012-01-01T00:00:00&end_date=2019-01-01T00:00:01')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, bytes)
        data = json.loads(res.data)
        self.assertEqual(data["total_messages"], 1816)
        self.assertEqual(data["number_appointments_booked"], 28)

    def test_activity_logged_out(self):
        res = self.client().get('/v1/activity?start_date=2012-01-01T00:00:00&end_date=2019-01-01T00:00:01&patient_id=4')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, bytes)
        data = json.loads(res.data)
        self.assertEqual(data["total_messages"], 256)
        self.assertEqual(data["number_appointments_booked"], 7)
        self.assertEqual(data["time_logged_out"], 212379556)
