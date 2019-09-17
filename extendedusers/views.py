from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import ExtendedUser

# are you using the default user? ok

User = get_user_model()

class VerifyAccount(generic.View):

    def get(self, request, token_uuid, user_email):
        user_objects = User.objects.filter(email=user_email)

        # I did this because with django's default
        #User model, the email address is not unique.
        user_object = None
        if user_objects.count() > 0:
            user_object = user_objects[0]
        
        if hasattr(user_object, 'profile'):
            profile = user_object.profile # I'm thinking we should've tied the tokens to the User model directly...but it'll still work, just messier
            # yeah
            if profile.tokens.count() > 0:
                # token exists | we'll need to make 1to1, but i'll leave it for now
                if profile.tokens.filter(token=token_uuid).exists():
                    profile.set_verified()
                    messages.success(request, 'Account was verified correctly! Now you can start using the application')
                    # return HttpResponseRedirect(reverse('index'))
                    return HttpResponse('cool, worked')
                else:
                    return HttpResponse("Token invalid")
            else:
                return HttpResponse("No tokens found on account")
        else:
            # Unwanted scenario
            return HttpResponse("Account setup invalid")


verify_account_view = VerifyAccount.as_view()

