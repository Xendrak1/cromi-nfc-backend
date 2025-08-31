from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from micros.models import Micro


class MicrosListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        micros = Micro.objects.all().values('id_micro', 'linea', 'placa')
        return Response(list(micros), status=status.HTTP_200_OK)
