from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from notes.models import Note, CustomUser
from notes.serializers import NoteSerializer, CustomUserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
import logging


# Create your views here.

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def notes_list(request):
    """
    List all code notes, or create a new snippet.
    """
    if request.method == 'GET':
        notes = Note.objects.filter(created_by__id=request.user.id)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def users_list(request):
    """
    List all the app users.
    This method can accessed by staff users only
    """
    if request.method == 'GET' and request.user.is_staff == True:
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    """
    Returns details of a user
    """
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET' and request.user == user:
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
        if request.method == 'GET':
            serializer = NoteSerializer(note)
            # serializer.data['uploaded_file'] = note.uploaded_file.url
            # serializer.data['url'] = note.uploaded_file.url
            # dict = {'url': note.uploaded_file.url}
            return Response(serializer.data)
        elif request.method == 'DELETE':
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            request.data["created_by"] = request.user.id
            serializer = NoteSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', ])
def register_user(request):
    """
    Register a new user
    Returns auth token for the user. The token needs to be addes to all the requests after authentication
    """
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        logger.debug(request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get_or_create(user=user)
            data = get_user_response_dict(user, token)
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            logger.debug("***** User Creattion Failed *****")
            return Response({"error": "Request Failed !!!!"}, status=status.HTTP_400_BAD_REQUEST)


def get_user_response_dict(user, token):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "token": str(token[0]) # token is a tuple, returning first item of the tuple in response
    }
