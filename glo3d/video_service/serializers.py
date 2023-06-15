from email.policy import default
from rest_framework import serializers
import os


class VideoSerializer(serializers.Serializer):
    video = serializers.FileField()
    x = serializers.IntegerField(allow_null=True, min_value=0, default=0)
    x1 = serializers.IntegerField(allow_null=True, min_value=0, default=0)
    y = serializers.IntegerField(allow_null=True, min_value=0, default=0)
    y1 = serializers.IntegerField(allow_null=True, min_value=0, default=0)

    def validate_file(self, value):
        allowed_extensions = ['mp4', ]  # Set the allowed file extensions

        file_extension = value.name.split('.')[-1].lower()

        max_size = int(os.getenv("MAX_FILE_SIZE"))

        if file_extension not in allowed_extensions:
            raise serializers.ValidationError("Invalid file extension. Only mp4 files are allowed.")
        
        if value.size > max_size:
            raise serializers.ValidationError("File size exceeds the maximum limit of 2 MB.")

        return value
    
    def validate(self, data):
        data = super().validate(data)
        self.validate_file(data['video'])

        # Perform additional validations or manipulations on the data
        return data
