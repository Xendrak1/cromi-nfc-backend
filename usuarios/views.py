from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usuarios.models import Usuario
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
import random
import json

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		nombre = request.data.get('nombre')
		correo = request.data.get('correo')
		telefono = request.data.get('telefono')
		# Generar PIN aleatorio de 4 dígitos
		pin = str(random.randint(1000, 9999))
		tipo_usuario = request.data.get('tipo_usuario', 'usuario')
		try:
			usuario = Usuario.objects.create_user(
				correo=correo,
				pin=pin,
				nombre=nombre,
				tipo_usuario=tipo_usuario,
			)
			return Response({'success': True, 'id_usuario': str(usuario.id_usuario), 'pin': pin}, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		correo = request.data.get('correo')
		pin = request.data.get('pin')
		try:
			usuario = Usuario.objects.get(correo=correo, pin=pin)
			return Response({'success': True, 'id_usuario': str(usuario.id_usuario)}, status=status.HTTP_200_OK)
		except Usuario.DoesNotExist:
			return Response({'success': False, 'error': 'Usuario o PIN incorrecto'}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class UsuarioDetailView(APIView):
	permission_classes = [AllowAny]

	def get(self, request, id_usuario):
		try:
			usuario = Usuario.objects.get(id_usuario=id_usuario)
			return Response({
				'nombre': usuario.nombre,
				'saldo': usuario.saldo,
				'correo': usuario.correo,
				'id_usuario': str(usuario.id_usuario),
			}, status=status.HTTP_200_OK)
		except Usuario.DoesNotExist:
			return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_exempt, name='dispatch')
class VerificarTransaccionView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		tx_hash = request.data.get('tx_hash')
		id_usuario = request.data.get('id_usuario')
		monto_eth = float(request.data.get('monto_eth', 0))
		monto_bs = float(request.data.get('monto_bs', 0))
		# Si el hash es 'simulado', omite la verificación y recarga directo
		try:
			usuario = Usuario.objects.get(id_usuario=id_usuario)
		except Usuario.DoesNotExist:
			return Response({'success': False, 'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
		if tx_hash == 'simulado':
			try:
				usuario.saldo = float(usuario.saldo) + monto_bs
				usuario.save()
				return Response({'success': True, 'msg': 'Recarga simulada y saldo actualizado.'}, status=status.HTTP_200_OK)
			except Exception as e:
				return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		# Sin Web3: devolver no implementado
		return Response({'success': False, 'error': 'Verificación on-chain deshabilitada'}, status=status.HTTP_501_NOT_IMPLEMENTED)


# Create your views here.
