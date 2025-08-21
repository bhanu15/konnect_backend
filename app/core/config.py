import yaml
from pathlib import Path
import os

class Settings:
    def __init__(self, env: str = "dev"):
        base_config = self._load_yaml("config/base.yaml")
        env_config = self._load_yaml(f"config/{env}.yaml")
        cfg = {**base_config, **env_config}

        self.APP_NAME = cfg.get("app_name")
        self.LOG_LEVEL = cfg.get("log_level", "INFO")
        self.DATABASE_URL = cfg["database_url"]

    def _load_yaml(self, path: str):
        file_path = Path(path)
        if not file_path.exists():
            return {}
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

ENV = os.getenv("ENV", "dev")
settings = Settings(env=ENV)
