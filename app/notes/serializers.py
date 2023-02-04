from rest_framework import serializers
from notes.models import Note, CustomUser

class NoteSerializer(serializers.ModelSerializer):
    uploaded_file = serializers.SerializerMethodField('get_uploaded_file')
    class Meta:
        model = Note
        # fields = '__all__'
        fields = ('content','created_at','updated_at','created_by','uploaded_file')

    def get_uploaded_file(self, obj):
        return obj.uploaded_file.url

    # def to_representation(self, data):
    #     data = super(NoteSerializer, self).to_representation(data)
    #     data['uploaded_file'] = self.instance.uploaded_file.url
    #     return data

class CustomUserSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name','email', 'notes')