from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from . import keys

def validate_image(image):
    allowed_extensions = ['jpg', 'jpeg', 'png']
    validator = FileExtensionValidator(allowed_extensions)
    try:
        validator(image)
        width, height = get_image_dimensions(image)
        if width > 5000 or height > 5000:
            raise ValidationError("Image dimensions should not exceed 5000x5000 pixels.")
    except ValidationError as e:
        return str(e)
    return None



def get_tokens_for_user(user):
    """Generate access and refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



def get_user_from_token(request):
    """Extract and validate JWT token to get the user"""
    auth_header = request.META.get("HTTP_AUTHORIZATION", None)

    if not auth_header:
        return None, JsonResponse({keys.Error: "Authorization header missing"}, status=401)

    try:
        # Expecting header in "Bearer <token>" format
        token_type, access_token = auth_header.split(" ")
        if token_type.lower() != "bearer":
            return None, JsonResponse({keys.Error: "Invalid token format"}, status=401)

        # Decode the token
        decoded_token = AccessToken(access_token)
        
        # Get user from token
        user = User.objects.get(id=decoded_token["user_id"])
        return user, None

    except Exception as e:
        return None, JsonResponse({keys.Error: f"Invalid or expired token: {str(e)}"}, status=401)
