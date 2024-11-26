import json
from typing import List, Optional

from books import Book


# Файл для хранения данных библиотеки
LIBRARY_FILE = "library.json"


def load_library(file_path: str) -> List[Book]:
    """
    Метод загружает библиотеку книг из json файла.

    :param file_path: Путь к файлу, из которого загружаются книги.
    :return: Список объектов книг, загруженных из файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [Book.from_dict(book) for book in json.load(file)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_library(books: List[Book], file_path: str) -> None:
    """
    Метод сохраняет список книг в json файл.

    :param books: Список объектов книг, которые нужно сохранить в json файл.
    :param file_path: Путь к файлу, в который нужно сохранить данные.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)
    print(f"Запись в {file_path}.")


def add_book(title: str, author: str, year: int, file_path: str) -> Book:
    """
    Метод добавляет книгу в библиотеку и записывает в json файл.

    :param title: Название книги.
    :param author: Автор книги.
    :param year: Год издания книги.
    :param file_path: Путь к файлу, где хранится библиотека.
    :return: Объект добавленной книги.
    """
    books = load_library(file_path)
    new_id = max((book.id for book in books), default=0) + 1
    new_book = Book(id=new_id, title=title, author=author, year=year)
    books.append(new_book)
    save_library(books, file_path)
    return new_book


def remove_book(book_id: int, file_path: str) -> bool:
    """
    Метод удаляет книгу по её ID и записывает изменения в json файл.

    :param book_id: ID книги, которую нужно удалить.
    :param file_path: Путь к файлу, где хранится библиотека.
    :return: True, если книга была удалена, иначе False.
    """
    books = load_library(file_path)
    filtered_books = [book for book in books if book.id != book_id]
    if len(filtered_books) == len(books):
        return False
    save_library(filtered_books, file_path)
    return True


def search_books(file_path: str, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
    """
    Метод поиска книги по названию, автору или году.

    :param file_path: Путь к файлу, где хранится библиотека.
    :param title: Название книги (поиск по частичному совпадению).
    :param author: Автор книги (поиск по частичному совпадению).
    :param year: Год издания книги.
    :return: Список книг, соответствующих критериям поиска.
    """
    books = load_library(file_path)
    results = books
    if title:
        results = [book for book in results if title.lower() in book.title.lower()]
    if author:
        results = [book for book in results if author.lower() in book.author.lower()]
    if year:
        results = [book for book in results if book.year == year]
    return results


def list_books(file_path: str) -> List[Book]:
    """
    Метод возвращает список всех книг в библиотеке.

    :param file_path: Путь к файлу, где хранится библиотека.
    :return: Список всех книг.
    """
    return load_library(file_path)


def update_book_status(book_id: int, status: str, file_path: str) -> bool:
    """
    Метод обновляет статус книги (например, 'в наличии' или 'выдана').

    :param book_id: ID книги, для которой нужно изменить статус.
    :param status: Новый статус книги.
    :param file_path: Путь к файлу, где хранится библиотека.
    :return: True, если статус был успешно обновлён, иначе False.
    """
    if status not in ["в наличии", "выдана"]:
        raise ValueError("Invalid status. Use 'в наличии' or 'выдана'.")
    books = load_library(file_path)
    for book in books:
        if book.id == book_id:
            book.status = status
            save_library(books, file_path)
            return True
    return False

def add_book_to_library()->None:
    """
    Метод ввода данных для добавления книги в библиотеку
    :return: None
    """
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = int(input("Введите год издания: "))
    new_book = add_book(title, author, year, LIBRARY_FILE)
    print(f"Книга добавлена: {new_book.to_dict()}")

def del_book()->None:
    """
    Метод ввода данных для удаления книги из библиотеки
    :return: None
    """
    book_id = int(input("Введите ID книги для удаления: "))
    if remove_book(book_id, LIBRARY_FILE):
        print("Книга удалена.")
    else:
        print("Книга с таким ID не найдена.")

def search_for_book()->None:
    """
    Метод ввода данных для поиска книги в библиотеке
    :return: None
    """
    title = input("Введите название книги, или оставьте пустым: ")
    author = input("Введите автора книги, или оставьте пустым: ")
    year_input = input("Введите год издания, или оставьте пустым: ")
    year = int(year_input) if year_input else None
    results = search_books(LIBRARY_FILE, title=title, author=author, year=year)
    if results:
        for book in results:
            print(book.to_dict())
    else:
        print("Книга не найдена.")

def show_all_books()->None:
    """
    Метод вывода всех книг библиотеки в консоль
    :return: None
    """
    books = list_books(LIBRARY_FILE)
    if books:
        for book in books:
            print(book.to_dict())
    else:
        print("Библиотека пуста.")

def change_status_of_book()->None:
    """
    Метод ввода данных для изменения статуса книги в библиотеку
    :return: None
    """
    book_id = int(input("Введите ID книги для изменения статуса: "))
    status = input("Введите новый статус ('в наличии' или 'выдана'): ")
    if update_book_status(book_id, status, LIBRARY_FILE):
        print("Статус книги обновлён.")
    else:
        print("Книга с таким ID не найдена.")

def exit_library()->None:
    """
    Метод завершения работы програаааааммы
    :return: None
    """
    print("Завершение работы.")
    quit()

def сhoosing_method(choice:str)->None:
    """
    Метод обработки выбора в меню пункта
    :param choice: номер пункта в меню
    :return:
    """
    method_dict = {"1": add_book_to_library,
                   "2": del_book,
                   "3": search_for_book,
                   "4": show_all_books,
                   "5": change_status_of_book,
                   "6": exit_library}

    if (method_dict.get((choice))==None):
        print("Нет такого пункта в меню, попробуйте снова.")
    else:
        method_dict[choice]()


def main() -> None:
    """
    Интерфейс программы, который позволяет пользователю взаимодействовать с библиотекой.
    Он отображает меню и вызывает соответствующие методы в зависимости от выбора пользователя.
    """
    while True:
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        choice = input("Выберите действие (1-6): ")
        try:
            сhoosing_method(choice)
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        books = list_books(LIBRARY_FILE)
        save_library(books, LIBRARY_FILE)
        print("Изменения сохранены. Работа завершена.")