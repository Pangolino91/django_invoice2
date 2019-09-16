# verification login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


class VerificationRequiredMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            messages.info(request, 'Please login to see this page')
            return HttpResponseRedirect(reverse('login'))
        elif not request.user.profile.verified:
            messages.info(request, 'Your account needs to be verified in order to start using the application. Please check your email and follow the link provided for the verification.')
            return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

# verification required decorator (for function based view)

def verification_required(function):
    def wrapper(request, *args, **kwargs):
        user=request.user  
        if not user.profile.verified:
            messages.info(request, 'Your account needs to be verified in order to start using the application. Please check your email and follow the link provided for the verification.')
            return HttpResponseRedirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)
    return wrapper

# end of verification testing
