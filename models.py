from dataclasses import dataclass, field

# Clase para representar un libro
@dataclass
class Book:
    book_id: int           # Identificador único del libro
    title: str             # Título del libro
    author: str            # Autor
    year: int              # Año de publicación
    available: bool = field(default=True)  # Estado: disponible o prestado

    def mark_borrowed(self):
        """Marca el libro como prestado"""
        if not self.available:
            raise ValueError("El libro ya está prestado.")
        self.available = False

    def mark_returned(self):
        """Marca el libro como disponible otra vez"""
        self.available = True


# Clase para representar un miembro de la biblioteca
@dataclass
class Member:
    member_id: int   # Identificador único del miembro
    name: str        # Nombre del miembro