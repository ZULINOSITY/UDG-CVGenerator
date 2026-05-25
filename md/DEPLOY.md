# Guía de despliegue — Flask + WeasyPrint + MongoDB Atlas → Railway

## Estructura esperada del proyecto

```
raiz/
├── run.py              ← punto de entrada Flask
├── config.py           ← carga variables de entorno
├── requirements.txt    ← dependencias Python
├── Dockerfile          ← ← ← nuevo
├── .dockerignore       ← ← ← nuevo
├── railway.toml        ← ← ← nuevo
├── .env                ← solo local, NUNCA subir a git
└── app/
    ├── __init__.py
    ├── database.py
    ├── routes/
    ├── templates/
    └── static/
```

---

## Paso 1 — Verificar requirements.txt

Asegúrate de que incluya exactamente estas dependencias:

```
flask
pymongo
certifi
python-dotenv
weasyprint
gunicorn
```

Genera uno actualizado con:
```bash
pip freeze > requirements.txt
```

---

## Paso 2 — Verificar que run.py exponga `app`

Railway necesita importar `app` desde `run.py`. Asegúrate de que tu archivo termine así:

```python
from app import create_app   # o como lo tengas estructurado

app = create_app()

if __name__ == "__main__":
    app.run()
```

El objeto debe llamarse `app` (en minúscula) para que gunicorn lo encuentre con `run:app`.

---

## Paso 3 — Verificar config.py para producción

En producción no hay archivo `.env`, Railway inyecta las variables directamente.
`python-dotenv` maneja esto bien: si no hay `.env`, lee del entorno del sistema.

Tu `config.py` debería verse así:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # no falla si no existe .env en producción

MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esto-en-produccion")
```

---

## Paso 4 — Subir a GitHub

```bash
git init                        # si aún no tienes repo
git add .
git commit -m "feat: preparar para despliegue en Railway"
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

⚠️  Verifica que `.gitignore` incluya `.env` antes de hacer push.

---

## Paso 5 — Crear proyecto en Railway

1. Ir a https://railway.app y crear cuenta (gratis con GitHub)
2. Clic en **New Project** → **Deploy from GitHub repo**
3. Seleccionar tu repositorio
4. Railway detecta el `Dockerfile` automáticamente

---

## Paso 6 — Configurar variables de entorno en Railway

En el panel de tu proyecto → pestaña **Variables**, agregar:

| Variable       | Valor                                      |
|----------------|--------------------------------------------|
| `MONGO_URI`    | `mongodb+srv://usuario:pass@cluster.../db` |
| `SECRET_KEY`   | una cadena larga y aleatoria               |
| `FLASK_ENV`    | `production`                               |

Estas reemplazan tu archivo `.env` local.

---

## Paso 7 — Deploy y URL pública

Railway construye la imagen Docker y despliega automáticamente.
Al terminar, te asigna una URL del tipo:

```
https://tu-proyecto.up.railway.app
```

Cada `git push` a `main` dispara un redeploy automático.

---

## Solución de problemas comunes

**Error: `ModuleNotFoundError: No module named 'app'`**
→ Verifica que `run.py` esté en la raíz y que el CMD del Dockerfile use `run:app`.

**Error de WeasyPrint al generar PDF**
→ El `--timeout 120` de gunicorn previene timeouts en PDFs pesados.
→ Si persiste, revisa que `fonts-liberation` esté en el Dockerfile.

**MongoDB Atlas rechaza conexión**
→ En Atlas → Network Access → agrega `0.0.0.0/0` para permitir IPs de Railway.
→ Verifica que `MONGO_URI` incluya `?tls=true&tlsCAFile=...` o usa `certifi` en `database.py`.

**Certifi en producción**
En tu `database.py`, si usas certifi así:
```python
import certifi
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
```
Esto funciona igual en Docker, no necesita cambios.

---

## Costo estimado (Railway)

| Plan    | Incluye                          | Costo      |
|---------|----------------------------------|------------|
| Hobby   | $5 USD de crédito/mes gratis     | $0         |
| Pro     | Sin límite de horas              | ~$5–20/mes |

Para uso académico de bajo tráfico, el plan Hobby gratuito es suficiente.
