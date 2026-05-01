from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure

class SchedulePage(BasePage):
    # Локаторы
    ADD_EVENT_BTN = (By.CSS_SELECTOR, "button[data-testid='add-event']")
    EVENT_TITLE_INPUT = (By.CSS_SELECTOR, "input[name='title']")
    EVENT_DATE_INPUT = (By.CSS_SELECTOR, "input[name='date']")
    SAVE_EVENT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    DELETE_EVENT_BTN = (By.CSS_SELECTOR, "button[data-testid='delete-event']")
    CONFIRM_DELETE_BTN = (By.CSS_SELECTOR, "button.confirm-delete")
    EDIT_EVENT_BTN = (By.CSS_SELECTOR, "button[data-testid='edit-event']")
    COLOR_BTN = (By.CSS_SELECTOR, "button[data-testid='color-picker']")
    
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
    
    @allure.step("Создать событие с цветом: '{title}', '{color}'")
    def create_event_with_color(self, title: str, date: str, color: str):
        self.click(self.ADD_EVENT_BTN)
        self.input_text(self.EVENT_TITLE_INPUT, title)
        self.input_text(self.EVENT_DATE_INPUT, date)
        self.click(self.COLOR_BTN)
        color_selector = (By.CSS_SELECTOR, f"div[data-color='{color}']")
        self.click(color_selector)
        self.click(self.SAVE_EVENT_BTN)
        return self
    
    @allure.step("Редактировать событие '{old_title}' → '{new_title}'")
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
