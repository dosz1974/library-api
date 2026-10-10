# Library Books API

Лабораторная работа №4 — API для библиотеки книг.

## Технологии
Python, FastAPI, Uvicorn, Pydantic, pytest.

## Установка
```bash
pip install -r requirements.txt
```

## Запуск сервера
```bash
python -m uvicorn main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

## Эндпоинты
| Метод | Адрес | Описание |
|---|---|---|
| GET | /books | Список всех книг |
| GET | /books/{book_id} | Книга по ID |
| POST | /books | Добавление книги |
| PUT | /books/{book_id} | Обновление книги |
| DELETE | /books/{book_id} | Удаление книги |

## Пример JSON
```json
{
  "title": "1984",
  "author": "George Orwell",
  "year": 1949
}
```

ID назначается автоматически.

## Обработка ошибок
404 — книга не найдена.
422 — некорректные входные данные.

## Тестирование
```bash
python -m pytest -v
```

Результаты тестирования сохраняются в test_results.txt.

## Хранение данных
Книги хранятся в списке Python.
После перезапуска сервера данные очищаются.
