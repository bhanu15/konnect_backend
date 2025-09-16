import logging
from sqlalchemy.orm import Session
import json
from app.repositories.user_search_query_repository import UserSearchQueryRepository
from app.repositories.answer_repository import AnswerRepository
from app.schemas.user_search_query import UserSearchQueryCreate
from app.schemas.search import SearchResponse
from app.services.assistant_service import assistant_service

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.query_repo = UserSearchQueryRepository(db)
        self.answer_repo = AnswerRepository(db)
        self.assistant_service = assistant_service
        self.client = assistant_service.get_client()
        self.assistant_id = assistant_service.get_assistant_id()

    def search(self, query_in: UserSearchQueryCreate, request ) -> SearchResponse:
        request_id = getattr(request.state, "request_id", None) or "unknown"
        logger.info(f"[RequestID: {request_id}] Processing search for user '{query_in.userEmail}' question: {query_in.searchQuestion}")
        

        # Step 1: Get existing thread for user or create a new one
        existing_queries = self.query_repo.get_by_email(query_in.userEmail)
        thread_id = existing_queries[-1].thread_id if existing_queries else None

        if not thread_id:
            thread_id = self.assistant_service.create_thread()
            logger.info(f"New thread created for user {query_in.userEmail}: {thread_id}")

        # Step 2: Store user query
        query_record = self.query_repo.create(
            search_question=query_in.searchQuestion,
            user_email=query_in.userEmail,
            user_location=query_in.userLocation,
            user_nationality=query_in.userNationality,
            thread_id=None,
        )

        # Step 3: Send user message to assistant
        try:
            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=query_in.searchQuestion,
            )
        except Exception as e:
            logger.error(f"[RequestID: {request_id}] Failed to send message to assistant: {e}")
            raise RuntimeError(f"Failed to send message to assistant: {e}")

        # Step 4: Run assistant
        try:
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
            )
        except Exception as e:
            logger.error(f"[RequestID: {request_id}] Assistant run failed for thread {thread_id}: {e}")
            raise RuntimeError(f"Assistant run failed: {e}")

        if run.status != "completed":
            logger.error(f"Assistant run did not complete. Status: {run.status}")
            raise RuntimeError(f"Assistant run failed: {run.status}")

        # Step 5: Fetch latest assistant message
        try:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            assistant_messages = [m for m in messages.data if m.role == "assistant"]
            if not assistant_messages:
                raise RuntimeError("No assistant messages found in thread")
            answer_text = assistant_messages[-1].content[0].text.value.strip()
        except Exception as e:
            logger.error(f"Failed to retrieve assistant message: {e}")
            raise RuntimeError(f"Failed to retrieve assistant message: {e}")

        # Step 6: Store answer
        answer_record = self.answer_repo.create(query_id=query_record.id, answer_text=answer_text)

        # Step 7: Parse JSON or fallback
        try:
            answer_json = json.loads(answer_record.answer_text)
        except json.JSONDecodeError:
            logger.warning(f"[RequestID: {request_id}] Failed to parse JSON from assistant answer, returning raw text")
            answer_json = {"text": answer_record.answer_text}
        

        # Step 8: Return structured response
        return SearchResponse(
            searchQuestion=query_record.search_question,
            answer=answer_json,
            # Optionally include metadata:
            # userEmail=query_record.user_email,
            # userLocation=query_record.user_location,
            # userNationality=query_record.user_nationality,
            # createdAt=query_record.created_at,
            # threadId=query_record.thread_id,
        )
