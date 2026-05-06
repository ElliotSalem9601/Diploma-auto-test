import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


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

    @property
    def has_ui_credentials(self) -> bool:
        return bool(self.TEACHER_EMAIL and self.TEACHER_PASSWORD)

    @property
    def has_api_token(self) -> bool:
        return bool(self.API_TOKEN)


settings = Settings()
