import pytest
from datetime import datetime, timedelta
import allure
from utils.api_client import APIClient

def generate_event_data(days_offset: int = 5):
    """Генератор тестовых данных для событий в правильном формате"""
    start_at = (datetime.now() + timedelta(days=days_offset)).replace(
        hour=10, minute=0, second=0, microsecond=0
    )
    end_at = start_at + timedelta(hours=1)
    
    start_at_str = start_at.strftime("%Y-%m-%dT%H:%M:%S+03:00")
    end_at_str = end_at.strftime("%Y-%m-%dT%H:%M:%S+03:00")
    
    return {
        "title": f"API Тест {datetime.now().timestamp()}",
        "startAt": start_at_str,
        "endAt": end_at_str,
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "description": f"Автоматический тест {datetime.now()}"
    }

@allure.feature("API. Личные события")
class TestAPIPersonalEvents:
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @allure.title("API-1: Создание события в будущем")
    @pytest.mark.api
    def test_create_future_event(self, api_client):
        """Позитивный тест: создание события на будущую дату"""
        event_data = generate_event_data(days_offset=5)
        response = api_client.create_event(event_data)
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data.get("errors") is None
        assert "id" in json_data.get("data", {}).get("payload", {})
