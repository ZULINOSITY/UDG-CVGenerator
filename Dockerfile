# Imagen base Debian slim — compatible con GTK3 y WeasyPrint
FROM python:3.11-slim

# Dependencias del sistema para WeasyPrint (GTK3 runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # GTK3 y dependencias gráficas requeridas por WeasyPrint
    libgtk-3-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libssl-dev \
    # Fuentes para renderizado correcto de PDFs
    fonts-liberation \
    fonts-dejavu-core \
    # Utilidades mínimas
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Primero copiamos solo requirements para aprovechar caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Puerto que expondrá la app (Railway lo detecta automáticamente)
EXPOSE 8000

# Gunicorn como servidor WSGI de producción
# -w 2: 2 workers (suficiente para bajo tráfico académico)
# --timeout 120: tiempo extra para generación de PDFs con WeasyPrint
CMD ["gunicorn", "-w", "2", "--timeout", "120", "-b", "0.0.0.0:8000", "run:app"]
