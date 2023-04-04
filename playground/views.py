from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def say_hello(request):
    # pull data from DB
    # send email
    # transform datat
    return render(request, 'hello.html', context={'name': 'vahid'})
