# Proyecto Tienda de Ferretería Online (Ferretería Django)

Este es un proyecto de tienda online para una ferretería, desarrollado con Python y Django. Permite a los usuarios ver un catálogo de productos, agregarlos a un carrito de compras y realizar pedidos. La gestión de productos, categorías, clientes y pedidos se puede realizar a través del panel de administración de Django.

## Características Principales

* **Gestión de Catálogo:**
    * Visualización de productos con detalles (nombre, descripción, precio, imagen, stock).
    * Organización de productos por categorías (con imágenes para categorías).
* **Carrito de Compras:**
    * Añadir productos al carrito.
    * Visualizar ítems en el carrito.
    * Modificar la cantidad de ítems en el carrito.
    * Eliminar ítems del carrito.
    * Cálculo del precio total del carrito.
* **Proceso de Pedido:**
    * Colocar un pedido con los ítems del carrito.
    * Los pedidos se guardan con estado "pendiente".
    * El carrito se vacía después de realizar un pedido.
    * Actualización del stock de productos.
    * Página de confirmación del pedido.
* **Panel de Administración de Django:**
    * CRUD (Crear, Leer, Actualizar, Eliminar) para todas las tablas principales:
        * Categorías
        * Productos
        * Clientes
        * Pedidos y Detalles de Pedidos
        * (Gestión de ítems del carrito, aunque el carrito es más transaccional)

## Tecnologías Utilizadas

* **Backend:** Python, Django
* **Base de Datos:** SQLite3 (por defecto para desarrollo) - Configurable para MySQL/PostgreSQL en `settings.py`.
* **Frontend:** HTML, CSS (básico, integrado en plantillas Django)
* **Manejo de Imágenes:** Pillow

## Configuración e Instalación

Sigue estos pasos para poner en marcha el proyecto en un entorno de desarrollo local:

**Prerrequisitos:**
* Python 3.8+
* pip (manejador de paquetes de Python)
* Git

**Pasos:**

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DE_LA_CARPETA_DEL_PROYECTO>
    ```

2.  **Crear y Activar un Entorno Virtual:**
    (Se recomienda usar un entorno virtual)
    ```bash
    python3 -m venv venv
    ```
    * En Linux/macOS (bash/zsh):
        ```bash
        source venv/bin/activate
        ```
    * En Linux/macOS (fish):
        ```bash
        source venv/bin/activate.fish
        ```
    * En Windows (cmd):
        ```bash
        venv\Scripts\activate
        ```
    * En Windows (PowerShell):
        ```bash
        venv\Scripts\Activate.ps1
        ```

3.  **Instalar Dependencias:**
    Asegúrate de tener un archivo `requirements.txt` (ver nota abajo).
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la Base de Datos:**
    El proyecto está configurado para usar SQLite por defecto. Las migraciones crearán el archivo `db.sqlite3`.
    Aplica las migraciones:
    ```bash
    python manage.py migrate
    ```

5.  **Crear un Superusuario:**
    Para acceder al panel de administración de Django:
    ```bash
    python manage.py createsuperuser
    ```
    Sigue las instrucciones para establecer un nombre de usuario, correo y contraseña.

6.  **Ejecutar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/`.
    El panel de administración estará en `http://127.0.0.1:8000/admin/`.

## Uso Básico

* **Catálogo de Productos:** Navega a la página principal (`http://127.0.0.1:8000/`) para ver los productos y añadirlos al carrito.
* **Carrito de Compras:** Accede a `/cart/` para ver, modificar o eliminar ítems de tu carrito y proceder a colocar el pedido.
* **Panel de Administración:** Accede a `/admin/` e inicia sesión con tus credenciales de superusuario para gestionar los datos del sistema.

## Estructura del Proyecto (Simplificada)

* `manage.py`: Script de utilidad de Django.
* `tienda_config/`: Directorio de configuración del proyecto Django (`settings.py`, `urls.py` principal).
* `ferreteria/`: Aplicación principal de Django que contiene:
    * `models.py`: Definiciones de los modelos de la base de datos.
    * `views.py`: Lógica para manejar las peticiones web.
    * `urls.py`: Definiciones de URL específicas de la app.
    * `templates/ferreteria/`: Plantillas HTML.
    * `admin.py`: Configuración del panel de administración para los modelos.
* `media/`: Directorio donde se almacenan las imágenes subidas (productos, categorías).
* `venv/`: Directorio del entorno virtual (ignorado por Git).

## Futuras Mejoras (To-Do)

* Implementar un sistema de autenticación de usuarios completo (registro, inicio de sesión, perfiles de cliente).
* Filtrado de productos por categoría en el catálogo.
* Mejoras en el diseño y la experiencia de usuario (CSS más avanzado, JavaScript).
* Integración con pasarelas de pago.
* Búsqueda de productos.
* Gestión de perfiles de cliente.
* Historial de pedidos para clientes.

---
*Este proyecto fue desarrollado como parte de la Práctica Final.*
*Autor: [Tu Nombre/Alias - teracrow]*
*Fecha: Mayo 2025*
