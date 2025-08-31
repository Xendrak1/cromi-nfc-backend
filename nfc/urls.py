"""
URL configuration for nfc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from micros.views import MicrosListView
from pagos.views import PagosListView, CrearPagoView
from recargas.views import RecargasListView, CrearRecargaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/micros/', MicrosListView.as_view(), name='micros-list'),
    path('api/pagos/', PagosListView.as_view(), name='pagos-list'),
    path('api/pagos/crear/', CrearPagoView.as_view(), name='pagos-crear'),
    path('api/recargas/', RecargasListView.as_view(), name='recargas-list'),
    path('api/recargas/crear/', CrearRecargaView.as_view(), name='recargas-crear'),
]
