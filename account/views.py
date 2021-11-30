from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
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


def login(request):
    if request.user.is_authenticated:
        # Redirect to homepage if user is already logged in
        return redirect('category:homepage')

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:    # If user is not None, then the user exists in the database
            auth.login(request, user)
            return redirect('category:homepage')
        else:   # If user is None, then the user does not exist in the database
            messages.warning(request, 'Invalid credentials')
            return redirect('account:login')
    return render(request, "account/login.html")


# This decorator is used to prevent users from accessing the logout page if they are not logged in
@login_required(login_url='account:login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('account:login')


"""
Currently, Only super user can log in. Normal user cannot log in because they haven't activated their account through the email verification which will be implemented in the future.

When creating the account model for normal user I have set the is_active field to False and it'll be become True when the user clicks on the link sent to their email.
"""
