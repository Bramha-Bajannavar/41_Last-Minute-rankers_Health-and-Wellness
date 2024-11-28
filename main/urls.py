# urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='patient_login'),
    path('hospital-login/', views.hospital_login, name='hospital_login'),
    path('logout/', views.logout_view, name='logout'),
    path('chatbot/', views.chatbot_api, name='chatbot_api'),
    path('home/', views.home, name='home'),
    path('hospital-home/', views.hospital_home, name='hospital_home'),
    path('result/<str:result>/', views.result_view, name='result'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('process-parameters/', views.process_parameters, name='process_parameters'),

]