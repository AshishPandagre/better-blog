from django.contrib import admin
from django.urls import path, include
from accounts import git_update_view

urlpatterns = [
	path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('update_server/', git_update_view.update, name='production-update'),
    path('', git_update_view.home, name='temp-home'),
]
