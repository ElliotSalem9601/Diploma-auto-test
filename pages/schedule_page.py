from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

class SchedulePage(BasePage):
    # Локаторы (примеры, вам нужно будет уточнить реальные селекторы)
    ADD_EVENT_BTN = (By.CSS_SELECTOR, "button[data-testid='add-event']")
    EVENT_TITLE_INPUT = (By.CSS_SELECTOR, "input[name='title']")
    EVENT_DATE_INPUT = (By.CSS_SELECTOR, "input[name='date']")
    SAVE_EVENT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    DELETE_EVENT_BTN = (By.CSS_SELECTOR, "button[data-testid='delete-event']")
    CONFIRM_DELETE_BTN = (By.CSS_SELECTOR, "button.confirm-delete")
    
    # Динамический локатор для поиска события по названию
    @staticmethod
    def get_event_by_title(title: str) -> tuple:
        return (By.XPATH, f"//div[contains(@class, 'event-item') and contains(text(), '{title}')]")
    
    @allure.step("Создать личное событие: название='{title}', дата='{date}'")
    def create_event(self, title: str, date: str):
        self.click(self.ADD_EVENT_BTN)
        self.input_text(self.EVENT_TITLE_INPUT, title)
        self.input_text(self.EVENT_DATE_INPUT, date)
        self.click(self.SAVE_EVENT_BTN)
        return self
    
    @allure.step("Попытаться создать событие с названием длиннее 40 символов")
    def try_create_event_long_title(self, long_title: str):
        self.click(self.ADD_EVENT_BTN)
        self.input_text(self.EVENT_TITLE_INPUT, long_title)
        self.click(self.SAVE_EVENT_BTN)
        # Здесь можно вернуть текст ошибки, если она появляется
        # return self.get_error_message()
    
    @allure.step("Удалить событие с названием '{title}'")
    def delete_event(self, title: str):
        event_locator = self.get_event_by_title(title)
        # Наводимся на событие, чтобы появилась кнопка удаления (пример)
        self.find_element(event_locator).click()
        self.click(self.DELETE_EVENT_BTN)
        self.click(self.CONFIRM_DELETE_BTN)
    
    @allure.step("Проверить, что событие с названием '{title}' отображается")
    def is_event_displayed(self, title: str) -> bool:
        return self.is_element_visible(self.get_event_by_title(title))
    
    @allure.step("Проверить, что событие с названием '{title}' НЕ отображается")
    def is_event_not_displayed(self, title: str) -> bool:
        return not self.is_element_visible(self.get_event_by_title(title))