from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from models import Character

def hello(request):
  return HttpResponse('Hello, Teledu!')

def charSheet(request, charId):
  character = get_object_or_404(Character, id = charId)
  return render(request, 'characterSheet.html', {'character': character})
