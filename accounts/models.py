from django.db import models
from django.contrib.auth.models import User, AbstractUser

genders = (
	('m', 'Male'),
	('f', 'Female')
)

class User(AbstractUser):
	first_name = None
	last_name = None

	def __str__(self):
		return self.username


countries = (
	('India', 'India'),
	('United States', 'United States'),
	('Spain', 'Spain'),
	('Germany', 'Germany'),
	('France', 'France')
)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	birthday = models.DateField(null=True, blank=True)
	gender = models.CharField(choices=genders, null=True, blank=True, max_length=10)
	phone = models.CharField(max_length=20, null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)
	number = models.IntegerField(null=True, blank=True)
	city = models.CharField(max_length=30, null=True, blank=True)
	country = models.CharField(choices=countries, max_length=30, null=True, blank=True)
	zip_code = models.CharField(max_length=6, null=True, blank=True)

	def __str__(self):
		return self.user.username

class UserSession(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	device = models.CharField(max_length=200)
	login_time = models.DateTimeField(auto_now_add=True)
	sess_key = models.CharField(max_length=200)

	def __str__(self):
		return f'{self.user.username} - {self.device}'
