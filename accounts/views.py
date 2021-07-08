from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import User, UserSession, Profile
from .forms import UserRegisterForm, UpdateProfileForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView
from user_agents import parse
from django.contrib.sessions.models import Session


class UpdateProfile(LoginRequiredMixin, UpdateView):
	model = Profile
	form_class = UpdateProfileForm
	template_name = 'registration/update_profile.html'
	success_url = reverse_lazy('get-profile')

	def get_object(self):
		print('*'*10)
		print(self.request.user.id)
		return Profile.objects.get(user=self.request.user)


class UserAnonymous(UserPassesTestMixin):
	def test_func(self):
		if self.request.user.is_authenticated:
			return False
		return True

	def handle_no_permission(self):
		return redirect('get-profile')


class SignUpView(UserAnonymous, SuccessMessageMixin, CreateView):
	redirect_field_name = 'get-profile'
	template_name = 'registration/signup.html'
	form_class = UserRegisterForm
	success_url = reverse_lazy('get-profile')
	success_message = "Your profile was created successfully."

	def form_valid(self, form):
		email = form.cleaned_data.get('email')
		if not User.objects.filter(email__iexact=email).exists():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(self.request)
			mail_subject = "Activate your account"
			message = render_to_string('registration/email_template.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			print('*'*20)
			print("Here email will be sent to ", to_email)
			send_mail(mail_subject, message, 'ashishpandagre4@gmail.com', [to_email], fail_silently=True)
			return HttpResponse("Verification email has been sent to you.")

		else:
			return HttpResponse("An email already exists.")


def activate(request, uidb64, token):
	User = get_user_model()
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
	else:
		return HttpResponse('Activation link is invalid!')
	

def logout_session(request, pk):
	session = UserSession.objects.get(id=pk)
	if session.user != request.user:
		return HttpResponse("Access Denied.")
	else:
		sess_key = session.sess_key
		s = Session(pk=sess_key)
		s.delete()
		UserSession.objects.filter(user=request.user, sess_key=sess_key).delete()
		return HttpResponse("Success")


class GetProfile(LoginRequiredMixin, DetailView):
	model = User
	template_name = 'registration/profile.html'
	context_object_name = 'user'

	def get_object(self):
		return self.request.user

	def get_context_data(self, *args, **kwargs):
		context = super(GetProfile, self).get_context_data(*args, **kwargs)
		
		sess_key = self.request.session.session_key
		sessions = UserSession.objects.filter(user=self.request.user).exclude(sess_key=sess_key)
		context['sessions'] = sessions

		return context


class NewLoginView(LoginView):
	def form_valid(self, form):
		data = super().form_valid(form)

		sess_key = self.request.session.session_key
		print('*'*10)
		print(sess_key)
		user_agent_string = self.request.POST.get('user-agent', 'unknown')
		
		if user_agent_string != 'unknown':
			user_agent = parse(user_agent_string)
			user_agent_string = user_agent.device.family + " " + user_agent.browser.family + " " + user_agent.os.family

		user_session = UserSession.objects.create(
			user = self.request.user,
			device = user_agent_string,
			sess_key = sess_key
		)
		user_session.save()

		return data

def ua_string(request):
	if request.method == "GET":
		return render(request, 'ua-string.html')
	else:
		user_agent_string = request.POST.get('user-agent', 'unknown')
		if user_agent_string != 'unknown':
			user_agent = parse(user_agent_string)
			return HttpResponse(f'{user_agent} || device-family={user_agent.device.family}, browser-family={user_agent.browser.family}, os-family={user_agent.os.family}')
		return HttpResponse('unknown')
