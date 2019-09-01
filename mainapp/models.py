from django.db import models

class Experiment(models.Model):
	start_date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField(auto_now=True)

class Temperature(models.Model):
	experiment = models.ForeignKey(Experiment, default=None)

	date = models.DateTimeField(auto_now_add=True)

	thermistor_1 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	thermistor_2 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	thermistor_3 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	thermistor_4 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	thermistor_5 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	thermistor_6 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	thermistor_7 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
	thermistor_8 = models.DecimalField(max_digits=4, decimal_places=1, null=True)

