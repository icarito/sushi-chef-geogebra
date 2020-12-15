Script para importar archivos SCORM de Geogebra
===============================================

(Sushi script for importing Geogebra SCORM files - english at bottom)

== Instalación de prerequisitos ==

Asumiendo que se tiene Python3 instalado y el gestor de paquetes de Python, pip (python3-pip en Debian y derivados).

  pip3 install -r requirements.txt

Debería instalar todos los prerequisitos.

== Ejecución ==

Previamente se debe haber descargado a una ruta conocida el archivo SCORM zip desde la página de Geogebra.

Por ejemplo https://www.geogebra.org/material/show/id/MQWTjB4u?trigger=download_scorm - oprimiendo "Descargar" y "Paquete SCORM .zip". Esto producirá el archivo `mMQWTjB4u-scorm-rea-limitada-por-dos-funciones.zip` en un directorio conocido.

Para publicar es necesario un token de un usuario de Kolibri Studio.

  python3 ./geogebra_chef.py (opcional: --token [token de kolibri studio] --deploy --publish)

  (se pueden ver algunas entradas de log que se pueden ignorar)

  Ingrese el título: [ingresar título del canal]

  Ingrese la descripción: [ingresar descripción del canal]

  Ruta del archivo SCORM: [ingresar ruta del archivo .zip]

Si se omitió el token, se preguntará a continuación:

  Enter content curation server token ('q' to quit): [token de kolibri studio]

Si se usó las opciones `--deploy` y `--publish` entonces ya estará publicado el contenido y podrá ser importado con el respectivo token en un servidor Kolibri.

== Para ver el contenido en Kolibri ==

Es necesario editar el archivo `options.ini` que se encuentra en el directorio de configuración de Kolibri, y añadir o editar las siguientes líneas:

  [HTML5] 
  SANDBOX = allow-scripts allow-same-origin

Esto puede concebiblemente constituir una falla de seguridad si el contenido hospedado fuese malicioso, por lo tanto no está activado en los servidores públicos de learningequality. Esperamos una mejor solución de parte de ellos.

= English Instructions =

For the benefit of others and for the kolibri team to understand the purpose of this repo.

Install dependencies with: `pip3 install -r requirements.txt`

Then run: `python3 ./geogebra_chef.py`

You will be asked the Channel title and description, and the full path for the SCORM file downloaded from the geogebra site, and the kolibri studio token (you can add the regular sushi arguments --token [token] --deploy --publish).

The content will only be visible if you configure your kolibri server's `options.ini` file with:

  [HTML5] 
  SANDBOX = allow-scripts allow-same-origin

This may constitute a security issue when malicious content is posted, so it needs to happen locally until a better option is offered in Kolibri.
