
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from .forms import RegisterForm
from users.tokens import account_activation_token
from users.tasks import send_confirmation_mail
from django.contrib import messages
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode 
from .models import User



class Register(View):
    form_class = RegisterForm
    template_name = 'users/login-register.html'
    print("1111111111111")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})

    print("22222222222222")

    def post(self, request):
        form = self.form_class(request.POST)
        print("valid")
        if form.is_valid():
            user = form.save(commit=False)
            print("post")
            user.is_active = False
            user.save()
            send_confirmation_mail(user)


            messages.success(request, 'We sent Confirmation Email !')
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})



def confirmation(request, uuidb64, token):
    uuid = force_str(urlsafe_base64_decode(uuidb64))
    user = User.objects.filter(id = int(uuid), is_active = False).first()
   
    if user and account_activation_token.check_token(user, token):
        messages.success(request, 'Your account activated') 
        user.is_active = True
        user.save()
        request.session['show_registration_message'] = True
        return redirect("login")
    else:
        messages.error(request, 'your link expired or link invalid')
        return redirect("/")


