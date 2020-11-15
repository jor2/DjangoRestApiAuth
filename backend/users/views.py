from django.http import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.permissions import AllowAny

from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from users.utils import get_token, revoke_token, refresh_token
from users.serializers import UserSerializer
# from DjangoAPI.logic.serializers import UserSerializer
# from backend.users.utils import get_token, revoke_token, refresh_token


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        token_response = get_token(request)
        return Response(token_response.data, status=token_response.status_code)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    token_response = get_token(request)
    return Response(token_response.data, status=token_response.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    token_response = revoke_token(request)
    return Response(token_response.data, status=token_response.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh(request):
    token_response = refresh_token(request)
    return Response(token_response.data, status=token_response.status_code)


class HelloWorldAPI(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
