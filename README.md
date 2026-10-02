# Desarrollo de Aplicaciones Web - Proyecto General

## Datos de los estudiantes  
**Nombres:** Mendieta López Stalin Gabriel - Quijije Coral Lilian Paulina  
**Asignatura:** Desarrollo de Aplicaciones Web  
**Paralelo:** (E)  
**Período académico:** 2026–2026  

## Descripción del trabajo
Este repositorio reúne el desarrollo de las actividades prácticas realizadas en la asignatura Desarrollo de Aplicaciones Web. El proyecto comenzó con una página web básica en HTML y, con el avance de las semanas, ha evolucionado incorporando estructura semántica, contenido multimedia, funcionalidades dinámicas mediante JavaScript y posteriormente un backend desarrollado con Flask.

En su versión actual, el proyecto presenta una página web institucional para IMPORDYCOM S.A., una empresa dedicada a la importación y distribución de materiales de acero inoxidable en Ecuador. El sitio incluye información sobre la empresa, sus productos, medios de contacto y diferentes módulos para la gestión de productos, clientes, proveedores y facturación. Además, incorpora formularios validados mediante Flask-WTF y persistencia de datos utilizando una base de datos relacional PostgreSQL.

## Estructura del código
El proyecto está compuesto por:  
- Archivo principal `app.py`
- Carpeta `templates/` para las plantillas HTML
- Plantilla base `base.html`
- Carpeta `forms/` para los formularios Flask-WTF y sus validaciones
- Carpeta `static/` para archivos CSS, JavaScript e imágenes
- Carpeta `data/` que conserva la base de datos SQLite utilizada en el avance anterior
- Carpeta `conexion/` para la conexión centralizada con PostgreSQL
- Carpeta `sql/` para el esquema de la base de datos relacional
- Rutas y enlaces dinámicos mediante Flask y `url_for()`
- Herencia de plantillas con Jinja2
- Diseño responsivo mediante Bootstrap
- Validaciones de formularios con Flask-WTF y WTForms
- Operaciones de consulta y gestión de productos mediante PostgreSQL

## Avances del proyecto  

### Semana 2  
- Creación de la estructura inicial del documento HTML.
- Uso de encabezados `<h1>`, `<h2>` y `<h3>`.
- Definición del tema general del proyecto.

### Semana 3  
- Creación de un menú de navegación interno.
- Desarrollo de las secciones Inicio, Quiénes Somos, Productos y Contacto.
- Inserción de imágenes relacionadas con la empresa.
- Incorporación de un video de YouTube sobre el proceso del acero inoxidable.
- Uso de etiquetas semánticas como `header`, `nav`, `main`, `section`, `aside` y `footer`.
- Mejora de la organización y presentación del contenido con CSS en línea.

### Semana 4  
- Implementación de estilos con **CSS3 externo** para mejorar la presentación del sitio.  
- Uso de clases y selectores para optimizar la estructura del diseño.  
- Aplicación de **Bootstrap** para lograr un diseño responsivo y adaptable a dispositivos móviles.  
- Mejora del diseño de botones, menús y tarjetas de contenido.  
- Optimización de la experiencia de usuario (UX) y organización visual del sitio.  
- Ajustes en la estructura para mejorar la accesibilidad y legibilidad del contenido.

### Semana 5  
- Implementación de JavaScript  
- Manipulación del DOM y eventos  
- Uso de `addEventListener`, `submit` y `preventDefault()`  
- Validación de formularios  
- Creación dinámica de elementos con `createElement()`  
- Eliminación de registros  
- Contador de solicitudes  
- Aplicación de diseño dinámico con Bootstrap  

### Semana 6  
- Implementación de validaciones dinámicas en formularios con JavaScript.  
- Validación en tiempo real usando eventos `input`, `blur`, `change` y `submit`.  
- Verificación de campos obligatorios y longitud mínima.  
- Validación de formato del nombre (solo letras y espacios).  
- Mensajes de error y éxito debajo de cada campo.  
- Aplicación de clases Bootstrap como `is-valid`, `is-invalid`, `alert-success` y `alert-danger`.  
- Mejora de la experiencia de usuario mediante retroalimentación visual inmediata.

### Semana 7
- Reorganización de la interfaz con una estructura preparada para futuras plantillas de Flask.  
- Identificación de secciones reutilizables mediante comentarios en el HTML.  
- Implementación de contenido dinámico utilizando arreglos y objetos en JavaScript.  
- Renderización dinámica de productos y solicitudes mediante funciones reutilizables.  
- Uso de estructuras repetitivas y condicionales para mostrar la información.  
- Conservación de las validaciones dinámicas implementadas en la Semana 6.  
- Organización del proyecto para facilitar su futura integración con Flask y bases de datos.

