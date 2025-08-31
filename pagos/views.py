from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils import timezone
from django.db import transaction

from pagos.models import Pago
from usuarios.models import Usuario
from micros.models import Micro


class PagosListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_id = request.GET.get('id_usuario')
        qs = Pago.objects.all()
        if user_id:
            qs = qs.filter(id_usuario__id_usuario=user_id)
        pagos = qs.values('id_pago', 'id_usuario', 'id_micro', 'monto', 'tarifa', 'fecha_hora', 'estado')
        return Response(list(pagos), status=status.HTTP_200_OK)


class CrearPagoView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        try:
            user_id = request.data.get('id_usuario')
            micro_id = request.data.get('id_micro')
            monto = float(request.data.get('monto'))
            tarifa = request.data.get('tarifa', 'General')

            usuario = Usuario.objects.select_for_update().get(id_usuario=user_id)
            micro = Micro.objects.get(id_micro=micro_id)

            if float(usuario.saldo) < monto:
                return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

            usuario.saldo = float(usuario.saldo) - monto
            usuario.save()

            pago = Pago.objects.create(
                id_usuario=usuario,
                id_micro=micro,
                monto=monto,
                tarifa=tarifa,
                fecha_hora=timezone.now(),
                estado='COMPLETADO',
            )
            return Response({'id_pago': str(pago.id_pago), 'saldo_restante': float(usuario.saldo)}, status=status.HTTP_201_CREATED)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Micro.DoesNotExist:
            return Response({'error': 'Micro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
