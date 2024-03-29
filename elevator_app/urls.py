"""
URL configuration for elevator_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.ujrls'))
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from elevator_app import views

urlpatterns = [
    path("elevators", views.ListCreateGetElevator.as_view(), name="Elevators"),
    path(
        "elevatorsRequest/<int:pk>",
        views.GetAllElevatorRequest.as_view(),
        name="Elevators Requsts",
    ),
    path("elevators/<int:pk>", views.GetUpdateElevator.as_view(), name="Elevator"),
    path(
        "request_elevators",
        views.GetCreateElevatorDoor.as_view(),
        name="Request Elevator",
    ),
    path(
        "request_elevators/<int:pk>",
        views.GetDetailElevetorRequest.as_view(),
        name="Get Detail Elevator",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
