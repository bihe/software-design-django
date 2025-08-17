from django.contrib.auth import logout
from django.db import connections
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse


# Create your views here.
def index_view(request):
    return HttpResponseRedirect(reverse("products:index"))


def logout_view(request):
    logout(request)
    return render(request, "core/logout.html")


def health_check(request):
    # Check database connections
    db_ok = all(conn.cursor().execute("SELECT 1") for conn in connections.all())

    status = db_ok
    status_code = 200 if status else 503
    return JsonResponse({"status": "ok" if status else "unhealthy"}, status=status_code)
