from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import \
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileViewForm
from .models import Profile
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token    
from django.core.mail import EmailMessage  
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes, force_text

def student_login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username} in student")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "users/Student_login.html", {"form": form})

def pcell_login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None and Profile.objects.get(user=user).user_type!='Student':
                login(request, user)
                messages.info(request, f"You are now logged in as {username} in pcell")
                return redirect('pcell_index')
            else:
                messages.error(request, "Invalid username or password or not authorized for login")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "users/Pcell_login.html", {"form": form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

@login_required
def show_users(request):
    all_users = Profile.objects.all()
    offer = []
    for i in range(len(all_users)):
        if all_users[i].placed_in != 'NoOffer':
            offer.append(all_users[i])

    return render(request, "placement/show_offers.html", {'offers': offer})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('email').endswith('@iiita.ac.in'):
            if User.objects.filter(email=form.cleaned_data.get('email')).exists():
                messages.error(request, "Email already exist")
                return render(request, "users/register.html", {"form": form})
            user = form.save(commit=False)
            user.is_active = False
            user.save()  
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, "Please confirm your email address to complete the registration")
            return redirect("/")
        else:
            messages.error(request, "Add Organization Email ID")
            return render(request, "users/register.html", {"form": form})
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        messages.info(request, "Thank you for your email confirmation.")
        return redirect("/")
    else:
        messages.info(request, "Activation Link Inactive")
        return redirect("/")

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        v_form = ProfileViewForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'v_form': v_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def delete_user(request, username):
    context = {}
    print(username)
    try:
        u = User.objects.get(id=username)
        u.delete()
        messages.success(
            request, f'Your account has been Deleted!!...Create New Account')
    except User.DoesNotExist:
        context['msg'] = 'User does not exist.'
    except Exception as e:
        context['msg'] = e.message

    form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

"""
def validate_login(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        user_name = request.GET.get("username")
        # check for the user name in the database.
        if User.objects.filter(username=user_name).exists():
            return JsonResponse({"valid": True}, status=200)

        # if username not found, then user can't login.
        else:
            return JsonResponse({
                "valid": False,
                "msg": "This user do not exist. Please register."
            }, status=200)


def is_username(s):
    for i in s.lower():
        if i not in 'abcdefghijklmnopqrstuvwxyz1234567890@.-_':
            return False
    return True


def validate(request, field):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":

        if field == 'username':

            user_name = request.GET.get("username", None)
            # check for valid username.
            if not is_username(user_name):
                return JsonResponse({
                    "valid": False,
                    "msg": "Enter a valid username. This value may contain \
                        only letters, numbers and @/./+/-/_ ."
                }, status=200)

            # check for the user name in the database.
            if User.objects.filter(username=user_name).exists():
                return JsonResponse({
                    "valid": False,
                    "msg": "A user with that username already exists."
                }, status=200)

            # if username not found, then user can be created.
            else:
                return JsonResponse({"valid": True}, status=200)

        elif field == 'email':

            user_email = request.GET.get("email", None)

            # check for email in database
            if User.objects.filter(email=user_email).exists():
                return JsonResponse({
                    "valid": False,
                    "msg": "A user with that e-mail already exists."
                }, status=200)
            else:
                return JsonResponse({"valid": True}, status=200)

        elif field == 'password1':

            user_password = request.GET.get("password1", None)

            res = None

            try:
                validate_password(password=user_password, user=User)

            except exceptions.ValidationError as e:
                res = list(e.messages)

            if res is not None:
                return JsonResponse({
                    "valid": False,
                    "msg": res,
                })
            else:
                return JsonResponse({"valid": True}, status=200)

        else:
            return JsonResponse({}, status=400)
"""