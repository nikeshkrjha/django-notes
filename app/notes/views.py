from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from notes.models import Note, CustomUser
from notes.serializers import NoteSerializer, CustomUserSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def notes_list(request):
    """
    List all code notes, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Note.objects.all()
        serializer = NoteSerializer(snippets, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def users_list(request):
    """
    List all code users.
    """
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, safe=False)


@api_view(['GET', 'POST'])
def user_detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def note_detail(request, pk):
    """
    Retrieve, update or delete a note.
    A user can only retrieve, delete or update a note if they are the one who created it.
    """
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if note.created_by == request.user:
        print('\nYohooooo\n')
        if request.method == 'GET':
            serializer = NoteSerializer(note)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
