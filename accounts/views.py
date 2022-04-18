from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
import random
from utils import send_otp_code
from .models import OtpCode
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.changed_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.changed_data['phone_number'], code=random_code)
            request.session['user_registration-info'] = {
                'phone_number': form.changed_data['phone_number'],
                'email': form.changed_data['email'],
                'full_name': form.changed_data['full_name'],
                'password': form.changed_data['password'],
            }
            messages.success(request, 'We sent verification code', extra_tags='success')
            return redirect('accounts:verify_code')
        return redirect('home:home')
