import io
import requests
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from ToDo import models as tm
from rest_framework.permissions import IsAuthenticated
from .serialize import ModelSerializer
from rest_framework.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User 

# Modify JWTToken data
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username # we add username in token
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
class ToDo(ModelViewSet):
    
    queryset = tm.TODO.objects.all().order_by('status', 'priority')
    permission_classes = [IsAuthenticated,]
    serializer_class = ModelSerializer
    
    def get_queryset(self):
        user = self.request.user # for find which use send request for data
        print(user)
        print(type(user))
        if user.is_authenticated:
            return tm.TODO.objects.filter(user = user)
        else:
            raise PermissionDenied() 

# for singup

def get_parsed_data(data):
    json_data = data
    stream = io.BytesIO(json_data)
    parsed_data = JSONParser().parse(stream)
    return parsed_data

# to get token
def createToken(username,password):
    data = { "username" : username,"password" : password}
    res = requests.post("https://sanket-todolist-backend.herokuapp.com/api/token/",data=data)
    return res.json()

@csrf_exempt
def signupView(request):

    if request.method == 'POST':
        user = get_parsed_data(request.body)

        # Check User already exists or not
        exist_user = None
        try:
            exist_user = User.objects.get(username=user['username'])
        except User.DoesNotExist:
            exist_user = None
        if exist_user is not None:
            return JsonResponse({'msg': "Username Already Exists !"}, status=403)
        
        if user["password1"] != user["password2"]:
            return JsonResponse({'msg':"Password Doesn't Match"},status=403)

        # Store in database
        userObj = User.objects.create_user(username = user['username'],password = user['password1'],email = user['email'])
        userObj.save()
        res = createToken(user['username'],user['password1'])
        print(res)            
        return JsonResponse(res)
    
    return JsonResponse("")
