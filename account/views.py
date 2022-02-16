from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.

# user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # form authentication
        if username == '':
            return redirect('user-login')
        elif password == '':
            return redirect('user-login')
        else:
            # user authenticate
            user = auth.authenticate(
                username = username,
                password = password
            )

            if user is None:
                messages.error(request, 'invalid user credentials')
                return redirect('account:user_login')
            else:
                auth.login(request, user)
                return redirect('home:index')

    else:
        return render(request, 'log_user.html')

# user registering
def user_reg(request):
    if request.method == 'POST':
        data = request.POST
        fname = data['fname']
        lname = data['lname']
        username = data['username']
        email = data['email']
        password1 = data['password']
        password2 = data['confirm_password']

        # confirm password
        if fname == '':
            messages.error(request, 'First name cannot be empty')
            return redirect('account:user_reg')
        elif lname == '':
            messages.error(request, "Last name cannot be emoty")
            return redirect('account:user_reg')
        elif username == '':
            messages.error(request, 'Username cannot be empty')
            return redirect('account:user_reg')
        elif email == '':
            messages.error(request, 'email field cannot be empty')
            return redirect('account:user_reg')
        elif password1 != password2:
            messages.error(request, 'passwords do not match')
            return redirect('account:user_reg')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
            return redirect('account:user_reg')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Already registered an account with this email')
            return redirect('account:user_reg')
        else:

            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email,
                first_name=fname,
                last_name=lname,
                is_staff=True,
                is_active=True,
            )

            # authenticate and login the user
            auth.login(request, user)
            return redirect('home:index')
    else:
        return render(request, 'reg_user.html')

# logout user
def logout_user(request):
    auth.logout(request)
    return redirect('account:user_login')

# user admin login
def admin_login(request):
    if request.method == 'POST':
        data = request.POST.get
        username = data('username')
        password = data('password')

        # form authentication
        if username == '':
            return redirect('admin-login')
        elif password == '':
            return redirect('admin-login')
        else:
            # user authenticate
            user = auth.authenticate(
                username = username,
                password = password
            )

            if user is None:
                messages.error(request, 'invalid user credentials')
                return redirect('account:admin-login')
            else:
                auth.login(request, user)
                return redirect('loan:dashboard')

    else:
        return render(request, 'log_admin.html')

def admin_reg(request):
    if request.method == 'POST':
        data = request.POST
        fname = data['fname']
        lname = data['lname']
        username = data['username']
        email = data['email']
        password1 = data['password']
        password2 = data['confirm_password']

        # confirm password
        if fname == '':
            messages.error(request, 'First name cannot be empty')
            return redirect('account:user_reg')
        elif lname == '':
            messages.error(request, "Last name cannot be emoty")
            return redirect('account:user_reg')
        elif username == '':
            messages.error(request, 'Username cannot be empty')
            return redirect('account:user_reg')
        elif email == '':
            messages.error(request, 'email field cannot be empty')
            return redirect('account:user_reg')
        elif password1 != password2:
            messages.error(request, 'passwords do not match')
            return redirect('account:user_reg')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
            return redirect('account:user_reg')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Already registered an account with this email')
            return redirect('account:user_reg')
        else:

            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email,
                first_name=fname,
                last_name=lname,
                is_staff=True,
                is_active=True,
                is_superuser=True,
            )

            # authenticate and login the user
            auth.login(request, user)
            return redirect('loan:dashboard')
    else:
        return render(request, 'admin_reg.html')
def admin_logout(request):
    auth.logout(request)
    return redirect('account:admin-login')
