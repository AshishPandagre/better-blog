from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('email', 'password1', 'password2')

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.username = user.email.split('@')[0]

		if commit:
			user.save()
		return user

class UpdateProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ('user',)