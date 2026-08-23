# api-productos-fastapi
Desarrollar una API REST funcional utilizando Python y FastAPI, aplicando principios de programación, estructuras de datos, manejo de solicitudes HTTP, validación de información y documentación automática de servicios.
# API de Productos - FastAPI

API REST desarrollada con Python y FastAPI para la administración de productos de una empresa. Permite consultar, registrar, actualizar y eliminar productos, aplicando validaciones de datos y manejo de errores mediante códigos de estado HTTP.


## Tecnologías utilizadas

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic (validación de datos)
- Swagger UI / OpenAPI (documentación interactiva)

## Estructura del proyecto


## Recurso: Producto

| Campo      | Tipo    | Descripción                          |
|------------|---------|---------------------------------------|
| id         | Entero  | Generado automáticamente por el sistema |
| nombre     | Texto   | Obligatorio, no puede estar vacío     |
| categoria  | Texto   | Categoría del producto                |
| precio     | Decimal | Debe ser mayor que 0                  |
| stock      | Entero  | No puede ser negativo (mínimo 0)      |

## Endpoints

| Método | Ruta                | Descripción                          | Código éxito | Códigos de error |
|--------|---------------------|---------------------------------------|--------------|-------------------|
| GET    | `/productos`        | Consulta todos los productos          | 200          | -                 |
| GET    | `/productos/{id}`   | Consulta un producto específico       | 200          | 404               |
| POST   | `/productos`        | Registra un nuevo producto            | 201          | 422               |
| PUT    | `/productos/{id}`   | Actualiza un producto existente       | 200          | 404, 422          |
| DELETE | `/productos/{id}`   | Elimina un producto                   | 204          | 404               |

http://127.0.0.1:8000/docs ---> Esto abre **Swagger UI**, donde se pueden probar todos los endpoints de forma interactiva.

## Validaciones implementadas

- El nombre del producto es obligatorio (no se aceptan valores vacíos).
- El precio debe ser mayor que 0.
- El stock no puede ser negativo.
- El ID es generado automáticamente por el sistema, garantizando que siempre sea único.
- Se retorna código **404** al consultar, actualizar o eliminar un producto que no existe.
- Se retorna código **422** cuando los datos enviados no cumplen las validaciones.


