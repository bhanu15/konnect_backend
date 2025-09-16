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
        
        # S3 settings
        self.S3_BUCKET = cfg["s3"]["bucket"]
        self.S3_REGION = cfg["s3"]["region"]
        self.S3_ACCESS_KEY = cfg["s3"]["access_key"]
        self.S3_SECRET_KEY = cfg["s3"]["secret_key"]

        
        self.OPENAI_API_KEY = cfg["openai"]["api_key"]
        
        self.ALLOWED_CONTENT_TYPES = cfg.get("allowed_content_types", ["image/jpeg", "image/png", "image/webp"])
        self.MAX_UPLOAD_SIZE_BYTES = cfg.get("max_upload_size_bytes", 10 * 1024 * 1024)
        
        self.ASSISTANT_ID = self._load_yaml("config/assistant.yaml").get("assistant_id")
        self.SYSTEM_PROMPT = self._load_yaml("config/prompt.yaml").get("system_prompt")

    def _load_yaml(self, path: str):
        file_path = Path(path)
        if not file_path.exists():
            return {}
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
        
    def get_prompt(self, key: str = "default_prompt") -> str:
        path = Path("config/prompt.yaml")
        if not path.exists():
            return ""
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        if "prompts" in data:
            return data["prompts"].get(key, "")
        return data.get(key, "")

ENV = os.getenv("ENV", "dev")
settings = Settings(env=ENV)
