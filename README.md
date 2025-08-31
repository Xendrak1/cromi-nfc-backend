# Cromi NFC Backend

Backend Django para Cromi (usuarios, pagos, recargas, micros).

## Desarrollo
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Configuración
- Variables en .env (raíz del proyecto):
  - ETHEREUM_RECEIVER, ETH_BOLIVIANO_RATE
- Base de datos: ver `nfc/settings.py` (PostgreSQL).

## Endpoints
- /api/usuarios/ (login, register, detalle, recarga)
- /api/micros/
- /api/pagos/, /api/pagos/crear/
- /api/recargas/, /api/recargas/crear/

