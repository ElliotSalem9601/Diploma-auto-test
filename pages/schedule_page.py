import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SchedulePage(BasePage):
    ADD_EVENT_BTN = (
        By.XPATH,
        "//button[contains(., 'Добавить') or contains(., 'Создать')"
        " or @data-testid='add-event']",
    )
    PERSONAL_EVENT_ITEM = (
        By.XPATH,
        "//*[self::button or self::div][contains(., 'Личное событие')]",
    )
    EVENT_TITLE_INPUT = (
        By.CSS_SELECTOR,
        "input[name='title'], input[placeholder*='Название'], textarea[name='title']",
    )
    EVENT_DATE_INPUT = (
        By.CSS_SELECTOR,
        "input[name='date'], input[placeholder*='Дата'], input[type='date']",
    )
    SAVE_EVENT_BTN = (
        By.XPATH,
        "//button[@type='submit' or contains(., 'Сохранить') or contains(., 'Создать')]",
    )
    DELETE_EVENT_BTN = (
        By.XPATH,
        "//button[contains(., 'Удалить') or @data-testid='delete-event']",
    )
    CONFIRM_DELETE_BTN = (
        By.XPATH,
        "//button[contains(., 'Удалить') or contains(., 'Да')]",
    )
    EDIT_EVENT_BTN = (
        By.XPATH,
        "//button[contains(., 'Редактировать') or @data-testid='edit-event']",
    )
    COLOR_BTN = (
        By.CSS_SELECTOR,
        "button[data-testid='color-picker'], button[aria-label*='цвет']",
    )

    @staticmethod
    def get_event_by_title(title: str) -> tuple:
        return (
            By.XPATH,
            "//*[contains(@class, 'event') or contains(@class, 'Event')]"
            f"[contains(., '{title}')]",
        )

    def open_personal_event_form(self):
        self.click(self.ADD_EVENT_BTN)
        if self.is_element_visible(self.PERSONAL_EVENT_ITEM):
            self.click(self.PERSONAL_EVENT_ITEM)
        return self

    @allure.step("Создать личное событие: название='{title}', дата='{date}'")
    def create_event(self, title: str, date: str):
        self.open_personal_event_form()
        self.input_text(self.EVENT_TITLE_INPUT, title)
        self.input_text(self.EVENT_DATE_INPUT, date)
        self.click(self.SAVE_EVENT_BTN)
        return self

    @allure.step("Создать событие с цветом: '{title}', '{color}'")
    def create_event_with_color(self, title: str, date: str, color: str):
        self.open_personal_event_form()
        self.input_text(self.EVENT_TITLE_INPUT, title)
        self.input_text(self.EVENT_DATE_INPUT, date)
        self.click(self.COLOR_BTN)
        color_selector = (By.CSS_SELECTOR, f"div[data-color='{color}']")
        self.click(color_selector)
        self.click(self.SAVE_EVENT_BTN)
        return self

    @allure.step("Редактировать событие '{old_title}' на '{new_title}'")
    def edit_event(self, old_title: str, new_title: str):
        event_locator = self.get_event_by_title(old_title)
        self.find_element(event_locator).click()
        self.click(self.EDIT_EVENT_BTN)
        self.input_text(self.EVENT_TITLE_INPUT, new_title)
        self.click(self.SAVE_EVENT_BTN)
        return self

    @allure.step("Удалить событие с названием '{title}'")
    def delete_event(self, title: str):
        event_locator = self.get_event_by_title(title)
        self.find_element(event_locator).click()
        self.click(self.DELETE_EVENT_BTN)
        self.click(self.CONFIRM_DELETE_BTN)
        return self

    @allure.step("Получить цвет события '{title}'")
    def get_event_color(self, title: str) -> str:
        event = self.find_element(self.get_event_by_title(title))
        return event.value_of_css_property("background-color")

    @allure.step("Проверить, что событие '{title}' отображается")
    def is_event_displayed(self, title: str) -> bool:
        return self.is_element_visible(self.get_event_by_title(title))

    @allure.step("Проверить, что событие '{title}' НЕ отображается")
    def is_event_not_displayed(self, title: str) -> bool:
        return not self.is_element_visible(self.get_event_by_title(title))
