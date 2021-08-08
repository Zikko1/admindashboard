from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from . forms import CreateUserForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request,f'Hi {user_name}!, you have successfully created your account. Kindly login to continue')
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context ={
    'form':form
    }
    return render(request,'user/register.html',context)

def profile(request):
    return render(request,'user/profile.html')

def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form':profile_form,
        }
    return render(request,'user/profile_update.html',context)

# CREATING CUSTOM PASSWORD RESET MESSAGE
def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Password Reset'
                    email_template_name = 'user/password_message.txt'
                    parameters = {
                    'email':user.email,
                    'domain': 'http://127.0.0.1:8000',
                    'site_name': 'The Gentlemens Club',
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name,parameters)
                    try:
                        send_mail(subject,email,'',[user.email],fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form': password_form,
        }
    return render(request,'user/password_reset.html',context)
