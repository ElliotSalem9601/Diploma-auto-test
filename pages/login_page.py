import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    PASSWORD_INPUT = (
        By.CSS_SELECTOR,
        "input[type='password'], input[name='password']",
    )
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    @allure.step("Авторизация с email: {email}")
    def login(self, email: str, password: str) -> "LoginPage":
        """Выполняет авторизацию на сайте."""
        self.input_text(self.EMAIL_INPUT, email)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)
        return self

    @allure.step("Проверка успешной авторизации")
    def is_login_successful(self) -> bool:
        from pages.schedule_page import SchedulePage

        return self.is_element_visible(SchedulePage.ADD_EVENT_BTN)
