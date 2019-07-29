from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def index(request):
    return render(request, 'index.html')
    

# def testauth(request, id):
#     user = get_object_or_404(User, id=id)
#     user_auth = authenticate(username='test', password='test')
#     if user_auth is not None:
#         return HttpResponse(str(user_auth))
#     else:
#         return HttpResponse('nobody with this name')
