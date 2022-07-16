from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from apps.users.serializers import RegisterSerializer


@api_view(('POST', ))
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)

        pay_load = {}
        pay_load['value'] = {}
        pay_load['errors'] = []
        pay_load['success'] = True

        if serializer.is_valid():

            user = serializer.save()

            token, _ = Token.objects.get_or_create(user=user)
            pay_load['value'].update(serializer.data)
            pay_load['value'].update({'token': token.key})

            return Response(pay_load, status=status.HTTP_201_CREATED)
        else:
            pay_load['value'] = None
            pay_load['errors'].append(serializer.errors)
            pay_load['success'] = False
            return Response(pay_load, status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST', ))
@permission_classes((IsAuthenticated, ))
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response()
