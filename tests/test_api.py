import pytest
import allure
from utils.api_client import APIClient
from utils.helpers import generate_event_data

@allure.feature("API. Личные события")
class TestAPIPersonalEvents:
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @allure.title("API-1: Создание события в будущем (позитивный тест)")
    @allure.story("Создание")
    @pytest.mark.api
    def test_create_future_event(self, api_client):
        event_data = generate_event_data(days_from_now=5)  # через 5 дней
        response = api_client.create_event(event_data)
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        assert "id" in response.json(), "В ответе нет id созданного события"
    
    @allure.title("API-2: Создание события в прошлом (потребность Анастасии Петровны)")
    @allure.story("Создание")
    @pytest.mark.api
    def test_create_past_event(self, api_client):
        past_event_data = generate_event_data(days_from_now=-10)  # 10 дней назад
        response = api_client.create_event(past_event_data)
        # Согласно вашему отчету, API позволяет создавать события в прошлом
        assert response.status_code == 201, "API должен允许创建 прошлые события"
    
    @allure.title("API-3: Создание события с невалидной длительностью (негативный тест)")
    @allure.story("Валидация")
    @pytest.mark.api
    def test_create_event_invalid_duration(self, api_client):
        event_data = generate_event_data(duration_hours=10)  # 10 часов (макс 9ч 40м)
        response = api_client.create_event(event_data)
        # Ожидаем ошибку валидации
        assert response.status_code == 400, "API должен вернуть 400 на невалидную длительность"
        assert "длительность" in response.text.lower(), "В сообщении об ошибке должно быть указано поле 'длительность'"
    
    @allure.title("API-4: Редактирование события")
    @allure.story("Редактирование")
    @pytest.mark.api
    def test_update_event(self, api_client):
        # Сначала создаем событие
        event_data = generate_event_data()
        create_resp = api_client.create_event(event_data)
        event_id = create_resp.json()["id"]
        
        # Обновляем событие (меняем название)
        updated_data = {"title": "Обновленное название события"}
        update_resp = api_client.update_event(event_id, updated_data)
        assert update_resp.status_code == 200, "Не удалось обновить событие"
        
        # Проверяем, что данные обновились (нужен GET запрос)
        get_resp = api_client.get_events_by_date(event_data["date"])
        titles = [event["title"] for event in get_resp.json()]
        assert "Обновленное название события" in titles, "Название не обновилось в системе"
    
    @allure.title("API-5: Получение списка событий за конкретную дату")
    @allure.story("Получение данных")
    @pytest.mark.api
    def test_get_events_by_date(self, api_client):
        test_date = "2025-05-20"
        response = api_client.get_events_by_date(test_date)
        assert response.status_code == 200, "Не удалось получить расписание"
        events = response.json()
        assert isinstance(events, list), "Ответ должен быть списком событий"
        # Дополнительно: можно проверить, что все события в ответе имеют нужную дату
        for event in events:
            assert event.get("date") == test_date, f"Событие {event.get('id')} имеет другую дату"