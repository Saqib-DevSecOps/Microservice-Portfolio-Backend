from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return Response({'message': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = token.split(' ')[1]  # Assumes token is in 'Bearer <token>' format
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            user_info = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            return Response({'message': 'Token is valid', 'user_info': user_info}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
