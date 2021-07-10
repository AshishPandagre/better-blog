from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Blog, Tag, Comment



class BlogDetail(TemplateView):
	template_name = 'blog/blog-detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs['slug']
		blog = get_object_or_404(Blog, slug=slug)
		comments = Comment.objects.filter(blog=blog)
		context['blog'] = blog
		context['comments'] = comments
		return context
