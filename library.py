from typing import List, Optional
from models import Book, Member

# Clase que gestiona toda la lógica de la biblioteca
class Library:
    def __init__(self):
        # Lista de libros en la biblioteca
        self.books: List[Book] = []
        # Lista de miembros registrados
        self.members: List[Member] = []
        # Diccionario de préstamos: book_id -> member_id
        self._loans: dict[int, int] = {}

    # ---- Gestión de libros ----
    def add_book(self, title: str, author: str, year: int) -> Book:
        """Agrega un nuevo libro con ID incremental"""
        new_id = (max([b.book_id for b in self.books]) + 1) if self.books else 1
        book = Book(book_id=new_id, title=title.strip(), author=author.strip(), year=int(year))
        self.books.append(book)
        return book

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """Busca un libro por su ID"""
        return next((b for b in self.books if b.book_id == book_id), None)

    def search_books(self, query: str) -> List[Book]:
        """Busca libros por título o autor"""
        q = query.lower().strip()
        return [b for b in self.books if q in b.title.lower() or q in b.author.lower()]

    def list_available(self) -> List[Book]:
        """Devuelve todos los libros que están disponibles"""
        return [b for b in self.books if b.available]

    # ---- Gestión de miembros ----
    def add_member(self, name: str) -> Member:
        """Agrega un miembro con ID incremental"""
        new_id = (max([m.member_id for m in self.members]) + 1) if self.members else 1
        member = Member(member_id=new_id, name=name.strip())
        self.members.append(member)
        return member

    def find_member_by_id(self, member_id: int) -> Optional[Member]:
        """Busca un miembro por su ID"""
        return next((m for m in self.members if m.member_id == member_id), None)

    # ---- Préstamos ----
    def lend_book(self, book_id: int, member_id: int) -> None:
        """Presta un libro a un miembro"""
        book = self.find_book_by_id(book_id)
        member = self.find_member_by_id(member_id)
        if not book:
            raise ValueError("Libro no encontrado.")
        if not member:
            raise ValueError("Miembro no encontrado.")
        if not book.available:
            raise ValueError("El libro ya está prestado.")
        book.mark_borrowed()
        self._loans[book_id] = member_id  # Registramos el préstamo

    def return_book(self, book_id: int) -> None:
        """Devuelve un libro prestado"""
        book = self.find_book_by_id(book_id)
        if not book:
            raise ValueError("Libro no encontrado.")
        if book_id not in self._loans:
            raise ValueError("Ese libro no está prestado.")
        book.mark_returned()
        del self._loans[book_id]  # Eliminamos el préstamo del registro