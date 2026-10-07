from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app.models import db

class Baul(db.Model):
    __tablename__ = "baul"

    id_baul: Mapped[int] = mapped_column(Integer, primary_key=True)
    Plataforma: Mapped[str] = mapped_column(String(100), nullable=False)
    usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    clave: Mapped[str] = mapped_column(String(255), nullable=False)

    def to_dict(self):
        return {
            "id_baul": self.id_baul,
            "Plataforma": self.Plataforma,
            "usuario": self.usuario,
            "clave": self.clave
        }