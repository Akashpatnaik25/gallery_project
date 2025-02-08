import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from user.models import UserProfile
from helper import keys

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    """Fixture to create a test user"""
    user = User.objects.create_user(username="testuser", password="testpass")
    UserProfile.objects.create(user=user, full_name="Test User", age=25, gender="male")
    return user

@pytest.mark.django_db
def test_login_api_missing_fields(api_client):
    """Test login with missing fields"""
    response = api_client.post("/login/", {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[keys.Message] == "Please provide both username and password."

@pytest.mark.django_db
def test_login_api_user_not_found(api_client):
    """Test login with a non-existent user"""
    response = api_client.post("/login/", {"username": "nonexistent", "password": "testpass"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()[keys.Message] == "User does not exist."

@pytest.mark.django_db
def test_login_api_invalid_password(api_client, create_user):
    """Test login with incorrect password"""
    response = api_client.post("/login/", {"username": "testuser", "password": "wrongpass"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()[keys.Message] == "Incorrect password."

@pytest.mark.django_db
def test_login_api_success(api_client, create_user, mocker):
    """Test successful login"""
    mock_tokens = {"access": "mock_access_token", "refresh": "mock_refresh_token"}
    mocker.patch("helper.functions.get_tokens_for_user", return_value=mock_tokens)

    response = api_client.post("/login/", {"username": "testuser", "password": "testpass"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[keys.Message] == "Login successful."
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.django_db
def test_signup_api_missing_fields(api_client):
    """Test signup with missing fields"""
    response = api_client.post("/signup/", {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[keys.Message] == "All fields are required."

@pytest.mark.django_db
def test_signup_api_invalid_age(api_client):
    """Test signup with invalid age"""
    data = {"username": "newuser", "fullname": "New User", "password": "newpass", "age": "-5", "gender": "male"}
    response = api_client.post("/signup/", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[keys.Message] == "Invalid age provided."

@pytest.mark.django_db
def test_signup_api_invalid_gender(api_client):
    """Test signup with an invalid gender"""
    data = {"username": "newuser", "fullname": "New User", "password": "newpass", "age": "25", "gender": "invalid"}
    response = api_client.post("/signup/", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[keys.Message] == "Gender must be 'male', 'female', or 'other'."

@pytest.mark.django_db
def test_signup_api_existing_username(api_client, create_user):
    """Test signup with an existing username"""
    data = {"username": "testuser", "fullname": "Test User", "password": "newpass", "age": "25", "gender": "male"}
    response = api_client.post("/signup/", data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()[keys.Message] == "Username already exists. Please choose another username."

@pytest.mark.django_db
def test_signup_api_success(api_client, mocker):
    """Test successful signup"""
    mock_tokens = {"access": "mock_access_token", "refresh": "mock_refresh_token"}
    mocker.patch("helper.functions.get_tokens_for_user", return_value=mock_tokens)

    data = {"username": "newuser", "fullname": "New User", "password": "newpass", "age": "25", "gender": "male"}
    response = api_client.post("/signup/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()[keys.Message] == "Signup successful."
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.django_db
def test_login_page_view(api_client):
    """Test login page rendering"""
    response = api_client.get("/login-page/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_signup_page_view(api_client):
    """Test signup page rendering"""
    response = api_client.get("/signup-page/")
    assert response.status_code == 200
