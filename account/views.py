from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .utils import send_email, get_user
from cart.models import Cart, CartItem
from cart.views import get_or_set_session_id
# Create your views here.

# User Account Activation
from django.contrib.auth.tokens import default_token_generator


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
            subject = 'Activate Your Account'
            template = 'account_activation_email'
            send_email(request, user, email, subject, template)
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
            try:
                cart = Cart.objects.get(cart_id=get_or_set_session_id(request))
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
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
    user = get_user(uidb64, Account, False)
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


def forgot_password(request):
    """If user email address exist in the database, then send an email to the user with a link to reset the password. The link uses validate_reset_password_link route to validate the link"""
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # Send email to the user to reset the account password
            subject = 'Reset Password'
            template = 'account_reset_password_email'
            send_email(request, user, email, subject, template)
            messages.success(
                request, 'An email has been sent to your email address to reset your password.')
            return redirect('account:login')
        else:
            messages.warning(request, 'Account does not exist.')
            return redirect("account:forgot_password")
    else:
        return render(request, "account/forgot_password.html")


def validate_reset_password_link(request, uidb64, token):
    """Store the user id in the session and redirect user to the reset_password page"""
    user, uid = get_user(uidb64, Account, True)
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid    # Store the user id in the session
        return redirect('account:reset_password')
    else:
        messages.warning(request, 'Activation link is invalid or expired!')
        return redirect('account:forgot_password')


def reset_password(request):
    """Set a new password for the user if he comes from a valid link"""
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            # Get the user id from the session which was set in the validate_reset_password_link function
            uid = request.session['uid']
            # Get the user from the database using the user id
            user = Account._default_manager.get(pk=uid)
            # Set the password. set_password method is provided by Django to create a hashed password.
            user.set_password(password)
            user.save()
            messages.success(
                request, 'Your password has been changed successfully.')
            return redirect('account:login')
        else:
            messages.warning(
                request, 'Password and confirm password do not match.')
            return redirect('account:reset_password')
    else:
        return render(request, "account/reset_password.html")
