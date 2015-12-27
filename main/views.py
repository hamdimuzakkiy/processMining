from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
import make_graph
from django import forms

def index(request):
    return redirect('/main/form')

def handleFile(file_name,f):
    with open('uploads/'+file_name  , 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return

def makeGraph(request):
    try:
        file_content = request.FILES['files']
        file_name = request.FILES['files'].name
        handleFile(file_name,file_content)
        graph = make_graph.makeGraph("uploads/"+file_name)
        context = {
            'list_graph' : graph,
            'res' : graph,
        }
        return render(request, 'main/result.html',context)
    except:
        # pass
        return redirect('/main/form')

def form(request):
    return render(request, 'main/form2.html')