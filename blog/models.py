from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError


User = get_user_model()

class Tag(models.Model):
	name = models.CharField(max_length=15)

	def __str__(self):
		return self.name


class Blog(models.Model):
	title = models.CharField(max_length=20)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date_updated = models.DateField(auto_now=True)
	content = models.TextField()
	tags = models.ManyToManyField(Tag)							# limiting number of tags to be max 5, admin can add more than 5 but users can't
	slug = models.CharField(max_length=30, unique=True)

	@property
	def read_time(self):
		plain_content = strip_tags(self.content)
		word_count = len(plain_content.split())   
		avg = 200

		minutes = word_count // avg
		seconds = (word_count/avg - minutes)*0.6

		if seconds > 0.3:
			minutes += 1

		if minutes == 0:
			minutes += 1

		return minutes


	def __str__(self):
		return self.title


class Comment(models.Model):
	commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	body = models.CharField(max_length=1000)
	blog = models.ForeignKey(Blog, models.CASCADE)
	n_likes = models.IntegerField(default=0)
	n_dislikes = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.commenter.username} - {self.body}'