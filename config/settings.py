import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api-teachers.skyeng.ru")
    BASE_URL = os.getenv("BASE_URL", "https://teachers.skyeng.ru/schedule")
    
    # Учетные данные
    TEACHER_EMAIL = os.getenv("EMAIL")
    TEACHER_PASSWORD = os.getenv("PASSWORD")
    API_TOKEN = os.getenv("API_TOKEN")
    
    # Настройки ожиданий
    IMPLICITLY_WAIT = 10
    EXPLICITLY_WAIT = 15

settings = Settings()
