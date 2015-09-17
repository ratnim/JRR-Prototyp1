from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions

from .serializers import ExpertSerializer, ProfileSerializer, ExpertRegistrationSerializer, \
    SuperuserRegistrationSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Profile, Expert

#authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash

from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response





class ExpertListView(generics.ListAPIView):
    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer


class ExpertCreateView(generics.CreateAPIView):
    queryset = Expert.experts.all()
    serializer_class = ExpertRegistrationSerializer


class ExpertLoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                serialized = UserSerializer(user, context={'request': request})
                return Response({
                    'account': serialized.data
                })
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This authentication has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if request.user.is_active:
                serialized = UserSerializer(request.user, context={'request': request})
                return Response({
                    'account': serialized.data
                })
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class ExpertLogoutView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ExpertActivateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ExpertRegistrationSerializer


class ExpertRetrieveView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    queryset = User.objects.all()
    serializer_class = ExpertSerializer


class SuperuserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SuperuserRegistrationSerializer


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileCreateView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class WebMasterView(TemplateView):
    template_name = 'google4c82de08f55a8973.html'
    #
    # def dispatch(self, *args, **kwargs):
    #     return super(WebMasterView, self).dispatch(*args, **kwargs)
