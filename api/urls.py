from django.urls import path , include
from .views import ToDo

# For Token generate
from rest_framework_simplejwt.views import TokenRefreshView , TokenVerifyView
# To get modify Token which contain usename also
from .views import MyTokenObtainPairView

#For Model viewset
from rest_framework import routers
from .views import signupView
obj = routers.DefaultRouter()

obj.register('todo-list',ToDo)


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/',TokenVerifyView.as_view(),name='token_verify'),
    path('signup/',signupView),
    path('',include(obj.urls))
]
