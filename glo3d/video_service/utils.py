import cv2
import os
import shutil
import uuid

from PIL import Image

def extract_frames_from_video(validated_data):
    video_file = validated_data['video']
    crop_x = validated_data['x']
    crop_y = validated_data['y']
    crop_x1 = validated_data['x1']
    crop_y1 = validated_data['y1']

    video_input = os.getenv("VIDEO_INPUT")
    resized_frames_dir = os.getenv("RESIZED_FRAMES_DIR")
    os.makedirs(video_input, exist_ok=True)
    os.makedirs(resized_frames_dir, exist_ok=True)

    file_extension = os.path.splitext(video_file.name)[1]
    video_file.name = f'{uuid.uuid4().hex}{file_extension}'
    video_path = os.path.join(video_input, video_file.name)
        
    # Save the video file to the temporary directory
    with open(video_path, 'wb') as file:
        for chunk in video_file.chunks():
            file.write(chunk)
    video = cv2.VideoCapture(video_path)
    
    # Extract frames from the video
    num_frames = 24
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = total_frames // num_frames
    
    # Create a zip file containing the frames
    frame_numbers = []
    for i in range(num_frames):
        frame_number = i * frame_interval
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()

        if ret:
            # Save the frame as an image file
            frame_path = os.path.join(resized_frames_dir, f'frame_{frame_number}.jpg')
            cv2.imwrite(frame_path, frame)
            
            # Store the frame number for later use
            frame_numbers.append(frame_number)
    quality_resolutions = {'2K': (2560, 1440), '1080p': (1920, 1080), '720p': (1280, 720)}
    os.makedirs(resized_frames_dir, exist_ok=True)
    for frame_number in frame_numbers:
        original_frame_path = os.path.join(resized_frames_dir, f'frame_{frame_number}.jpg')
        
        for quality, resolution in quality_resolutions.items():
            resized_frame_path = os.path.join(resized_frames_dir, f'frame_{frame_number}_{quality}.jpg')
            crop_and_resize_image(original_frame_path, resized_frame_path, crop_x, crop_y, crop_x1, crop_y1, resolution)
    
    zip_file_name = create_zip_file(resized_frames_dir, video_file.name)
    
    for frame_file in os.listdir(resized_frames_dir):
        frame_path = os.path.join(resized_frames_dir, frame_file)
        os.remove(frame_path)
    os.rmdir(resized_frames_dir)

    return zip_file_name


def create_zip_file(directory_path, zip_path):
    shutil.make_archive(zip_path, 'zip', directory_path)


def crop_and_resize_image(input_path, output_path, x, y, x1, y1, target_resolution):
    image = Image.open(input_path)
    validate_image_coordinates(input_path, x, y, x1, y1)
    cropped_image = image.crop((x, y, x1, y1))
    resized_image = cropped_image.resize(target_resolution)
    resized_image.save(output_path, 'JPEG')


def validate_image_coordinates(image_path, x, y, x1, y1):
    # Open the image
    image = Image.open(image_path)
    
    # Get the image dimensions
    image_width, image_height = image.size
    
    # Validate the coordinates
    if x < 0 or y < 0 or x1 < 0 or y1 < 0:
        raise ValueError("Coordinates cannot be negative.")
    if x >= image_width or y >= image_height or x1 >= image_width or y1 >= image_height:
        raise ValueError("Coordinates exceed the image dimensions.")
    
    return True