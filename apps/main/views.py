from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import ExpertSerializer, ProfileSerializer, ExpertRegistrationSerializer, \
    UserSerializer, StatusSerializer
from .models import Profile, Expert


class ExpertListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer


class ExpertCreateView(generics.CreateAPIView):
    queryset = Expert.experts.all()
    serializer_class = ExpertRegistrationSerializer


class ExpertLoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                serialized = UserSerializer(user, context={'request': request})
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'user': serialized.data,
                    'token': token.key
                })
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This authentication has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)


class ExpertLogoutView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ExpertActivateView(generics.CreateAPIView):
    queryset = Expert.experts.all()
    serializer_class = ExpertRegistrationSerializer


class ExpertRetrieveView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer


class ExpertOwnView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer

    def get(self, request):

        user_data = UserSerializer(request.user)
        profile_data = ProfileSerializer(request.user.expert.profile)
        status_data = StatusSerializer(request.user.expert.status)

        return Response({
                'user': user_data.data,
                'profile': profile_data.data,
                'status': status_data.data
            }
        )

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
