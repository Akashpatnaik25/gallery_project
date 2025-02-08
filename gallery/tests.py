from django.test import TestCase

# Create your tests here.
import pytest
import io
import qrcode
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from user.models import UserProfile
from gallery.models import UploadedImage
from helper import keys

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    """Fixture to create a test user"""
    user = User.objects.create_user(username="testuser", password="testpass")
    user_profile = UserProfile.objects.create(user=user)
    return user, user_profile

@pytest.fixture
def auth_client(api_client, create_user):
    """Fixture to authenticate a test user"""
    user, _ = create_user
    api_client.force_authenticate(user=user)
    return api_client, user

@pytest.fixture
def sample_image():
    """Fixture to generate a simple image"""
    return SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

@pytest.fixture
def sample_qr():
    """Fixture to generate a sample QR code"""
    buffer = io.BytesIO()
    qr = qrcode.make("https://example.com/test_image.jpg")
    qr.save(buffer, format="PNG")
    return SimpleUploadedFile("test_qr.png", buffer.getvalue(), content_type="image/png")

@pytest.mark.django_db
def test_upload_image_api_missing_fields(auth_client):
    """Test image upload API with missing fields"""
    client, _ = auth_client
    response = client.post("/upload-image/", {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert keys.Error in response.json()

@pytest.mark.django_db
def test_upload_image_api_invalid_image(auth_client):
    """Test image upload API with an invalid image format"""
    client, _ = auth_client
    invalid_file = SimpleUploadedFile("test.txt", b"invalid content", content_type="text/plain")
    data = {"image": invalid_file, keys.IMAGE_TYPE: "portrait"}

    response = client.post("/upload-image/", data, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert keys.Error in response.json()

@pytest.mark.django_db
def test_upload_image_api_success(auth_client, sample_image):
    """Test successful image upload"""
    client, user = auth_client
    data = {"image": sample_image, keys.IMAGE_TYPE: "portrait"}

    response = client.post("/upload-image/", data, format='multipart')
    assert response.status_code == status.HTTP_201_CREATED
    assert keys.Message in response.json()

@pytest.mark.django_db
def test_image_gallery_api_no_auth(api_client):
    """Test image gallery API without authentication"""
    response = api_client.get("/image-gallery/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # Unauthorized due to missing token

@pytest.mark.django_db
def test_image_gallery_api_no_images(auth_client):
    """Test image gallery API when user has no images"""
    client, _ = auth_client
    response = client.get("/image-gallery/")
    assert response.status_code == status.HTTP_200_OK
    assert "images" in response.json()
    assert response.json()["images"] == []

@pytest.mark.django_db
def test_image_gallery_api_with_images(auth_client, sample_image):
    """Test image gallery API when user has images"""
    client, user = auth_client
    user_profile = UserProfile.objects.get(user=user)
    
    UploadedImage.objects.create(user=user_profile, image=sample_image, image_type="portrait")

    response = client.get("/image-gallery/")
    assert response.status_code == status.HTTP_200_OK
    assert "images" in response.json()
    assert len(response.json()["images"]) == 1

@pytest.mark.django_db
def test_gallery_view(api_client):
    """Test gallery view rendering"""
    response = api_client.get("/gallery/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_image_upload_view(api_client):
    """Test image upload form rendering"""
    response = api_client.get("/image-upload/")
    assert response.status_code == 200
