from django.views.generic import TemplateView
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from django.http import JsonResponse

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"
