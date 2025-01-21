# Ingeniería de Requisitos - Proyecto AgroOvino

## 1. Introducción

Este documento detalla los requisitos de ingeniería para una aplicación web de gestión ovina, diseñada para ayudar a los criadores de ovejas (cabañas) a administrar eficientemente su plantel.

## 2. Descripción General del Sistema

La aplicación permitirá a los usuarios gestionar su plantel ovino, incluyendo el registro individual de ovejas, la gestión de planteletas de venta y exposición, y el seguimiento genealógico de ovejas pedigree.

## 3. Requisitos Funcionales

### 3.1 Gestión de Cabaña (Usuario)

- RF1.1: El sistema debe permitir el registro de nuevas cabañas (usuarios).
- RF1.2: Cada cabaña debe poder gestionar su propio plantel de ovejas.

### 3.2 Gestión de Ovejas

- RF2.1: El sistema debe permitir el registro individual de ovejas con los siguientes datos:
  - Raza
  - Tipo (M0 o Pedigree)
  - Género
  - Peso
  - Edad
  - Número de identificación
  - Alias (opcional)
- RF2.2: El sistema debe permitir el registro por lotes de ovejas.
- RF2.3: El sistema debe proporcionar una vista en formato tabla de todas las ovejas del plantel.
- RF2.4: El sistema debe permitir ver el detalle individual de cada oveja.
- RF2.5: El sistema debe permitir la edición de la información de cada oveja.

### 3.3 Planteletas

- RF3.1: El sistema debe proporcionar una sección de "Planteleta de Venta" para las ovejas destinadas a la venta.
- RF3.2: El sistema debe proporcionar una sección de "Planteleta de Exposición" para las ovejas destinadas a exhibición.
- RF3.3: El sistema debe permitir marcar/desmarcar ovejas para venta o exposición.

### 3.4 Genealogía

- RF4.1: Para ovejas pedigree, el sistema debe permitir el registro de su ascendencia (padre y madre).
- RF4.2: El sistema debe permitir ver el árbol genealógico de una oveja pedigree.
- RF4.3: El sistema debe permitir el registro del número identificador y alias (opcional) de los padres.

### 3.5 Ranking (Prioridad Baja)

- RF5.1: El sistema debe proporcionar una sección de ranking que muestre las mejores ovejas del establecimiento según criterios predefinidos.

## 4. Requisitos No Funcionales

### 4.1 Usabilidad

- RNF1.1: La interfaz de usuario debe ser intuitiva y fácil de usar.
- RNF1.2: El sistema debe ser accesible desde dispositivos móviles y de escritorio.

### 4.2 Rendimiento

- RNF2.1: El sistema debe cargar las páginas en menos de 3 segundos con una conexión estándar.
- RNF2.2: El sistema debe ser capaz de manejar al menos 1000 registros de ovejas sin degradación del rendimiento.

### 4.3 Seguridad

- RNF3.1: Todos los datos transmitidos deben ser encriptados usando HTTPS.
- RNF3.2: Las contraseñas de usuario deben ser almacenadas de forma segura utilizando técnicas de hashing.

### 4.4 Disponibilidad

- RNF4.1: El sistema debe estar disponible el 99.9% del tiempo.

### 4.5 Escalabilidad

- RNF5.1: El sistema debe ser capaz de escalar para manejar un aumento en el número de usuarios y datos sin una degradación significativa del rendimiento.

## 5. Restricciones

- El sistema debe ser desarrollado utilizando tecnologías web modernas (por ejemplo, React, Next.js).
- El sistema debe cumplir con las regulaciones locales de protección de datos.

## 6. Supuestos y Dependencias

- Se asume que los usuarios tendrán acceso a dispositivos con conexión a internet.
- El sistema dependerá de un servicio de base de datos para almacenar la información de las ovejas y usuarios.

## 7. Futuros Desarrollos

- Implementación de un sistema de notificaciones para eventos importantes (por ejemplo, fechas de vacunación, esquila).
- Desarrollo de una API para integración con otros sistemas agrícolas.
- Implementación de análisis predictivo para la salud y productividad del ganado.






### Antes de terminar el proyecto para entrega en harvard

* Refactorizar y colocar comentarios en ingles
* Generar una profunda documentacion en README.MD
* Grabar la pantalla mostrando el proyecto

* Importante:
  * Terminar la funcionalidad de eliminar ovino y eliminar venta
  * Corregir el valor individual en la venta ind de los ovinos en lotes
  * Agregar mensajes de errores 

  

















para borrar la base de datos comandos


python3 manage.py flush


rm db.sqlite3


find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

python3 manage.py makemigrations
python3 manage.py migrate


# crea archivo requerimientos con las dependencias
pip freeze > requirements.txt