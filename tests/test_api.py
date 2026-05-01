import pytest
import random
from datetime import datetime, timedelta
import allure
from utils.api_client import APIClient

def generate_event_data(days_offset: int = 5) -> dict:
    """Генератор тестовых данных для событий"""
    event_date = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    return {
        "title": f"API Тест {random.randint(1, 999)}",
        "date": event_date,
        "duration_minutes": 60,
        "description": f"Автоматический тест {datetime.now()}"
    }

@allure.feature("API. Личные события")
class TestAPIPersonalEvents:
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @allure.title("API-1: Создание события в будущем")
    @allure.story("Создание")
    @pytest.mark.api
    def test_create_future_event(self, api_client):
        """Позитивный тест: создание события на будущую дату"""
        event_data = generate_event_data(days_offset=5)
        response = api_client.create_event(event_data)
        assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
        assert "id" in response.json(), "Ответ не содержит ID события"
    
    @allure.title("API-2: Создание события в прошлом")
    @allure.story("Создание")
    @pytest.mark.api
    def test_create_past_event(self, api_client):
        """Проверка потребности Анастасии Петровны: добавление событий задним числом"""
        past_event_data = generate_event_data(days_offset=-10)
        response = api_client.create_event(past_event_data)
        assert response.status_code == 201, "API должен создать прошлые события"
    
    @allure.title("API-3: Негативный тест - невалидная длительность (>9ч 40м)")
    @allure.story("Валидация")
    @pytest.mark.api
    def test_create_event_invalid_duration(self, api_client):
        """Негативный тест: длительность 10 часов (превышает лимит 9ч 40м)"""
        event_data = generate_event_data()
        event_data["duration_minutes"] = 600  # 10 часов
        response = api_client.create_event(event_data)
        assert response.status_code == 400, "API должен вернуть 400 на невалидную длительность"
    
    @allure.title("API-4: Редактирование события")
    @allure.story("Редактирование")
    @pytest.mark.api
    def test_update_event(self, api_client):
        """Тест редактирования названия события"""
        # Создаем событие
        event_data = generate_event_data()
        create_response = api_client.create_event(event_data)
        assert create_response.status_code == 201
        event_id = create_response.json()["id"]
        
        # Обновляем событие
        updated_data = {"title": "Обновленное API название"}
        update_response = api_client.update_event(event_id, updated_data)
        assert update_response.status_code == 200, "Не удалось обновить событие"
    
    @allure.title("API-5: Получение списка событий за дату")
    @allure.story("Получение данных")
    @pytest.mark.api
    def test_get_events_by_date(self, api_client):
        """Позитивный тест: получение расписания на конкретную дату"""
        test_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = api_client.get_events_by_date(test_date)
        assert response.status_code == 200, "Не удалось получить расписание"
        assert isinstance(response.json(), list), "Ответ должен быть списком событий"
