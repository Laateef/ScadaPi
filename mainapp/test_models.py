from django.test import TestCase
from django.urls import resolve

from mainapp.models import Experiment, Temperature

from datetime import datetime

class ExperimentModelTest(TestCase):
	def test_default_experiment(self):
		e = Experiment()

		self.assertEqual(e.start_date, None)
		self.assertEqual(e.end_date, None)

class TemperatureModelTest(TestCase):
	def test_default_temperature(self):
		t = Temperature()

		self.assertEqual(t.thermistor_1, None)
		self.assertEqual(t.thermistor_2, None)
		self.assertEqual(t.thermistor_3, None)
		self.assertEqual(t.thermistor_4, None)
		self.assertEqual(t.thermistor_5, None)
		self.assertEqual(t.thermistor_6, None)
		self.assertEqual(t.thermistor_7, None)
		self.assertEqual(t.thermistor_8, None)


	def test_temperature_is_related_to_experiment(self):
		e = Experiment.objects.create()
		t = Temperature()
		t.experiment = e
		t.save()
		
		self.assertIn(t, e.temperature_set.all())

