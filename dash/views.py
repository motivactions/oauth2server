from django.shortcuts import render


def index(request):
    return render(request, "dash_index.html")
