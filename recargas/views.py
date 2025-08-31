from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils import timezone

from recargas.models import Recarga
from usuarios.models import Usuario


class RecargasListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_id = request.GET.get('id_usuario')
        qs = Recarga.objects.all()
        if user_id:
            qs = qs.filter(id_usuario__id_usuario=user_id)
        recs = qs.values('id_recarga', 'id_usuario', 'monto', 'fecha_hora', 'metodo')
        return Response(list(recs), status=status.HTTP_200_OK)


class CrearRecargaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_id = request.data.get('id_usuario')
            monto = float(request.data.get('monto'))
            metodo = request.data.get('metodo', 'Manual')

            usuario = Usuario.objects.get(id_usuario=user_id)
            usuario.saldo = float(usuario.saldo) + monto
            usuario.save()

            rec = Recarga.objects.create(
                id_usuario=usuario,
                monto=monto,
                fecha_hora=timezone.now(),
                metodo=metodo,
            )
            return Response({'id_recarga': str(rec.id_recarga), 'saldo': float(usuario.saldo)}, status=status.HTTP_201_CREATED)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
