import os
import time
from threading import Timer
from typing import Any, List, Dict

from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_core.outputs import LLMResult

from app.shared.service.qa_service_external import save_new_message_to_history


class AsyncCallbackHandler(AsyncIteratorCallbackHandler):
    counter: int = 0
    final_found: bool = False
    answer_found: bool = False
    colon_found: bool = False
    result: Dict[int, List[str]] = {}

    def __init__(
            self,
            user_id: str,
            subject_id: int = None,
            topic_id: int = None
    ) -> None:
        super().__init__()
        self.user_id = user_id
        self.subject_id = subject_id
        self.topic_id = topic_id

    async def on_llm_new_token(
            self,
            token: str,
            **kwargs: Any
    ) -> None:
        if not self.final_found or not self.answer_found or not self.colon_found:
            self.counter += 1

        if not self.final_found:
            if "Final" in token:
                self.final_found = True
        else:
            if not self.answer_found:
                if "Answer" in token:
                    self.answer_found = True
                else:
                    self.final_found = False
            else:
                if not self.colon_found:
                    if ":" in token:
                        self.colon_found = True
                        self.result.update({self.counter: []})
                    else:
                        self.answer_found = False
                        self.final_found = False
                else:
                    value: List[str] = self.result.get(self.counter)
                    value.append(token)
                    self.result.update({self.counter: value})

    async def on_llm_end(
            self,
            response: LLMResult,
            **kwargs: Any
    ) -> None:
        if self.final_found and self.answer_found and self.colon_found:
            counter_on_trigger: int = self.counter
            self.final_found = False
            self.answer_found = False
            self.colon_found = False

            Timer(
                interval=float(os.environ["AGENT_COMMON_FINAL_ANSWER_GRACE_PERIOD_SECONDS"]),
                function=self._stream_response_if_truly_final,
                args=[counter_on_trigger]
            ).start()

    def _stream_response_if_truly_final(
            self,
            counter_on_trigger: int
    ) -> None:
        if counter_on_trigger == self.counter:
            for token in self.result.get(self.counter):
                self.queue.put_nowait(token)
                time.sleep(float(os.environ["AGENT_COMMON_RESPONSE_TOKEN_DELAY_SECONDS"]))
            self.done.set()
            save_new_message_to_history(
                user_id=self.user_id,
                subject_id=self.subject_id,
                topic_id=self.topic_id,
                message_content=''.join(self.result.get(self.counter))
            )
