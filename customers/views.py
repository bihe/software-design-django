from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import UpdateView

from .models import Customer


# Create your views here.
# https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-editing/
class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ["first_name", "last_name", "credit"]


class CustomerProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "customers/index.html")
