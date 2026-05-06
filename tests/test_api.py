from datetime import datetime, timedelta, timezone
from typing import Optional

import allure
import pytest

from config.settings import settings
from utils.api_client import APIClient


def format_date(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%S+03:00")


MSK = timezone(timedelta(hours=3))


def generate_event_data(days_offset: int = 5, title: Optional[str] = None) -> dict:
    """Генератор тестовых данных для личного события."""
    start_at = (datetime.now(MSK) + timedelta(days=days_offset)).replace(
        hour=10,
        minute=0,
        second=0,
        microsecond=0,
    )
    end_at = start_at + timedelta(hours=1)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    event_title = title if title is not None else f"API Test {timestamp}"

    return {
        "title": event_title,
        "startAt": format_date(start_at),
        "endAt": format_date(end_at),
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "description": f"Автоматический API-тест {timestamp}",
    }


def assert_success_response(response):
    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("errors") in (None, [])
    return json_data


def get_payload(response):
    json_data = assert_success_response(response)
    data = json_data.get("data", {})
    return data.get("payload", data)


def get_payload_without_status_check(response):
    json_data = response.json()
    data = json_data.get("data", {})
    return data.get("payload", data)


def get_event_id(response) -> str:
    payload = get_payload(response)
    event_id = payload.get("id")
    assert event_id, "В ответе создания события нет id"
    return event_id


def collect_events(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("events", "items", "payload"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


@allure.feature("API. Личные события")
@pytest.mark.api
class TestAPIPersonalEvents:
    @pytest.fixture
    def api_client(self):
        if not settings.has_api_token:
            pytest.skip("Для API-тестов нужен API_TOKEN в файле .env")
        return APIClient()

    @pytest.fixture
    def created_event_ids(self, api_client):
        event_ids = []
        yield event_ids
        for event_id, start_at in event_ids:
            api_client.delete_event(event_id, start_at)

    @allure.title("API-1: Создание личного события в будущем")
    def test_create_future_event(self, api_client, created_event_ids):
        event_data = generate_event_data(days_offset=5)
        response = api_client.create_event(event_data)

        event_id = get_event_id(response)
        created_event_ids.append((event_id, event_data["startAt"]))

    @allure.title("API-2: Получение созданного события в расписании")
    def test_get_events_contains_created_event(self, api_client, created_event_ids):
        event_data = generate_event_data(days_offset=6)
        create_response = api_client.create_event(event_data)
        event_id = get_event_id(create_response)
        created_event_ids.append((event_id, event_data["startAt"]))

        response = api_client.get_events(event_data["startAt"], event_data["endAt"])
        events = collect_events(get_payload(response))

        assert any(str(event.get("id")) == str(event_id) for event in events)

    @allure.title("API-3: Редактирование названия личного события")
    def test_update_event_title(self, api_client, created_event_ids):
        event_data = generate_event_data(days_offset=7)
        create_response = api_client.create_event(event_data)
        event_id = get_event_id(create_response)
        created_event_ids.append((event_id, event_data["startAt"]))

        updated_data = {
            **event_data,
            "title": f"{event_data['title']} updated",
        }
        response = api_client.update_event(
            event_id,
            event_data["startAt"],
            updated_data,
        )

        assert_success_response(response)

    @allure.title("API-4: Удаление личного события")
    def test_delete_event(self, api_client):
        event_data = generate_event_data(days_offset=8)
        create_response = api_client.create_event(event_data)
        event_id = get_event_id(create_response)

        response = api_client.delete_event(event_id, event_data["startAt"])

        assert_success_response(response)

    @allure.title("API-5: Нельзя создать событие без названия")
    def test_create_event_without_title_returns_error(self, api_client):
        event_data = generate_event_data(days_offset=9, title="")
        response = api_client.create_event(event_data)
        json_data = response.json()

        assert response.status_code in (200, 400, 422)
        payload = get_payload_without_status_check(response)

        assert json_data.get("errors") or not payload.get("id")
