# Guía de Despliegue en Google Compute Engine

Esta guía describe los pasos necesarios para desplegar la aplicación `aparking-backend` en **Google Compute Engine** utilizando contenedores Docker.

## Preparación

1. **Construir la Imagen Docker Localmente:**

   Antes de desplegar en Compute Engine, construye tu imagen Docker localmente para asegurarte de que todo está configurado correctamente.

    ```bash
    docker build --platform linux/amd64 --tag aparking-image .
    ```

2. **Ejecutar Localmente (Opcional):**

   Para probar la imagen localmente, puedes ejecutarla con Docker:

    ```bash
    docker run --privileged -p 3000:3000 --name aparking-container -d aparking-image
    ```

   O si estás utilizando Docker Compose y deseas construir y ejecutar todo tu entorno:

    ```bash
    docker-compose up --build
    ```

## Despliegue en Google Cloud

1. **Subir la Imagen a Google Container Registry:**

    Si es la primera vez deberás ejecutar el siguiente comando:
    ```bash
    gcloud auth configure-docker eu.gcr.io
    ```
   Etiqueta y sube la imagen Docker al Google Container Registry del proyecto.

    ```bash
    docker tag aparking-image eu.gcr.io/aparking-g11-s1/aparking-container
    ```
    ```bash
    docker push eu.gcr.io/aparking-g11-s1/aparking-container
    ```

2. **Crear y Configurar la Instancia de VM en Compute Engine:**

   Ve a la [consola de Compute Engine](https://console.cloud.google.com/compute/instances?onCreate=true&project=aparking-g11-s1) para crear una nueva instancia de VM.

   - **Nombre:** `aparking-instance-s{x}` (Siendo x el sprint).
   - **Región:** `europe-southwest1`
   - **Contenedor:** Especifica la imagen del contenedor `eu.gcr.io/aparking-g11-s1/aparking-container:latest`
   - **Opciones:** Marca la opción "Ejecutar con privilegios".
   - **Identidad y Acceso a la API:** Selecciona "Permitir el acceso total a todas las APIs de Cloud".
   - **Firewall:** Seleccionar todo para permitir el tráfico entrante.
   - **Opciones Avanzadas/Herramientas de Redes/Etiquetas de Red:** Usa `backend` como etiqueta de red para asociar las reglas de firewall específicas.
   - **Tarjeta de interfaz de red**: VirtIO.

   Puedes revisar y modificar las reglas de firewall en el [gestor de firewall](https://console.cloud.google.com/net-security/firewall-manager/firewall-policies/list?project=aparking-g11-s1).

   Puedes comprobar que las reglas de firewall se aplican a la instancia en los [detalles de la regla de firewall](https://console.cloud.google.com/net-security/firewall-manager/firewall-policies/details/aparking-backend?project=aparking-g11-s1).

## Verificación

Una vez desplegada, verifica que la aplicación esté ejecutándose correctamente accediendo a ella a través de la IP pública de la instancia de VM y al puerto `3000`.

**Nota:** El proceso de despliegue puede llegar a tardar más de 15 min desde que se arranca la VM.