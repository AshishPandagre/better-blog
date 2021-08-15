from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Blog, Tag, Comment
from .forms import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse



class BlogDetail(TemplateView):
	template_name = 'blog/blog-detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		blog = get_object_or_404(Blog, slug=slug)
		comments = Comment.objects.filter(blog=blog)

		if self.request.user.is_authenticated:
			if not Comment.objects.filter(commenter=self.request.user, blog=blog).exists():
				form = CommentForm()
				context['commentForm'] = form

		context['blog'] = blog
		context['comments'] = comments
		return context



def addComment(request):
	data = json.loads(request.body)
	blogId = data['blogId']
	comment = data['comment']
	blog = get_object_or_404(Blog, id=blogId)
	if Comment.objects.filter(commenter=request.user, blog=blog).exists():
		response = json.dumps({"response": "Comment already exists."})
	else:
		comment = Comment(commenter=request.user, body=comment, blog=blog)
		comment.save()
		response = json.dumps({'response': 'OK', 'comment': comment.body, 'date_created': comment.date_created, 'n_likes': comment.n_likes}, default=str)
	return HttpResponse(response)


def deleteComment(request):
	data = json.loads(request.body)
	blogId = data['blogId']
	commentId = data['commentId']
	comment = get_object_or_404(Comment, id=commentId)
	comment.delete()
	return HttpResponse(json.dumps({'response': 'OK'}))

