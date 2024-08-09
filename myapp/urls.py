from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.user_login, name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/retrieve-photos/', views.retrieve_and_store_photos, name='retrieve_photos'),
]