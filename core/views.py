from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
def index_view(request):
    return HttpResponseRedirect(reverse("products:index"))


def logout_view(request):
    logout(request)
    return render(request, "core/logout.html")
