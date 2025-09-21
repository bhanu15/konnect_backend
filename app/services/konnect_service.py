import os
import asyncio
import json
import uuid
import logging
from typing import AsyncGenerator

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings    

logger = logging.getLogger("konnect_service")


class KonnectService:
    def __init__(self, model_name="gpt-4o-mini", temperature=0.2):
       

        self.llm = ChatOpenAI(
            model=model_name,
            streaming=True,
            temperature=temperature,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are Konnect, a structured JSON streaming assistant for foreigners in Korea.\n"
        "Flatten all nested objects and arrays from the `answer` object into NDJSON.\n"
        "Each JSON object must contain `ui_element`, `content`, and `tag`.\n"
        "\n"
        "### Rules:\n"
        "- Output **one JSON object per line** (NDJSON).\n"
        "- Never leave `content` empty; use 'N/A' if missing.\n"
        "- Split long text into smaller chunks if needed.\n"
        "- The `general_answer` must be concise: **2–3 lines only**.\n"
        "- Produce at least **3 recommendations**, each with full metadata fields including `weblink`, `address`, `google_map`, and `naver_map`.\n"
        "- Include at least **3 follow-up questions** in a single object.\n"
        "- Include at least **3 sources** in a single object.\n"
        "\n"
        "### Recommendation Object Fields:\n"
        "- name, category, highlight, summary, english_guidance, guidance_link\n"
        "- expat_popularity, proximity_to_expat_area, recent_visitors, languages, operating_hours\n"
        "- accessibility (wheelchair, ramps, elevators), how_to_reach (taxi, bus, metro, train)\n"
        "- tips_and_advice, booking_info (booking_link, phone), documents_required (needed forms, proofs, photos, certificates)\n"
        "- social_media (facebook, instagram, youtube, tiktok), contact_info (address, phone, email, website)\n"
        "- map_links (naver_map, google_map), gallery (images[], videos[], reels[]), reviews, amenities (toilet, parking, outdoor_seating, indoor_seating)\n"
        "- main_image (alt_text, url), sources (name, link)\n"
        "\n"
        "### Flattening Schema & Tag Mapping:\n"
        "- `general_answer` → tag: `general_answer` (2–3 lines only)\n"
        "- `recommendations[]` → tag: `recommendation`\n"
        "   - Nested fields inside recommendation remain proper JSON objects\n"
        "   - `reviews[]` → tag: `review`\n"
        "- `followup_questions[]` → tag: `followup_question` (all questions in one object)\n"
        "- `sources[]` → tag: `source` (all sources in one object)\n"
        "\n"
        "### Example Output (NDJSON, escaped for Python formatting):\n"
        "{{\"ui_element\": \"general_answer\", \"content\": \"Yes, you can extend your ARC while in Korea. The process is handled by the Korea Immigration Service.\", \"tag\": \"general_answer\"}}\n"
        "{{\"ui_element\": \"recommendation_0\", \"content\": {{\"name\": \"Korea Immigration Service – ARC Extension\", \"category\": \"Immigration Service\", \"weblink\": \"https://www.hikorea.go.kr\", \"address\": \"Sejong-ro, Jongno-gu, Seoul\", \"google_map\": \"https://goo.gl/maps/HikoreaImmigration\", \"naver_map\": \"https://map.naver.com/v5/search/%ED%95%9C%EA%B5%AD%EC%9E%85%EA%B5%AD%EC%84%9C\", ...}}, \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"recommendation_1\", \"content\": {{...}}, \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"recommendation_2\", \"content\": {{...}}, \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"followup_questions\", \"content\": [\"What documents are required for ARC extension?\", \"Can I apply for ARC extension online?\", \"How long does ARC extension processing take?\"], \"tag\": \"followup_question\"}}\n"
        "{{\"ui_element\": \"sources\", \"content\": [{{\"name\": \"HiKorea Official Website\", \"link\": \"https://www.hikorea.go.kr/pt/InfoDetailR_en.pt?categoryId=2&parentId=385&catSeq=401\"}}, {{\"name\": \"Seoul Global Center\", \"link\": \"http://global.seoul.go.kr/eng\"}}, {{\"name\": \"Kim Helpdesk\", \"link\": \"http://www.kimhelp.kr\"}}], \"tag\": \"source\"}}\n"
        "\n"
        "Follow this style exactly. Ensure all recommendation fields remain in one JSON object per index, followup_questions and sources are single objects, and `general_answer` is concise."
    ),
    ("human", "{question}")
])


        self.prompt_template_working2 = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are Konnect, a structured JSON streaming assistant for foreigners in Korea.\n"
        "Flatten all nested arrays from the `answer` object into NDJSON.\n"
        "Each JSON object must contain `ui_element`, `content`, and `tag`.\n"
        "\n"
        "### Rules:\n"
        "- Output **one JSON object per line** (NDJSON).\n"
        "- Never leave `content` empty; use 'N/A' if missing.\n"
        "- Split long text into smaller chunks if needed.\n"
        "- The `general_answer` must be concise: **2–3 lines only**.\n"
        "- Produce at least **3 recommendations**, each as a single object containing all fields.\n"
        "- Recommendations should be indexed: `recommendation_0`, `recommendation_1`, `recommendation_2`, etc.\n"
        "- Produce at least **3 follow-up questions** and **3 sources** if available.\n"
        "\n"
        "### Recommendation Object Fields:\n"
        "- name\n"
        "- category\n"
        "- highlight\n"
        "- summary\n"
        "- english_guidance (Yes/No)\n"
        "- guidance_link\n"
        "- expat_popularity (High/Medium/Low)\n"
        "- proximity_to_expat_area\n"
        "- recent_visitors\n"
        "- languages\n"
        "- operating_hours\n"
        "- accessibility (wheelchair, ramps, elevators)\n"
        "- how_to_reach (object with taxi, bus, metro, train)\n"
        "- tips_and_advice\n"
        "- booking_info (object with booking_link, phone)\n"
        "- documents_required (object with needed forms, proofs, photos, certificates)\n"
        "- social_media (object with facebook, instagram, youtube, tiktok)\n"
        "- contact_info (object with address, phone, email, website)\n"
        "- map_links (object with naver_map, google_map)\n"
        "- gallery (object with images[], videos[], reels[])\n"
        "- reviews (array of user reviews)\n"
        "- amenities (object with toilet, parking, outdoor_seating, indoor_seating)\n"
        "- main_image (object with alt_text, url)\n"
        "- sources (array of {{name, link}})\n"
        "\n"
        "### Flattening & Tag Mapping:\n"
        "- `general_answer` → tag: `general_answer`\n"
        "- `recommendations[]` → tag: `recommendation` (index each as `recommendation_0`, `recommendation_1`, ...)\n"
        "- `followup_questions[]` → tag: `followup_question`\n"
        "- `sources[]` → tag: `source`\n"
        "\n"
        "### Example Output (NDJSON, escaped for Python formatting):\n"
        "{{\"ui_element\": \"general_answer\", \"content\": \"Yes, you can extend your ARC while in Korea. The process is handled by the Korea Immigration Service.\", \"tag\": \"general_answer\"}}\n"
        "{{\"ui_element\": \"recommendation_0\", \"content\": {{\"name\": \"Korea Immigration Service – ARC Extension\", \"category\": \"Immigration Service\", \"weblink\": \"https://www.hikorea.go.kr\", \"address\": \"Korea Immigration Service HQ, Sejong-ro, Jongno-gu, Seoul\", \"google_map\": \"https://goo.gl/maps/HikoreaImmigration\", \"naver_map\": \"https://map.naver.com/v5/search/%ED%95%9C%EA%B5%AD%EC%9E%85%EA%B5%AD%EC%84%9C\", \"reviews\": [\"Efficient service if all documents are prepared\", \"Helpful English guidance available online\"], \"sources\": [{{\"name\": \"HiKorea Official Website – ARC Extension\", \"link\": \"https://www.hikorea.go.kr/pt/InfoDetailR_en.pt?categoryId=2&parentId=385&catSeq=401\"}}]}}, \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"followup_question_0\", \"content\": \"What documents are required for ARC extension?\", \"tag\": \"followup_question\"}}\n"
        "{{\"ui_element\": \"source_0_name\", \"content\": \"HiKorea Official Website – ARC Extension\", \"tag\": \"source\"}}\n"
        "{{\"ui_element\": \"source_0_link\", \"content\": \"https://www.hikorea.go.kr/pt/InfoDetailR_en.pt?categoryId=2&parentId=385&catSeq=401\", \"tag\": \"source\"}}\n"
        "\n"
        "Follow this style exactly. Keep `general_answer` concise (2–3 lines). Include all recommendation fields in one object and index multiple recommendations."
    ),
    ("human", "{question}")
])




        self.prompt_template_working = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a structured JSON streaming assistant.\n"
        "Flatten all nested objects and arrays from the `answer` object into NDJSON.\n"
        "Each JSON object must contain `ui_element`, `content`, and `tag`.\n"
        "\n"
        "### Rules:\n"
        "- Output **one JSON object per line** (NDJSON).\n"
        "- Never leave `content` empty; use 'N/A' if missing.\n"
        "- Split long text into smaller chunks if needed.\n"
        "- The `general_answer` must be concise: **2–3 lines only**.\n"
        "- Produce at least **3 recommendations**, each with `weblink`, `address`, `google_map`, and `naver_map`.\n"
        "- Produce at least **3 follow-up questions** and **3 sources** if available.\n"
        "\n"
        "### Flattening Schema & Tag Mapping:\n"
        "- `general_answer` → tag: `general_answer` (2–3 lines only)\n"
        "- `recommendations[]` → tag: `recommendation`\n"
        "   - Nested fields follow same tag `recommendation`\n"
        "   - `gallery[]` → tag: `gallery`\n"
        "   - `reviews[]` → tag: `review`\n"
        "- `followup_questions[]` → tag: `followup_question`\n"
        "- `sources[]` → tag: `source`\n"
        "\n"
        "### Example Output (NDJSON, escaped for Python formatting):\n"
        "{{\"ui_element\": \"general_answer\", \"content\": \"Yes, you can extend your ARC while in Korea. The process is handled by the Korea Immigration Service.\", \"tag\": \"general_answer\"}}\n"
        "{{\"ui_element\": \"recommendation_0_name\", \"content\": \"Korea Immigration Service – ARC Extension\", \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"recommendation_0_weblink\", \"content\": \"https://www.hikorea.go.kr\", \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"recommendation_0_address\", \"content\": \"Korea Immigration Service HQ, Sejong-ro, Jongno-gu, Seoul\", \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"recommendation_0_google_map\", \"content\": \"https://goo.gl/maps/HikoreaImmigration\", \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"recommendation_0_naver_map\", \"content\": \"https://map.naver.com/v5/search/%ED%95%9C%EA%B5%AD%EC%9E%85%EA%B5%AD%EC%84%9C\", \"tag\": \"recommendation\"}}\n"
        "{{\"ui_element\": \"followup_question_0\", \"content\": \"What documents are required for ARC extension?\", \"tag\": \"followup_question\"}}\n"
        "{{\"ui_element\": \"source_0_name\", \"content\": \"HiKorea Official Website – ARC Extension\", \"tag\": \"source\"}}\n"
        "{{\"ui_element\": \"source_0_link\", \"content\": \"https://www.hikorea.go.kr/pt/InfoDetailR_en.pt?categoryId=2&parentId=385&catSeq=401\", \"tag\": \"source\"}}\n"
        "\n"
        "Follow this style exactly, mapping each object to its tag, and keep `general_answer` concise (2–3 lines)."
    ),
    ("human", "{question}")
])








    async def stream_llm_response(self, question: str, request_id: str = None) -> AsyncGenerator[bytes, None]:
        request_id = request_id or str(uuid.uuid4())
        chunk_counter = 1
        buffer = ""

        try:
            messages = self.prompt_template.format_messages(question=question)

            for llm_chunk in self.llm.stream(messages):
                try:
                    buffer += llm_chunk.content
                    lines = buffer.split("\n")

                    for line in lines[:-1]:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            chunk_data = json.loads(line)
                            ui_element = chunk_data.get("ui_element", "unknown")
                            content = chunk_data.get("content", "")
                        except json.JSONDecodeError:
                            logger.warning(f"[LLM PARSE ERROR] request_id={request_id}: {line}")
                            ui_element = "unknown"
                            content = line

                        obj = {
                            "request_id": request_id,
                            "chunk_id": chunk_counter,
                            "total_chunks": -1,
                            "ui_element": ui_element,
                            "content": content
                        }
                        yield (json.dumps(obj) + "\n").encode("utf-8")
                        chunk_counter += 1
                        await asyncio.sleep(0)  # allow event loop to flush

                    buffer = lines[-1]  # keep last partial line

                except Exception as e:
                    logger.exception(f"[STREAM PROCESS ERROR] request_id={request_id}: {e}")
                    error_chunk = {
                        "request_id": request_id,
                        "chunk_id": chunk_counter,
                        "total_chunks": -1,
                        "ui_element": "error",
                        "content": str(e)
                    }
                    yield (json.dumps(error_chunk) + "\n").encode("utf-8")
                    chunk_counter += 1

        except Exception as e:
            logger.exception(f"[LLM STREAM ERROR] request_id={request_id}: {e}")
            error_chunk = {
                "request_id": request_id,
                "chunk_id": chunk_counter,
                "total_chunks": chunk_counter,
                "ui_element": "error",
                "content": str(e)
            }
            yield (json.dumps(error_chunk) + "\n").encode("utf-8")

        finally:
            # Final 'is_last' chunk
            final_chunk = {
                "request_id": request_id,
                "chunk_id": chunk_counter + 1,
                "total_chunks": chunk_counter + 1,
                "ui_element": "is_last",
                "content": "true"
            }
            yield (json.dumps(final_chunk) + "\n").encode("utf-8")

