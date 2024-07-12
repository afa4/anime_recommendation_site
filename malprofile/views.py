from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "malprofile/index.html")

def profile_submit(request):
    print(request.POST['profile_name'])
    return HttpResponse("You're submitting your profile!")
    