from django.urls import path
from .views import RegisterUserView, LoginUserView, UsuarioDetailView, RecargaEthereumView, VerificarTransaccionView, recarga_coingate, coingate_webhook

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('<uuid:id_usuario>/', UsuarioDetailView.as_view(), name='usuario-detail'),
    path('recarga/ethereum/', RecargaEthereumView.as_view(), name='recarga-ethereum'),
    path('recarga/verificar/', VerificarTransaccionView.as_view(), name='verificar-transaccion'),
    path('recarga/coingate/', recarga_coingate, name='recarga-coingate'),
    path('recarga/webhook/', coingate_webhook, name='coingate-webhook'),
]
