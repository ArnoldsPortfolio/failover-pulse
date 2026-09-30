from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_secret: str = "failover-pulse-dev"
    database_url: str = "sqlite:///./failover_pulse.db"
    fail_threshold: int = 3
    recover_threshold: int = 2
