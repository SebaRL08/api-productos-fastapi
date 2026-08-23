from fastapi import FastAPI
from pydantic import BaseModel, Field

# Creamos la instancia principal de la aplicación FastAPI
app = FastAPI(title="API de Productos", version="1.0.0")


# Modelo para CREAR un producto (lo que el usuario envía en el POST)
# No incluye "id" porque el sistema lo genera automáticamente
class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del producto")
    categoria: str
    precio: float = Field(..., gt=0, description="Debe ser mayor que 0")
    stock: int = Field(..., ge=0, description="No puede ser negativo")


# Modelo para RESPONDER (lo que el usuario recibe al consultar)
# Incluye "id" porque ya fue asignado por el sistema
class Producto(ProductoCreate):
    id: int


# "Base de datos" en memoria: una lista de productos
productos: list[Producto] = []

# Contador para asignar IDs automáticamente
siguiente_id = 1

@app.get("/productos", response_model=list[Producto])
def obtener_productos():
    return productos

from fastapi import FastAPI, HTTPException

@app.post("/productos", response_model=Producto, status_code=201)
def crear_producto(producto: ProductoCreate):
    global siguiente_id

    nuevo_producto = Producto(
        id=siguiente_id,
        nombre=producto.nombre,
        categoria=producto.categoria,
        precio=producto.precio,
        stock=producto.stock,
    )

    productos.append(nuevo_producto)
    siguiente_id += 1

    return nuevo_producto

@app.get("/productos/{id}", response_model=Producto)
def obtener_producto(id: int):
    for producto in productos:
        if producto.id == id:
            return producto

    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.put("/productos/{id}", response_model=Producto)
def actualizar_producto(id: int, datos: ProductoCreate):
    for producto in productos:
        if producto.id == id:
            producto.nombre = datos.nombre
            producto.categoria = datos.categoria
            producto.precio = datos.precio
            producto.stock = datos.stock
            return producto

    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/productos/{id}", status_code=204)
def eliminar_producto(id: int):
    for producto in productos:
        if producto.id == id:
            productos.remove(producto)
            return

    raise HTTPException(status_code=404, detail="Producto no encontrado")

