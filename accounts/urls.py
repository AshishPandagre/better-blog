from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path('profile/', views.GetProfile.as_view(), name='get-profile'),
	path('settings/', views.UpdateProfile.as_view(), name='update-profile'),
	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('emailVerification/<uidb64>/<token>', views.activate, name='activate'),
	path('security/', auth_views.PasswordChangeView.as_view(), name='password_change'),
	path('login/', views.NewLoginView.as_view(redirect_authenticated_user=True), name='login'),
	path('logout-session/<int:pk>/', views.logout_session, name='logout-session'),
	path('', include('django.contrib.auth.urls')),
]

