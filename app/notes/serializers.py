from rest_framework import serializers
from notes.models import Note, CustomUser

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        # depth = 2

class CustomUserSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name','email', 'notes')