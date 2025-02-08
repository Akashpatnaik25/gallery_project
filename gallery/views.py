# system imports
import qrcode, io

# library imports
from django.shortcuts import render
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status

from django.http import JsonResponse
from django.shortcuts import render

from gallery.serializers import GallerySerilaizers



# helper imports
from .models import UploadedImage
from user.models import UserProfile
from helper import keys , functions




@csrf_exempt
@api_view(['POST'])
def upload_image_api(request):
    if 'image' not in request.data or keys.IMAGE_TYPE not in request.data:
        return Response({keys.Error: "Image and image_type are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    image = request.data.get('image')
    image_type = request.data.get(keys.IMAGE_TYPE)
    validation_error = functions.validate_image(image)
    print(image_type,validation_error)
    if validation_error:
        return Response({keys.Error: validation_error}, status=status.HTTP_400_BAD_REQUEST)
    user, error_response = functions.get_user_from_token(request)

    if error_response:
        return error_response  # Return if token is invalid
    
    print(f"Authenticated user: {user.username}")  # Debugging info

    user_profile = UserProfile.objects.filter(user=user).first()
    if not user:
        return Response({keys.Error: "No user found."}, status=status.HTTP_400_BAD_REQUEST)
    
    image_instance = UploadedImage.objects.create(user=user_profile, image=image, image_type=image_type)
    qr = qrcode.make(image_instance.image.url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    image_instance.qr_code.save(f"qr_{image_instance.id}.png", ContentFile(buffer.getvalue()), save=True)
    
    return Response({keys.Message: "Successfully added", "image_id": image_instance.id}, status=status.HTTP_201_CREATED)



def gallery(request):
    return render(request, 'gallery/gallery.html')


@api_view(['GET'])
def image_gallery_api(request):
    """This view is used to show the gallery images with JWT authentication"""
    
    user, error_response = functions.get_user_from_token(request)
    if error_response:
        return error_response  # Return if token is invalid
    
    user_profile = UserProfile.objects.filter(user=user).first()
    
    if not user_profile:
        return JsonResponse({keys.Error: "User profile not found"}, status=400)
    
    images = UploadedImage.objects.filter(user=user_profile)
    
    if not images:
        return Response({keys.Message: "Successfully Loaded","images" : [],'first_type': "portrait"}, status=status.HTTP_200_OK)
        # return render(request, 'gallery/gallery_list.html', {'images': [], 'first_type': "portrait"})
    
    first_type =  images.first().image_type if images.first() else "landscape"

    return Response({keys.Message: "Successfully Loaded",
                     "images" : GallerySerilaizers(images,many=True,context={'request':request}).data,
                     "first_type":first_type}, status=status.HTTP_200_OK)



def image_upload(request):
    """This view is used for image uploading"""
    return render(request, 'gallery/upload_form.html')
