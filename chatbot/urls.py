from django.urls import path
from . import views

urlpatterns = [

    path('', views.home),

    path('chat/', views.chat),

    path('analyze-image/', views.analyze_image),

    path('analyze-pdf/', views.analyze_pdf),
]