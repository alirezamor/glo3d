import os
import io
import zipfile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import VideoSerializer
from .utils import extract_frames_from_video


class FrameExtractionView(APIView):
    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the uploaded video file from the serializer
        video_file = serializer.validated_data['video']
        
        zip_file_name = extract_frames_from_video(validated_data=serializer.validated_data)

        response = Response()
        response['Content-Disposition'] = f'attachment; filename="{zip_file_name}"'
        response['Content-Type'] = 'application/zip'
        return response
