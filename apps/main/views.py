import csv
import os

from django.http import HttpResponse
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

    """
    View all experts on the roster.

    * Requires authentication
    * Requires admin permission
    """
    # TODO: use admin authentication
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer


class ExpertCreateView(generics.CreateAPIView):

    """
    Register a new expert (and user account)
    """
    queryset = Expert.experts.all()
    serializer_class = ExpertRegistrationSerializer


class ExpertLoginView(views.APIView):

    """
    Sign in an expert
    """

    def post(self, request, format=None):

        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                expert = Expert.experts.get(user__pk=user.pk)
                serializedExpert = ExpertSerializer(expert)
                token, created = Token.objects.get_or_create(user=user)

                responseData = serializedExpert.data
                responseData['token'] = token.key
                return Response(responseData)
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


class DownloadCsvView(views.APIView):

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="download.csv"'
        fieldnames = ['name', 'surname', 'global_south', 'region', 'country']
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()

        experts = Expert.experts.all()
        for expert in experts:
            surname = expert.profile.surname
            name = expert.profile.name
            global_south = False
            country = expert.profile.contact_info.address.country
            country_to_region = self.read_in_country_log()
            region = country_to_region[country]

            my_dict = {'name': name, 'surname': surname, 'global_south': global_south,
                       'region': region, 'country': country}

            writer.writerow(my_dict)

            # writer.writerow([name, surname, global_south, regions])

        return response

    def read_in_country_log(self):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'country_log.csv')
        country_to_abbr = {}

        with open(file_path, 'rt') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                country_to_abbr[row[0]] = row[2]

        return country_to_abbr


class ExpertActivateView(generics.CreateAPIView):
    # TODO
    queryset = Expert.experts.all()
    serializer_class = ExpertRegistrationSerializer


class ExpertRetrieveView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser, )

    queryset = Expert.experts.all()
    serializer_class = ExpertSerializer


class ExpertOwnView(views.APIView):
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
        # TODO Doesnt work, wrong lookup_field
        updated_profile = ProfileSerializer(request.user.expert.profile,
                                            data=request.data.get('profile'))
        updated_user = ProfileSerializer(request.user, data=request.data)
        updated_state = StateSerializer(request.user.expert.state,
                                        data=request.data)

        updated_profile.is_valid(raise_exception=True)
        updated_state.is_valid(raise_exception=True)
        updated_user.is_valid(raise_exception=True)

        updated_user.save()
        updated_state.save()
        updated_profile.save()
        response = ExpertSerializer(request.user.expert)
        return Response({
           'expert': response.data
        }, status=status.HTTP_200_OK)


class ProfileListView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # permission_classes = (permissions.IsAdminUser, )

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def patch(self, request, pk):
        # updated_profile = ProfileSerializer(
        #    request.user.expert.profile, data=request.data.get('profile'))
        # updated_user = ProfileSerializer(request.user, data=request.data)
        # updated_state = StateSerializer(
        #    request.user.expert.state, data=request.data)
        profile = Profile.objects.get(pk=pk)
        updated = ProfileSerializer(profile, data=request.data)
        updated.update(profile, request.data)
        updated.is_valid(raise_exception=True)
        return Response({
           'expert': updated.data
        }, status=status.HTTP_200_OK)


class StateRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAdminUser, )

    queryset = State.objects.all()
    serializer_class = StateSerializer

    def patch(self, request):
        updated = StateSerializer(request.user.expert.profile,
                                  data=request.data)
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
