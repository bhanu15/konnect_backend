import logging
import httpx
import yaml
from pathlib import Path
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

class AssistantService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return

        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set in env or config")

        self.http_client = httpx.Client(follow_redirects=True, timeout=30.0)
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY, http_client=self.http_client)
        self.assistant_id = settings.ASSISTANT_ID
        self.system_prompt = settings.SYSTEM_PROMPT
        self._initialized = True
        logger.info(f"AssistantService initialized with assistant_id={self.assistant_id}")

    def get_client(self): 
        return self.client

    def get_assistant_id(self): 
        if not self.assistant_id:
            raise RuntimeError("Assistant ID not set. Call create_assistant() first.")
        return self.assistant_id

    def get_system_prompt(self): 
        return self.system_prompt

    def create_thread(self):
        thread = self.client.beta.threads.create()
        logger.info(f"Created new thread: {thread.id}")
        return thread.id

    def create_assistant(self, name="DefaultAssistant", description="Default assistant"):
        if self.assistant_id:
            logger.info("Assistant already exists, skipping creation.")
            return self.assistant_id
        try:
            resp = self.client.assistants.create(name=name, description=description)
            new_id = resp.id
            path = Path("config/assistant.yaml")
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                yaml.safe_dump({"assistant_id": new_id}, f)
            self.assistant_id = new_id
            logger.info(f"Created new assistant with ID: {new_id}")
            return new_id
        except Exception as e:
            logger.exception("Failed to create assistant")
            raise RuntimeError(f"Failed to create assistant: {e}")

assistant_service = AssistantService()
