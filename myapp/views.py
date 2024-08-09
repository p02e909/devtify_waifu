from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import Photo
import requests
from django.db import IntegrityError

def home(request):
    return HttpResponse("Hello, Django!")

def about(request):
    return render(request, 'myapp/about.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def retrieve_and_store_photos(request):
    # URL of the 3rd party API
    api_url = "https://api.waifu.pics/many/sfw/waifu"  # Replace with actual API URL
    
    photos_to_store = 300
    photos_stored = 0
    api_calls = 0
    max_api_calls = 15  # Limit API calls to prevent infinite loop
    
    # Get all existing photo URLs from the database
    exclude_list = list(Photo.objects.values_list('url', flat=True))
    
    while photos_stored < photos_to_store and api_calls < max_api_calls:
        try:
            # Prepare the request body with the exclude list
            request_body = {
                "exclude": exclude_list
            }
            
            # Make POST request to the 3rd party API with the exclude list
            response = requests.post(api_url, json=request_body)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            api_calls += 1
            
            data = response.json()
            photo_urls = data.get('files', [])
            
            for url in photo_urls:
                Photo.objects.create(url=url)
                photos_stored += 1
                exclude_list.append(url)  # Add the new URL to the exclude list
                
                if photos_stored >= photos_to_store:
                    break
            
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'message': f'{photos_stored} photos have been retrieved and stored.',
        'api_calls': api_calls
    }, status=status.HTTP_200_OK)
