import allure
import requests

from config.settings import settings


class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.cookies = {}
        self.headers = {
            "Content-Type": "application/json",
        }

        if settings.API_TOKEN:
            self.cookies["token_global"] = settings.API_TOKEN
            self.headers["Authorization"] = f"Bearer {settings.API_TOKEN}"

        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        self.session.headers.update(self.headers)

    def _post(self, endpoint: str, payload: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=payload)

    @allure.step("API: Создать личное событие")
    def create_event(self, data: dict) -> requests.Response:
        """POST /v2/schedule/createPersonal - создание события."""
        payload = {
            "backgroundColor": data.get("backgroundColor", "#FFF7C7"),
            "color": data.get("color", "#FAC641"),
            "description": data.get("description", ""),
            "title": data["title"],
            "startAt": data["startAt"],
            "endAt": data["endAt"],
        }
        return self._post("/v2/schedule/createPersonal", payload)

    @allure.step("API: Получить события за период")
    def get_events(self, from_date: str, till_date: str) -> requests.Response:
        """POST /v2/schedule/events - получение списка событий."""
        payload = {
            "from": from_date,
            "till": till_date,
            "onlyTypes": [],
        }
        return self._post("/v2/schedule/events", payload)

    @allure.step("API: Обновить событие")
    def update_event(
        self,
        event_id: str,
        old_start_at: str,
        data: dict,
    ) -> requests.Response:
        """POST /v2/schedule/updatePersonal - обновление события."""
        payload = {
            "id": event_id,
            "oldStartAt": old_start_at,
            **data,
        }
        return self._post("/v2/schedule/updatePersonal", payload)

    @allure.step("API: Удалить событие")
    def delete_event(self, event_id: str, start_at: str) -> requests.Response:
        """POST /v2/schedule/removePersonal - удаление события."""
        payload = {
            "id": event_id,
            "startAt": start_at,
        }
        return self._post("/v2/schedule/removePersonal", payload)
