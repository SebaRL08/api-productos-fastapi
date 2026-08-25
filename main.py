from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, Session, mapped_column

from database import Base, SessionLocal, engine


app = FastAPI(title="API de Productos", version="1.0.0")


class ProductoDB(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    precio: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)


def obtener_sesion():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    categoria: str
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class Producto(ProductoCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


@app.get("/productos", response_model=list[Producto])
def obtener_productos(db: Session = Depends(obtener_sesion)):
    return db.query(ProductoDB).all()


@app.post("/productos", response_model=Producto, status_code=201)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(obtener_sesion)
):
    nuevo_producto = ProductoDB(
        nombre=producto.nombre,
        categoria=producto.categoria,
        precio=producto.precio,
        stock=producto.stock,
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto


@app.get("/productos/{id}", response_model=Producto)
def obtener_producto(
    id: int,
    db: Session = Depends(obtener_sesion)
):
    producto = db.get(ProductoDB, id)

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto
    

@app.put("/productos/{id}", response_model=Producto)
def actualizar_producto(
    id: int,
    datos: ProductoCreate,
    db: Session = Depends(obtener_sesion)
):
    producto = db.get(ProductoDB, id)

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto.nombre = datos.nombre
    producto.categoria = datos.categoria
    producto.precio = datos.precio
    producto.stock = datos.stock

    db.commit()
    db.refresh(producto)

    return producto


@app.delete("/productos/{id}", status_code=204)
def eliminar_producto(
    id: int,
    db: Session = Depends(obtener_sesion)
):
    producto = db.get(ProductoDB, id)

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    db.delete(producto)
    db.commit()
