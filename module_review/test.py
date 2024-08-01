from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone
from collections import Counter
from operator import itemgetter
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from rest_framework import status
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from account.models import User
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, HttpResponseForbidden
from .models import Module, Program, ProgramReview, ProgramReview, AcademicYear
from .serializers import ProgramSerializer, ProgramReviewSerializer, ProgramSerializer, ProgramReviewSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Q
















