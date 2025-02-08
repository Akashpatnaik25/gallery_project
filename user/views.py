from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction


from .models import User, UserProfile
from helper import keys ,functions



@csrf_exempt
@api_view(['POST'])
def login_api(request):
    username = request.data.get("username", "").strip()
    password = request.data.get("password", "").strip()
    
    if not username or not password:
        return Response({keys.Message: "Please provide both username and password."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({keys.Message: "User does not exist."},
                        status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
        return Response({keys.Message: "Incorrect password."},
                        status=status.HTTP_401_UNAUTHORIZED)
    
    tokens = functions.get_tokens_for_user(user)
    return Response({
        keys.Message: "Login successful.",
        "access_token": tokens['access'],
        "refresh_token": tokens['refresh']
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup_api(request):
    username = request.data.get('username', "").strip()
    fullname = request.data.get('fullname', "").strip()
    password = request.data.get('password', "").strip()
    age = request.data.get('age',0)
    gender = request.data.get('gender', "").strip().lower()
    
    if not username or not fullname or not password or not age or not gender:
        return Response({keys.Message: "All fields are required."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({keys.Message: "Username already exists. Please choose another username."},
                        status=status.HTTP_409_CONFLICT)
    
    try:
        age = int(age)
        if age <= 0:
            raise ValueError("Age must be a positive number.")
    except ValueError:
        return Response({keys.Message: "Invalid age provided."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    if gender not in ["male", "female", "other"]:
        return Response({keys.Message: "Gender must be 'male', 'female', or 'other'."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        
        try:
            UserProfile.objects.create(user=user, full_name=fullname, age=age, gender=gender)
        except Exception as e:
            return Response({keys.Message: f"Error creating user profile: {e}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        tokens = functions.get_tokens_for_user(user)
        return Response({
            keys.Message: "Signup successful.",
            "access_token": tokens['access'],
            "refresh_token": tokens['refresh']
        }, status=status.HTTP_201_CREATED)


def login_page(request):
    """This view is to access the login page"""
    return render(request, 'user/login.html')

def signup_page(request):
    """This view is to access the signup page"""
    return render(request, 'user/signup.html')
