from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from .serializers import RegisterSerializer, LoginSerializer, UsuarioSerializer
from apps.feed.models import Atividade


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UsuarioSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UsuarioSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UsuarioDetailView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class SeguirView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            alvo = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if alvo == request.user:
            return Response({'error': 'Você não pode seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.seguindo.filter(pk=alvo.pk).exists():
            request.user.seguindo.remove(alvo)
            return Response({'seguindo': False})
        else:
            request.user.seguindo.add(alvo)
            Atividade.objects.create(usuario=request.user, tipo='seguiu', usuario_alvo=alvo)
            return Response({'seguindo': True})
