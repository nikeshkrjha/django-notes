from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from notes.models import Note, CustomUser
from notes.serializers import NoteSerializer, CustomUserSerializer

# Create your views here.
@csrf_exempt
def notes_list(request):
    """
    List all code notes, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Note.objects.all()
        serializer = NoteSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def users_list(request):
    """
    List all code users.
    """
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def user_detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)