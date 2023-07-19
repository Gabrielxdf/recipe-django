from django.http import HttpResponse

from django.shortcuts import render


def home(request):
    return render(request, 'recipes/home.html', context={
        'name':'Gabriel Nascimento',
        'idade':'23',
    })


def sobre(request):
    return HttpResponse("SOBRE")


def contato(request):
    return HttpResponse("CONTATO")