### Semana 8
- Integración de componentes interactivos de Bootstrap, como Modal y Spinner.  
- Implementación de un indicador de carga durante el registro de solicitudes.  
- Mejora del diseño del formulario mediante `form-control`, `form-select` y el sistema Grid de Bootstrap.  
- Optimización de la interfaz utilizando clases utilitarias y componentes responsivos de Bootstrap.  
- Incorporación de una ventana Modal para mostrar información adicional de la empresa.

### Semana 9
- Integración del proyecto con el framework **Flask**.
- Creación de rutas para las diferentes páginas del sitio.
- Adaptación de las páginas HTML existentes a una estructura basada en Flask.
- Organización del proyecto para trabajar con plantillas dinámicas mediante Jinja2.
- Conservación de los estilos, imágenes y funcionalidades desarrolladas anteriormente.

### Semana 10
- Implementación de **plantillas dinámicas con Flask y Jinja2**.
- Creación de la plantilla base `base.html`.
- Uso de herencia de plantillas mediante `{% extends %}` y `{% block %}`.
- Implementación de componentes reutilizables.
- Uso de `url_for()` para la generación de rutas.
- Organización de las páginas de productos, clientes, proveedores y facturación.

### Semana 11
- Implementación de **Flask-WTF y WTForms** para la validación de formularios.
- Creación de formularios para productos, clientes, proveedores y facturación.
- Organización de los formularios dentro de la carpeta `forms/`.
- Implementación de validaciones como `DataRequired`, `Length`, `Email`, `Regexp` y `NumberRange`.
- Uso de `form.validate_on_submit()` para validar los datos recibidos.
- Implementación de protección CSRF mediante `form.hidden_tag()`.
- Actualización de `requirements.txt` con las dependencias utilizadas.

### Semana 12
- Implementación de **persistencia de datos mediante SQLite**.
- Creación de la base de datos `data/ferreteria.db` y la tabla `productos`.
- Conexión de Flask con SQLite mediante `sqlite3`.
- Almacenamiento de productos utilizando consultas `INSERT` parametrizadas.
- Consulta y visualización de productos mediante `SELECT`, `fetchall()` y Jinja2.
- Implementación de edición y eliminación de productos mediante `UPDATE` y `DELETE`.
- Comprobación de la persistencia de los datos después de cerrar y reiniciar la aplicación Flask.

### Semana 13
- Migración de la persistencia de productos desde **SQLite hacia PostgreSQL**.
- Configuración de la base de datos relacional `impordycom_web` mediante `sql/esquema.sql`.
- Implementación de una conexión centralizada con `psycopg` y variables de entorno.
- Creación de las tablas `productos`, `proveedores`, `clientes` y `facturas`, utilizando claves primarias y foráneas.
- Implementación de operaciones **SELECT, INSERT, UPDATE y DELETE** mediante consultas parametrizadas.
- Uso de consultas `JOIN` para relacionar productos con proveedores.
- Verificación de la persistencia de los datos y actualización de `requirements.txt`.

### Semana 14
- Implementación de un **sistema de login funcional** con Flask-Login.
- Registro de usuarios y almacenamiento seguro de contraseñas mediante **hash**.
- Implementación de inicio y cierre de sesión con `login_user()` y `logout_user()`.
- Protección de las rutas internas de **productos, clientes, proveedores y facturación** mediante `@login_required`.
- Creación de las vistas de **login, registro y dashboard**, integradas con Jinja2 y Bootstrap.
- Configuración de `SECRET_KEY` y credenciales mediante **variables de entorno**.
- Actualización de `requirements.txt` y `sql/esquema.sql`.
- Realización de pruebas funcionales del sistema de autenticación.

### Semana 15
* Implementación del **CRUD completo** de productos, clientes y proveedores con PostgreSQL.
* Desarrollo de operaciones **crear, listar, modificar y eliminar** mediante consultas SQL parametrizadas.
* Integración de relaciones mediante **claves primarias y foráneas**.
* Implementación de consultas **JOIN** para mostrar información relacionada.
* Realización de pruebas funcionales de los módulos y de la facturación.

### Semana 16
* Aplicación de **mejoras visuales finales** en la interfaz.
* Incorporación de imágenes de los productos y optimización del diseño responsivo.
* Implementación de validación para evitar **cédulas duplicadas**.
* Configuración y despliegue de la aplicación en **Render** con PostgreSQL.
* Realización de pruebas finales y **finalización del proyecto**.
