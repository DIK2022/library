from typing import Dict


class Book:
    """
    Класс для представления книги в библиотеке.

    Attributes
    __________
        id: int
         Уникальный идентификатор книги.
        title: str
         Название книги.
        author: str
         Автор книги.
        year: int
         Год издания книги.
        status: str
         Статус книги (по умолчанию "в наличии").
    Methods
    _______
    to_dict()
        Преобразует объект книги в словарь
    from_dict(data={})
        Создаёт объект книги из словаря
    """
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """
        Инициализирует объект книги.

        :param id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги, по умолчанию "в наличии".
        """
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> Dict[str, str]:
        """
        Метод преобразует объект книги в словарь.

        :return: Словарь с данными книги.
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "year": str(self.year),
            "status": self.status
        }

    @staticmethod
    def from_dict(data: Dict[str, str]) -> 'Book':
        """
        Метод создаёт объект книги из словаря.

        :param data: Словарь с данными книги.
        :return: Объект книги.
        """
        return Book(
            id=int(data["id"]),
            title=data["title"],
            author=data["author"],
            year=int(data["year"]),
            status=data["status"]
        )

