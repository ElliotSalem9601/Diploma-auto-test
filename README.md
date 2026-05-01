# Diploma-auto-test

Автотесты для дипломной работы

## Ссылка на финальный проект по ручному тестированию

[Курсовая работа: Тестирование функционала "Личные события" в расписании](https://elliotsalem9601.yonote.ru/share/c5147b1d-c7f2-4428-8bde-53912e961e8b)

---

## Описание проекта

Проект содержит автоматизированные тесты для проверки функционала **"Личные события"** на вкладке "Расписание" портала преподавателя Skyeng.

**Что автоматизировано:**
- **5 UI тестов** (Selenium WebDriver + Page Object Model)
- **5 API тестов** (Requests)

---

## Технологии

| Технология | Версия | Назначение |
|------------|--------|-------------|
| Python | 3.9+ | Язык программирования |
| Selenium | 4.15.0 | Автоматизация браузера |
| Requests | 2.31.0 | HTTP-запросы для API |
| Pytest | 7.4.3 | Фреймворк тестирования |
| Allure | 2.13.2 | Генерация отчетов |
| Page Object Model | - | Паттерн для UI тестов |

---

## Структура проекта
Diploma-auto-test/
├── .env.example # Шаблон переменных окружения
├── .gitignore # Игнорируемые файлы
├── pytest.ini # Настройки pytest (маркеры)
├── requirements.txt # Зависимости
├── README.md # Документация
│
├── config/
│ ├── init.py
│ └── settings.py # Настройки из .env
│
├── pages/ # Page Object Model
│ ├── init.py
│ ├── base_page.py # Базовый класс
│ ├── login_page.py # Страница логина
│ └── schedule_page.py # Страница расписания
│
├── tests/
│ ├── init.py
│ ├── test_ui.py # UI тесты (5 шт.)
│ └── test_api.py # API тесты (5 шт.)
│
└── utils/
├── init.py
└── api_client.py # Клиент для API

---

## Подготовка к работе

### 1. Клонирование репозитория

```bash
git clone https://github.com/ElliotSalem9601/Diploma-auto-test.git
cd Diploma-auto-test
