from django.urls import path
from .views import RegisterUserView, LoginUserView, UsuarioDetailView, VerificarTransaccionView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('<uuid:id_usuario>/', UsuarioDetailView.as_view(), name='usuario-detail'),
    path('recarga/verificar/', VerificarTransaccionView.as_view(), name='verificar-transaccion'),
]
