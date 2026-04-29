import requests
import allure
from config.settings import settings

class APIClient:
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.API_TOKEN}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    @allure.step("API: Создать событие с данными {data}")
    def create_event(self, data: dict) -> requests.Response:
        response = self.session.post(f"{self.base_url}/api/events", json=data)
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.JSON)
        return response
    
    @allure.step("API: Получить список событий за дату {date}")
    def get_events_by_date(self, date: str) -> requests.Response:
        response = self.session.get(f"{self.base_url}/api/schedule", params={"date": date})
        return response
    
    @allure.step("API: Обновить событие {event_id} с данными {data}")
    def update_event(self, event_id: str, data: dict) -> requests.Response:
        response = self.session.put(f"{self.base_url}/api/events/{event_id}", json=data)
        return response
    
    @allure.step("API: Удалить событие {event_id}")
    def delete_event(self, event_id: str) -> requests.Response:
        response = self.session.delete(f"{self.base_url}/api/events/{event_id}")
        return response