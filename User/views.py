from django.utils import timezone
from http import HTTPStatus
from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import Account
from .serializers import AccountSerializer
from rest_framework import  generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django import http
import requests
from django.db import transaction
from django.db.models import Q

from User import models
@csrf_exempt
def UpdateUser(request,user_id):
    if request.method == 'PATCH':
        try:
            user = get_object_or_404(Account, id = user_id)
            data = json.loads(request.body)
            new_username = data.get('username')
            new_email = data.get('email')
            new_password = data.get('password')
            new_gender = data.get('gender')
            new_birthday = data.get('birthday')
            new_role = data.get('role')
            new_type = data.get('type')
            new_department = data.get('department')
            new_classroom = data.get('classroom')
            new_avt_url = data.get('avt_url')
            new_background_url = data.get('background_url')

            # save
            if new_username:
                user.username = new_username
            if new_email:
                user.email = new_email
            if new_password:
                user.password = new_password
            if new_gender:
                user.gender = new_gender
            if new_birthday:
                user.birthday = new_birthday
            if new_role:
                user.role = new_role
            if new_type:
                user.type = new_type
            if new_department:
                user.department = new_department
            if new_classroom:
                user.classroom = new_classroom
            if new_avt_url:
                user.avt_url = new_avt_url
            if new_background_url:
                user.background_url = new_background_url            
                
            user.createdAt = timezone.now()
            user.updateAt = timezone.now()

            user.save()
            response_data = {
                    'status': HTTPStatus.OK,
                    'message': 'Update successfully',
                    'serviceName': 'USERSERVICE',
                    'body': {
                        'data': {
                            'message': 'User updated successfully',
                            'id': user.id,
                            'name': user.username,
                            'email': user.email,
                            'password':user.password,
                            'gender': user.gender,
                            'birthday': user.birthday,
                            'role': user.role,
                            'type':user.type,
                            'department':user.department,
                            'classroom':user.classroom,
                            'avt_url':user.avt_url,
                            'background_url': user.background_url,
                            'createAt': user.createdAt,
                            'updateAt': user.updateAt
                        }
                    }
            }

        except Exception as e:
            # Xử lý lỗi nếu có
            response_data = {
                'status': HTTPStatus.INTERNAL_SERVER_ERROR,
                'message': 'Internal Server Error',
                'serviceName': 'UsersService',
                'body': {
                    'data': False,
                    'error': str(e)
                }
            }
        return JsonResponse(response_data, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=HTTPStatus.BAD_REQUEST)
@csrf_exempt   
def Delete_user(request, user_id):
    try:
        user = get_object_or_404(Account, id = user_id)
        if request.method == 'DELETE':
            user.delete()
            response_data = {
                'status': HTTPStatus.OK,
                'mess': 'Deleted successfully',
                'body':{
                    'data' :{}
                }
            }
        else:
            response_data = {
                'status': HTTPStatus.INTERNAL_SERVER_ERROR,
                'mess': 'internal server error',
                'body':{
                    'error':'internal server error'
                }
            }
    except Account.DoesNotExist:
        response_data = {
            'status': HTTPStatus.NOT_FOUND,
            'mess': 'User not found',
            'body':{
                'error':'not found'
            }
        }

    return JsonResponse(response_data, status=response_data['status'])


@csrf_exempt
def SearchUser(request):
    try:
        keyword = request.GET.get('keyword','')
        user = Account.objects.filter(Q(id__icontains=keyword) | Q(email__icontains=keyword)).first()
        if user is not None:
            response_data = {
                        'status': HTTPStatus.OK,
                        'mess': 'Success',
                        'serviceName': 'USERSERVICE',
                        'body': {
                            'data': {
                                'id': user.id,
                                'name': user.username,
                                'email': user.email,
                                'password':user.password,
                                'gender': user.gender,
                                'birthday': user.birthday,
                                'role': user.role,
                                'type':user.type,
                                'department':user.department,
                                'classroom':user.classroom,
                                'avt_url':user.avt_url,
                                'background_url': user.background_url,
                                'createAt': user.createdAt,
                                'updateAt' : user.updateAt
                            },
                        }
                    }
        else:
            response_data = {
                'status': HTTPStatus.NOT_FOUND,
                'mess': 'User not found',
                'body':{
                    'error':'not found'
                }
            }
        return JsonResponse(response_data, status=HTTPStatus.OK)
    except:

        response_data = {
            'status': HTTPStatus.INTERNAL_SERVER_ERROR,
            'mess': 'internal server error',
            'serviceName': 'USERSERVICE',
            'body': {
                'error':'internal server error'
            }
        }
    return JsonResponse(response_data, status=response_data['status'])

@csrf_exempt
def getUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            gender = data.get('gender')
            birthday = data.get('birthday')
            role = data.get('role')
            type = data.get('type')
            department = data.get('department')
            classroom = data.get('classroom')
            avt_url = data.get('avt_url')
            background_url = data.get('background_url')
            
            # Kiểm tra nếu có dữ liệu bị thiếu
            if None in [username, password, email, gender, birthday, role,type,department,classroom,avt_url,background_url]:
                response_data = {
                    'status': HTTPStatus.BAD_REQUEST,
                    'mess': 'bad request',
                    'serviceName': 'USERSERVICE',
                    'body': {
                        'data': False,
                        'error': 'bad request'
                    }
                }
                return JsonResponse(response_data, status=HTTPStatus.BAD_REQUEST)

            user = Account( username=username, password=password, email=email, gender=gender, birthday=birthday, role=role)
            user.save()

            response_data = {
                'status': HTTPStatus.CREATED,
                'mess': 'register successfully',
                'serviceName': 'USERSERVICE',
                'body': {
                    'data': {
                        'id': user.id,
                        'name': user.username,
                        'email': user.email,
                        'gender': user.gender,
                        'birthday': user.birthday,
                        'role': user.role,
                        'type':user.type,
                        'department':user.department,
                        'classroom':user.classroom,
                        'avt_url':user.avt_url,
                        'background_url': user.background_url,
                        'createAt': user.createdAt,
                        'updateAt': user.updateAt
                    },
                    'error': 'NULL'
                }
            }

            return JsonResponse(response_data, status=HTTPStatus.CREATED)
        
        except Exception as e:
            # Xử lý lỗi nếu có
            response_data = {
                'status': HTTPStatus.INTERNAL_SERVER_ERROR,
                'mess': 'Internal Server Error',
                'serviceName': 'UsersService',
                'body': {
                    'data': False,
                    'error': str(e)
                }
            }
            return JsonResponse(response_data, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=HTTPStatus.BAD_REQUEST)
    
    


    


