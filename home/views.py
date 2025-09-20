from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'home/register.html'
    success_url = '/smart/notes'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes.list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()               # create the user
        login(self.request, user)        # log them in
        return redirect(self.success_url)

@method_decorator(csrf_exempt, name='dispatch')
class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'

@method_decorator(csrf_exempt, name='dispatch')
class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'

@method_decorator(csrf_exempt, name='dispatch')
class HomeView(TemplateView):
    template_name = "home/welcome.html"
    extra_context = {'now': datetime.today()}

@method_decorator(csrf_exempt, name='dispatch')
class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/authorized.html'
    login_url = '/admin'
    

# def home(request):
#     # return HttpResponse('Welcome to SmartNotes!')
#     return render(request, 'home/welcome.html', {'now': datetime.today()})

# @login_required(login_url='/admin')
# def authorized(request):
#     return render(request, 'home/authorized.html', {})