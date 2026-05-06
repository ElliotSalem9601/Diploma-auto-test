import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.settings import settings
from pages.login_page import LoginPage
from pages.schedule_page import SchedulePage


@allure.feature("UI. Личные события в расписании")
@pytest.mark.ui
class TestUIPersonalEvents:
    @pytest.fixture(autouse=True)
    def setup(self):
        if not settings.has_ui_credentials:
            pytest.skip("Для UI-тестов нужны EMAIL и PASSWORD в файле .env")

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(settings.IMPLICITLY_WAIT)

        login_page = LoginPage(self.driver)
        login_page.open(settings.BASE_URL)
        login_page.login(settings.TEACHER_EMAIL, settings.TEACHER_PASSWORD)

        self.schedule_page = SchedulePage(self.driver)
        yield
        self.driver.quit()

    @allure.title("UI-1: Добавление личного события")
    @allure.story("Создание события")
    def test_create_personal_event(self):
        event_title = "Важное совещание"
        event_date = "2026-05-15"
        self.schedule_page.create_event(event_title, event_date)
        assert self.schedule_page.is_event_displayed(event_title)

    @allure.title("UI-2: Валидация названия (40 символов)")
    @allure.story("Валидация")
    def test_event_title_validation(self):
        long_title = "A" * 41
        self.schedule_page.create_event(long_title, "2026-05-16")
        assert self.schedule_page.is_event_not_displayed(long_title)

    @allure.title("UI-3: Редактирование события")
    @allure.story("Редактирование")
    def test_edit_event(self):
        old_title = "Старое название"
        new_title = "Новое название"
        self.schedule_page.create_event(old_title, "2026-05-17")
        assert self.schedule_page.is_event_displayed(old_title)

        self.schedule_page.edit_event(old_title, new_title)

        assert self.schedule_page.is_event_displayed(new_title)

    @allure.title("UI-4: Удаление события")
    @allure.story("Удаление")
    def test_delete_event(self):
        event_title = "Событие для удаления"
        self.schedule_page.create_event(event_title, "2026-05-18")
        assert self.schedule_page.is_event_displayed(event_title)

        self.schedule_page.delete_event(event_title)

        assert self.schedule_page.is_event_not_displayed(event_title)

    @allure.title("UI-5: Цветовая маркировка события")
    @allure.story("Отображение")
    def test_event_color_marking(self):
        event_title = "Цветное событие"
        color = "blue"
        self.schedule_page.create_event_with_color(event_title, "2026-05-19", color)
        assert self.schedule_page.get_event_color(event_title)
