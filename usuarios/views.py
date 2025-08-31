from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usuarios.models import Usuario
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
import random
from nfc.config_vars import ETHEREUM_RECEIVER, ETH_BOLIVIANO_RATE
from web3 import Web3
import requests
import json
from django.http import JsonResponse

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
class RecargaEthereumView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        monto_bs = float(request.data.get('monto_bs', 0))
        monto_eth = round(monto_bs * ETH_BOLIVIANO_RATE, 8)
        return Response({
            'receiver': ETHEREUM_RECEIVER,
            'monto_eth': monto_eth,
            'monto_bs': monto_bs,
        }, status=status.HTTP_200_OK)

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
        # Conexión a la red Ethereum (puedes usar Infura, Alchemy, etc.)
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/TU_INFURA_API_KEY'))
        try:
            tx = w3.eth.get_transaction(tx_hash)
            if tx['to'] and tx['to'].lower() == ETHEREUM_RECEIVER.lower() and w3.fromWei(tx['value'], 'ether') >= monto_eth:
                usuario.saldo = float(usuario.saldo) + monto_bs
                usuario.save()
                return Response({'success': True, 'msg': 'Recarga verificada y saldo actualizado.'}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'msg': 'Transacción no válida.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def recarga_coingate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        monto_bs = data.get('monto_bs')
        monto_usd = float(monto_bs) / 7  # Ajusta según tu tasa
        api_key = 'Vshnm7g46JbmmnsCd-8CyZad-h_xU5wKrteE4Sxx'  # Tu API Key real
        headers = {
            'Authorization': f'Token {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'order_id': 'recarga-' + str(monto_bs),
            'price_amount': monto_usd,
            'price_currency': 'USD',
            'receive_currency': 'BTC',
            'callback_url': 'https://TU_DOMINIO/api/usuarios/recarga/webhook/',
            'cancel_url': 'https://TU_DOMINIO/cancel/',
            'success_url': 'https://TU_DOMINIO/success/',
            'title': 'Recarga de saldo',
            'description': f'Recarga de saldo por {monto_bs} Bs'
        }
        response = requests.post(
            'https://api-sandbox.coingate.com/v2/orders',  # Usa sandbox para pruebas
            headers=headers,
            data=json.dumps(payload)
        )
        print(response.text)  # Para depuración
        result = response.json()
        payment_url = result.get('payment_url', '')
        return JsonResponse({'payment_url': payment_url})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def coingate_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        status = data.get('status')
        price_amount = data.get('price_amount')
        # Aquí puedes buscar el usuario y actualizar el saldo si el pago fue exitoso
        if status == 'paid':
            # Extrae el id_usuario si lo incluiste en order_id, por ejemplo: 'recarga-100.0-<id_usuario>'
            try:
                # Suponiendo que el order_id es 'recarga-<monto>-<id_usuario>'
                partes = order_id.split('-')
                if len(partes) >= 3:
                    id_usuario = partes[2]
                    from usuarios.models import Usuario
                    usuario = Usuario.objects.get(id_usuario=id_usuario)
                    usuario.saldo += float(price_amount)
                    usuario.save()
                    return JsonResponse({'success': True, 'msg': 'Saldo actualizado'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Create your views here.
