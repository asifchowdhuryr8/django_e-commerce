from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            # I have not added phone_number argument in the create_user method of the Account class. That's why I have to add it here manually after creating the user.
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'You have successfully registered!')
            return redirect('account:register')
        else:
            messages.info(request, 'An error occurred during registration.')
    else:
        # Use it inside the else block otherwise field errors will not work in template file
        form = RegistrationForm()
    context = {'form': form}
    return render(request, "account/register.html", context)
