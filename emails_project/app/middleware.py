# middleware.py в приложении accounts
from django.shortcuts import redirect
from django.urls import reverse

class AccountConfirmationRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.userprofile.is_confirmed and request.path not in [reverse('confirm_account', args=[request.user.userprofile.confirmation_token]), reverse('logout')]:
                return redirect('account_not_confirmed')
        return self.get_response(request)
