# Diploma-auto-test

Автотесты для дипломной работы по функционалу "Личные события" на вкладке
"Расписание" портала преподавателя Skyeng.

## Ссылка на финальный проект по ручному тестированию

[Курсовая работа: Тестирование функционала "Личные события"](https://elliotsalem9601.yonote.ru/share/c5147b1d-c7f2-4428-8bde-53912e961e8b)

## Технологии

- Python 3.9+
- Selenium + Page Object Model
- Requests
- Pytest
- Allure
- Flake8

## Установка

Склонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/ElliotSalem9601/Diploma-auto-test.git
cd Diploma-auto-test
```

Создайте и активируйте виртуальное окружение.

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Переменные окружения

Создайте в корне проекта файл `.env`. Важно: файл должен называться именно
`.env`, без расширений `.ini`, `.txt` и других суффиксов.

Пример заполнения:

```env
API_BASE_URL=https://api-teachers.skyeng.ru
BASE_URL=https://teachers.skyeng.ru/schedule
EMAIL=your_email@example.com
PASSWORD=your_password
API_TOKEN=your_api_token
```

`EMAIL` и `PASSWORD` нужны для UI-тестов. `API_TOKEN` нужен для API-тестов:
он передается и в cookie `token_global`, и в заголовке `Authorization`.

## Запуск тестов

Запустить все тесты:

```bash
pytest
```

Запустить только API-тесты:

```bash
pytest -m api
```

Запустить только UI-тесты:

```bash
pytest -m ui
```

Запустить тесты с сохранением результатов Allure:

```bash
pytest --alluredir=allure-results
```

Сформировать и открыть Allure-отчет:

```bash
allure serve allure-results
```

## Проверка стиля

Запуск flake8:

```bash
flake8
```

## Структура проекта

```text
config/             настройки и загрузка .env
pages/              Page Object Model для UI-тестов
tests/test_api.py   API-тесты личных событий
tests/test_ui.py    UI-тесты личных событий
utils/api_client.py клиент для API-запросов
```
