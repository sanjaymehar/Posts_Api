from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Image, Comment
from .serializers import UserSerializer,ImageSerializer, CommentSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(serializer.validated_data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class ImageView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            image = Image.objects.filter(pk=pk).first()
            if not image:
                return Response({'message': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ImageSerializer(image)
        else:
            images = Image.objects.all()
            serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageLikeView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, image_id):
        image = Image.objects.filter(pk=image_id).first()
        if not image:
            return Response({'message': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)
        if image.likes.filter(pk=request.user.pk).exists():
            image.likes.remove(request.user)
        else:
            image.likes.add(request.user)
        return Response({'message': 'Success.'}, status=status.HTTP_200_OK)


class CommentCreateView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            image = Image.objects.filter(pk=request.data['image']).first()
            if not image:
                return Response({'message': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer.save(user=request.user, image=image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
