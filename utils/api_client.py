import requests
import allure
from config.settings import settings

class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.cookies = {
            "token_global": settings.API_TOKEN
        }
        self.headers = {
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        self.session.headers.update(self.headers)
    
    @allure.step("API: Создать личное событие")
    def create_event(self, data: dict) -> requests.Response:
        """POST /v2/schedule/createPersonal - создание события"""
        url = f"{self.base_url}/v2/schedule/createPersonal"
        
        
        payload = {
            "backgroundColor": data.get("backgroundColor", "#FFF7C7"),
            "color": data.get("color", "#FAC641"),
            "description": data.get("description", ""),
            "title": data["title"],
            "startAt": data["startAt"],
            "endAt": data["endAt"]
        }
        
        response = self.session.post(url, json=payload)
        return response
    
    @allure.step("API: Получить события за период")
    def get_events(self, from_date: str, till_date: str) -> requests.Response:
        """POST /v2/schedule/events - получение списка событий"""
        url = f"{self.base_url}/v2/schedule/events"
        payload = {
            "from": from_date,
            "till": till_date,
            "onlyTypes": []
        }
        response = self.session.post(url, json=payload)
        return response
    
    @allure.step("API: Обновить событие")
    def update_event(self, event_id: str, old_start_at: str, data: dict) -> requests.Response:
        """POST /v2/schedule/updatePersonal - обновление события"""
        url = f"{self.base_url}/v2/schedule/updatePersonal"
        payload = {
            "id": event_id,
            "oldStartAt": old_start_at,
            **data
        }
        response = self.session.post(url, json=payload)
        return response
    
    @allure.step("API: Удалить событие")
    def delete_event(self, event_id: str, start_at: str) -> requests.Response:
        """POST /v2/schedule/removePersonal - удаление события"""
        url = f"{self.base_url}/v2/schedule/removePersonal"
        payload = {
            "id": event_id,
            "startAt": start_at
        }
        response = self.session.post(url, json=payload)
        return response
