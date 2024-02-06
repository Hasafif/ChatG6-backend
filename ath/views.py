from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from ath.serializers import check_password_validity
from django.views.decorators.csrf import csrf_exempt
from bd.settings import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import settings
def login_page(request):
  message = request.GET.get('message',None)
  if not message is None:
    return render(request,'log_in.html',{'message':message})
  else:
    return render(request,'log_in.html')

@login_required
def home(request):
  message = request.GET.get('message',None)
  if not message is None:
    return render(request,'base.html',{'message':message})
  else:
    return render(request,'base.html')

# Class-based view for user login
class LoginProc(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            usr = request.data['usr']
            pwd = request.data['pwd']
            user = authenticate(username=usr, password=pwd)

            if user is not None:
                login(request, user)
                return Response({"message": "Logged in successfully", "next": "home"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Username or password are incorrect, Try again or Signup!"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Class-based view for user registration
class SignUpProcView(APIView):
  
  @csrf_exempt
  def post(self,request):
    try:
        usr = request.data['usr']
        email = request.data['email']
        pwd = request.data['pwd']
        c_pwd = request.data['pwdC']
        if pwd == c_pwd :
               if User.objects.filter(email=email).exists():
                   return Response({"message":"Email already taken, please enter another one"})
               elif User.objects.filter(username=usr).exists():
                           return Response({'message':"Username is already taken, please enter another one"})
               elif check_password_validity(pwd) != 'Valid' :
                           val = check_password_validity(pwd)
                           val = val[2:len(val)-2]
                           errs = val.split("','")
                           errs = " ".join(errs)
                           return Response({'errors':errs})
               elif not usr.isalnum():
                           return Response({'message':"Username must be Alpha-numeric"})
               else:
                  user = User.objects.create_user(username=usr,email=email,password=pwd)
                  user.save()
                  #send_email(usr,email)
                  return Response({'message':"login,Account created successfully! please log in now."})
        else:
               return Response({'message':'signup,Passwords did not match!'})
    except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def signup_page(request):
  message = request.GET.get('message',None)
  if not message is None:
    return render(request,'sign_up.html',{'message':message})
  else:
    return render(request,'sign_up.html')


def signup_redirect(request):
  return redirect('signup')

def login_redirect(request):
  return redirect('login')
#log_out process
def logout_proc(request):
  logout(request)
  return Response({'message':'login,You logged out ,log in again please.'})

def message(viewName:str,msg:str) -> HttpResponsePermanentRedirect:
  return redirect(reverse(viewName) + '?message=' + msg)
#under Test
@csrf_exempt
def send_email(request):
  user = request.POST['usr']
  email = request.POST['em']
  subject = "Welcome to Our website!"
  message = str(f"Hi user:{user}, \n Thanks to login to our website! \n")
  from_email = EMAIL_HOST_USER
  to_list = [email]
  send_mail(subject,message,from_email,to_list,fail_silently=True)


