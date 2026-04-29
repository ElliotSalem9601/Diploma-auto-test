from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webriver import WebDriver
from selenium.common.exceptions import TimeoutException
import allure

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # EXPLICITLY_WAIT

    @allure.step("Открыть страницу {url}")
    def open(self, url: str):
        self.driver.get(url)
    
    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator: tuple):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    @allure.step("Ввести текст '{text}' в поле {locator}")
    def input_text(self, locator: tuple, text: str):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текст из элемента {locator}")
    def get_text(self, locator: tuple) -> str:
        return self.find_element(locator).text
    
    @allure.step("Проверить, виден ли элемент {locator}")
    def is_element_visible(self, locator: tuple) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False