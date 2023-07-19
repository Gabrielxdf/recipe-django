from django.http import HttpResponse

# from django.shortcuts import render


# Create your views here.
# HTTP REQUEST <- HTTP RESPONSE
# HTTP REQUEST
def home(request):
    return HttpResponse("HOME")
    # return HTTP Response


def sobre(request):
    return HttpResponse("SOBRE")


def contato(request):
    return HttpResponse("CONTATO")
