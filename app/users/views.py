import random

from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, UpdateView, RedirectView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from app.users.controllers import UserController
from app.users.enums import Role
from app.users.schemas import UserCreateSchema, UserUpdateSchema, UserListSchema
from app.users.serializers import UserSerializer
from app.utils.constants import Timeouts, CacheKeys, SMS
from app.utils.helpers import mobile_number_validation_check, qdict_to_dict, \
    generate_random_username, build_cache_key
from app.utils.views import BaseViewSet

User = get_user_model()


class OtpLoginViewSet(viewsets.ViewSet):

    @extend_schema(
        description="Generates OTP for the provided mobile number and sends it via SMS.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample('Example JSON', value={"mobile_no": "1234567890"})
        ]
    )
    @action(methods=["POST"], detail=False)
    def generate(self, request):
        # this api does not need auth token
        # Generate otp, store it in cache, send sms using yellow.ai
        # request_body : {"mobile_no"}

        mobile_no = request.data.get('mobile_no', None)
        mobile_no_valid = mobile_number_validation_check(mobile_no)
        if mobile_no_valid is not None:
            return Response(data={"message": mobile_no_valid}, status=status.HTTP_400_BAD_REQUEST)

        mobile_no = str(mobile_no)

        static_otp_mobile_numbers = ['9344015965', '8971165979', '7013991532', '9959727836', '1414141414',
                                     '8858327030']  # can keep the numbers in .env file
        if mobile_no in static_otp_mobile_numbers:
            otp = "1111"
        else:
            otp = str(random.randint(1000, 9999))
        if settings.DEBUG:
            otp = "1111"
        cache.set("otp_" + mobile_no, otp, timeout=300)
        message = SMS.OTP_LOGIN.format(otp=otp)
        # send_otp(mobile_no=mobile_no, message=message)
        # send_otp.apply_async(
        #     kwargs={'mobile_no': mobile_no, 'message': message})
        return Response(data={"message": "otp generated"}, status=status.HTTP_200_OK)

    @extend_schema(
        description="Resends the OTP to the provided mobile number.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample('Example JSON', value={"mobile_no": "1234567890"})
        ]
    )
    @action(methods=["POST"], detail=False)
    def resend(self, request):
        # request_body : {"mobile_no"}
        mobile_no = request.data.get('mobile_no', None)
        mobile_no_valid = mobile_number_validation_check(mobile_no)
        if mobile_no_valid is not None:
            return Response(data={"message": mobile_no_valid}, status=status.HTTP_400_BAD_REQUEST)
        mobile_no = str(mobile_no)
        otp = cache.get("otp_" + mobile_no)
        if otp:
            cache.set("otp_" + mobile_no, otp, timeout=300)
            # message = GupshupSMSIntegration.OTP_SMS.replace("{otp}", str(otp))
            # send_sms_to_user.delay(mobile_no=mobile_no, message=message)
            return Response(data={"message": "resent otp"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "OTP not sent or it is expired"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Verifies the provided OTP and logs in the user.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample('Example JSON', value={"mobile_no": "1234567890", "otp": "1234"})
        ]
    )
    @action(methods=["POST"], detail=False)
    def verify(self, request):
        # this api does not need auth token
        # request_body : {"otp", "mobile_no"}

        mobile_no = request.data.get('mobile_no', None)
        mobile_no_valid = mobile_number_validation_check(mobile_no)
        if mobile_no_valid is not None:
            return Response(data={"message": mobile_no_valid}, status=status.HTTP_400_BAD_REQUEST)
        mobile_no = str(mobile_no)
        otp = str(request.data.get("otp"))
        otp_from_cache = cache.get("otp_" + mobile_no)
        if otp_from_cache is None:
            return Response(data={"message": "OTP not sent or it is expired"},
                            status=status.HTTP_400_BAD_REQUEST)
        if otp != otp_from_cache:
            return Response(data={"message": "Incorrect otp"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cache.delete("otp_" + mobile_no)
            user = User.objects.filter(mobile_no=mobile_no).select_related('auth_token').order_by('-id').first()
            if user is None:
                user = User.objects.create(username=generate_random_username())
                user.mobile_no = mobile_no
                token, created = Token.objects.get_or_create(user=user)
                user.auth_token = token
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print(request.user)
            user.last_login = timezone.now()
            user.save()
            auth_token = user.auth_token
            response = Response(data={
                "message": "successfully logged in",
                "user_id": user.id,
                "token": auth_token.key},
                status=status.HTTP_200_OK)
            return response

    @extend_schema(
        description="Logs out the authenticated user.",
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(methods=["POST"], detail=False)
    def logout(self, request):
        # Get the token associated with the user and delete it
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass  # No token found for user

        logout(request)
        response = Response(data={"message": "successfully logged out"},
                            status=status.HTTP_200_OK)
        return response


class UserViewSet(BaseViewSet):
    # permission_classes = (IsOrganizationUser,)
    controller = UserController()
    serializer = UserSerializer
    create_schema = UserCreateSchema
    update_schema = UserUpdateSchema
    list_schema = UserListSchema
    cache_key_retrieve = CacheKeys.USER_DETAILS_BY_PK
    cache_key_list = CacheKeys.USER_LIST

    @extend_schema(
        description="Create a new user",
        request=UserCreateSchema,
        examples=[
            OpenApiExample('User Creation Request JSON', value={
                "name": "John Doe",
                "mobile_no": "1234567890",
                "role": "admin"
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing user",
        request=UserUpdateSchema,
        examples=[
            OpenApiExample('User Update Request JSON', value={
                "name": "Jane Doe",
                "mobile_no": "0987654321",
                "role": "user"
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter users",
        parameters=[
            OpenApiParameter(name='name', location=OpenApiParameter.QUERY, required=False, type=str,
                             description='name'),
            OpenApiParameter(name='mobile_no', location=OpenApiParameter.QUERY, required=False, type=str,
                             description='mobile_no'),
            OpenApiParameter(name='role', location=OpenApiParameter.QUERY, required=False, type=str,
                             description='role'),
        ],
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific user by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='pk'),
        ],
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a user inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='pk'),
        ],
    )
    @action(methods=['POST'], detail=True)
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = "Information successfully updated"

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
