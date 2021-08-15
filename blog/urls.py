from django.urls import path
from . import views


urlpatterns = [
	
	path('addComment/', views.addComment, name='addComment'),
	path('deleteComment/', views.deleteComment, name='deleteComment'),
	path('<str:slug>', views.BlogDetail.as_view(), name='blog-detail'),
	# path('', views.BlogList.as_view(), name='blog-list')

]
