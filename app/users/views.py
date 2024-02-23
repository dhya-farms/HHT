from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.decorators import action

from app.users.controllers import UserController
from app.users.schemas import UserCreateSchema, UserListSchema, UserUpdateSchema
from app.users.serializers import UserSerializer
from app.utils.constants import CacheKeys
from app.utils.views import BaseViewSet

User = get_user_model()


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
    success_message = _("Information successfully updated")

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
