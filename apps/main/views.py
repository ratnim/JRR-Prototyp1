from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import ExpertSerializer, ProfileSerializer, ExpertRegistrationSerializer, \
    UserSerializer, StateSerializer
from .models import Profile, Expert, State


class ExpertListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer


class ExpertCreateView(generics.CreateAPIView):

    queryset = Expert.experts.all()
    serializer_class = ExpertRegistrationSerializer


class ExpertLoginView(views.APIView):

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


class ExpertLogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ExpertActivateView(generics.CreateAPIView):
    #TODO
    queryset = Expert.experts.all()
    serializer_class = ExpertRegistrationSerializer


class ExpertRetrieveView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser, )

    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer


class ExpertOwnView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer

    def get(self, request):

        user_data = UserSerializer(request.user)
        profile_data = ProfileSerializer(request.user.expert.profile)
        state_data = StateSerializer(request.user.expert.state)

        return Response({
                'user': user_data.data,
                'profile': profile_data.data,
                'state': state_data.data}
        )

    def patch(self, request):
        #TODO Doesnt work wrong lookup
        updated_profile = ProfileSerializer(request.user.expert.profile, data=request.data)
        updated_profile.save()

        updated_user = ProfileSerializer(request.user, data=request.data)
        updated_user.save()

        update_state = StateSerializer(request.user.expert.state, data=request.data)
        update_state.save()


class ProfileListView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAdminUser, )

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def patch(self, request):
        updated = ProfileSerializer(request.user.expert.profile, data=request.data)
        updated.save()


class StateRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAdminUser, )

    queryset = State.objects.all()
    serializer_class = StateSerializer

    def patch(self, request):
        updated = StateSerializer(request.user.expert.profile, data=request.data)
        updated.save()


class StateListView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )

    queryset = State.objects.all()
    serializer_class = StateSerializer

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
