from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# Create your views here.

# User Account Activation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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

            # Send email to the user to activate the account
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(subject, message, to=[to_email])
            send_mail.send()
            return redirect('/account/login/?verify=email_verification&email='+email)
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
            messages.warning(
                request, 'Invalid credentials either your given details is incorrect or your account is not activated yet.')
            return redirect('account:login')
    return render(request, "account/login.html")


# This decorator is used to prevent users from accessing the logout page if they are not logged in
@login_required(login_url='account:login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('account:login')


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated!')
        return redirect('account:login')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('account:login')


@login_required(login_url='account:login')
def dashboard(request):
    context = {}
    return render(request, "account/dashboard.html", context)
