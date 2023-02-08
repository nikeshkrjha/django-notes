from rest_framework import serializers
from notes.models import Note, CustomUser, Label


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'name')


class NoteSerializer(serializers.ModelSerializer):

    uploaded_file = serializers.SerializerMethodField('get_uploaded_file')
    note_label =  LabelSerializer(many=False)

    class Meta:
        model = Note
        fields = ('id','content', 'created_at', 'updated_at', 'note_label', 'uploaded_file')
        # depth = 1

    def get_uploaded_file(self, obj):
        value_to_return = ""
        if obj.uploaded_file:
            value_to_return = obj.uploaded_file.url
        return value_to_return


class CustomUserSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'notes')
