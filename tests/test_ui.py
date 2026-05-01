# tests/test_ui.py (исправленная версия)
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage  # ← проверьте, что файл существует
from pages.schedule_page import SchedulePage
from config.settings import settings
import allure

@allure.feature("UI. Личные события в расписании")
class TestUIPersonalEvents:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(settings.IMPLICITLY_WAIT)
        
        # Авторизация
        login_page = LoginPage(self.driver)
        login_page.open(settings.BASE_URL)
        login_page.login(settings.TEACHER_EMAIL, settings.TEACHER_PASSWORD)
        
        self.schedule_page = SchedulePage(self.driver)
        yield
        self.driver.quit()
    
    @allure.title("UI-1: Добавление личного события")
    @allure.story("Создание события")
    @pytest.mark.ui
    def test_create_personal_event(self):
        """Тест 1: Создание личного события"""
        event_title = "Важное совещание"
        event_date = "2025-05-15"
        self.schedule_page.create_event(event_title, event_date)
        assert self.schedule_page.is_event_displayed(event_title)
    
    @allure.title("UI-2: Валидация названия (40 символов)")
    @allure.story("Валидация")
    @pytest.mark.ui
    def test_event_title_validation(self):
        """Тест 2: Проверка ограничения в 40 символов"""
        long_title = "A" * 41
        self.schedule_page.create_event(long_title, "2025-05-16")
        assert self.schedule_page.is_event_not_displayed(long_title)
    
    @allure.title("UI-3: Редактирование события")
    @allure.story("Редактирование")
    @pytest.mark.ui
    def test_edit_event(self):
        """Тест 3: Редактирование названия события"""
        old_title = "Старое название"
        new_title = "Новое название"
        self.schedule_page.create_event(old_title, "2025-05-17")
        assert self.schedule_page.is_event_displayed(old_title)
        # Редактирование
        self.schedule_page.edit_event(old_title, new_title)
        assert self.schedule_page.is_event_displayed(new_title)
    
    @allure.title("UI-4: Удаление события")
    @allure.story("Удаление")
    @pytest.mark.ui
    def test_delete_event(self):
        """Тест 4: Удаление события"""
        event_title = "Событие для удаления"
        self.schedule_page.create_event(event_title, "2025-05-18")
        assert self.schedule_page.is_event_displayed(event_title)
        self.schedule_page.delete_event(event_title)
        assert self.schedule_page.is_event_not_displayed(event_title)
    
    @allure.title("UI-5: Цветовая маркировка события")
    @allure.story("Отображение")
    @pytest.mark.ui
    def test_event_color_marking(self):
        """Тест 5: Выбор цвета события"""
        event_title = "Цветное событие"
        color = "blue"
        self.schedule_page.create_event_with_color(event_title, "2025-05-19", color)
        assert self.schedule_page.get_event_color(event_title) == color
