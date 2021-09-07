from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
import random

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


User = get_user_model()

class Tag(models.Model):
	name = models.CharField(max_length=15)

	def __str__(self):
		return self.name


CHOICES = (
	(1, "Publish"),
	(0, "Draft")
)


class Blog(models.Model):
	title = models.CharField(max_length=20)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date_updated = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	tags = models.ManyToManyField(Tag)							# limiting number of tags to be max 5, admin can add more than 5 but users can't
	slug = models.CharField(max_length=30, unique=True)
	status = models.IntegerField(choices=CHOICES, default=0)
	img = models.ImageField(upload_to='posts', blank=True, null=True)
	n_views = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		if self._state.adding:
			slug = slugify(self.title)
			if Blog.objects.filter(slug=slug).exists():
				self.slug = slug+str(random.randrange(0, 10000))
			else:
				self.slug = slug
		super(Blog, self).save(*args, **kwargs)


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


class Bookmark(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f'{self.user.username} - {self.blog}'




OPINIONS = (
	(-1, 'dislike'),
	(0, 'neutral'),
	(1, 'like')
)
class Opinion(models.Model):
	user = models.ForeignKey(User, models.CASCADE)
	# comment = models.ForeignKey(Comment, models.CASCADE)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField(null=True)
	comment = GenericForeignKey('content_type', 'object_id')

	action = models.IntegerField(choices=OPINIONS, default=0)



class Comment(models.Model):
	commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	body = models.CharField(max_length=1000)
	blog = models.ForeignKey(Blog, models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	opinions = GenericRelation(Opinion)

	def __str__(self):
		return f'{self.commenter.username} - {self.body}'

	class Meta:
		ordering = ['-date_created']

	def n_likes(self):
		print('*'*20)
		print(self.opinions.filter(action=1))
		# return 1
		return self.opinions.filter(action=1).count()

	def n_dislikes(self):
		# return 1
		return self.opinions.filter(action=-1).count()


class Reply(models.Model):
	commenter = models.ForeignKey(User, models.SET_NULL, null=True)
	body = models.CharField(max_length=1000)
	comment = models.ForeignKey(Comment, models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	opinions = GenericRelation(Opinion)

	def __str__(self):
		return f'{self.commenter.username} - {self.body}'

	class Meta:
		ordering = ['-date_created']

	def n_likes(self):
		# return 1
		return self.opinions.filter(action=1).count()

	def n_dislikes(self):
		# return 1
		return self.opinions.filter(action=-1).count()
