from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


def wrapper(func):
    def check_user_block(request):
        if request.user.is_authenticated and request.user.is_blocked:
            logout(request)
            messages.warning(request, 'You are blocked by admin.Please contact further info...')
            return redirect('user_login')
        return func(request)
    return check_user_block