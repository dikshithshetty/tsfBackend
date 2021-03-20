from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import School, Student, Observation, Subscription, Transfer, UserProfile
from .serializers import SchoolSerializer, StudentSerializer, ObservationSerializer, SubscriptionSerializer, TransferSerializer, UserProfileSerializer

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_201_CREATED
)


# Create your views here.


# User model 

# View all users and add new user
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST': 
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# View a given user, modify his information and delete 
@api_view(['GET', 'PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_details(request, id):
    try:
        user = UserProfile.objects.get(id = id)
    except UserProfile.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)




# School Model

# View all schools
@api_view(['GET'])
def school_list(request):
    if request.method == 'GET':
        schools = School.objects.all()
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)

# View details for a given school
@api_view(['GET'])
def school_detail(request, id):
        try:
            school = School.objects.get(id= id)
        except School.DoesNotExist:
            return HttpResponse(status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            serializer = SchoolSerializer(school)
            return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def school_change_mode(request, id):
    try:
        school = School.objects.get(id=id)
    except School.DoesNotExist:
        return HttpResponse(status.HTTP_400_BAD_REQUEST)

    if request.user.function.upper() == 'DIRECTOR' or request.user.function.upper() == 'ADMIN':
        if(school.mode==False):
            school.mode = True
        else:
            school.mode = False
        school.save(update_fields=['mode'])
        return HttpResponse(status.HTTP_202_ACCEPTED)
    else:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED)


# Student Model

# View students for a given school and add a new student for a given school 
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def student_list(request, schoolid):
    if request.method == 'GET':
        students = Student.objects.filter(school_id=schoolid)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST': 
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
# View a given student, modify his information and delete 
@api_view(['GET', 'PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def student_details(request, id):
    try:
        student = Student.objects.get(id = id)
    except Student.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        student.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Observation Model


# View all observations for a given student and create new observation
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def observation_list(request, id_student):
    if request.method == 'GET':
        observations = Observation.objects.filter(id_student = id_student)
        serializer = ObservationSerializer(observations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ObservationSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View only one observation for a given student (by selecting observation id), modify and delete that observation 
@api_view(['GET', 'PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def observation_detail(request, id_observation):
    try:
        observation = Observation.objects.get(id = id_observation)
    except Observation.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    
    mode = School.objects.get(id=request.user.school).mode
    function = request.user.function.upper()

    if function == 'USER' and mode == 1:
        return HttpResponse(status.HTTP_401_UNAUTHORIZED)
    
    else:

        if request.method == 'GET':
            serializer = ObservationSerializer(observation)
            return Response(serializer.data)
        
        if request.method == 'PUT':
            serializer = ObservationSerializer(observation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            observation.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)



# Subscription Model

# Get Subscription details for a given school id
@api_view(['GET'])
def subscription_detail(request, school_id):
    try:
        subscription = Subscription.objects.get(id_school=school_id)
    except Subscription.DoesNotExist:
        return HttpResponse(status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)


# Transfert Model

# View all transfers and create new ones
@api_view(['GET','POST'])
def transfer_list(request):
    if request.method == 'GET':
        transfers = Transfer.objects.all()
        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TransferSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Checks email and password and returns an auth token
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    school_id = user.school
    return Response({'token': token.key, 'school_id': school_id}, status=HTTP_200_OK)


# Logout by deleting token object assigned to the current user
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"success": "Successfully logged out."}, status=HTTP_200_OK)
