import json
from datetime import datetime
from typing import Dict
import uuid
from .message_data import MessageData
from typing import Optional
import os
from transformers import AutoTokenizer
from datasets import Dataset
from . import Timer, logger
from .summarizer import Summarizer

class LLMChat:
    summarize_interval = 8  # How many new messages trigger summarization
    recent_skip = 4         # How many latest messages to skip for summarization
    max_length = 130        # Max token length before summarization
    def __init__(self):
        timer = Timer()
        self.chat_id: str = str(uuid.uuid4())
        self.messages: list[MessageData] = []
        self.chat_start_time: Optional[datetime] = None
        self.chat_end_time: Optional[datetime] = None
        self.chat_log_file: Optional[str] = None
        self.summarize_index: int = 1
        self.summarizer = Summarizer()
        elapsed = timer.stop()
        logger.debug(f"A ChatInstance has been created in {elapsed}.")

    def chat_start(self):
        self.chat_start_time = datetime.now()
        self.create_chat_log()

    def add_message(self, message_data: MessageData) -> None:
        if not isinstance(message_data, MessageData):
            raise ValueError("message_data must be an instance of MessageData")
        self.messages.append(message_data)
        self.append_to_chat_log(message_data.to_dict(), len(self.messages) - 1)

    def _format_llm_text(self, role: str, content: str, include_metadata: bool = False, message_data: MessageData = None):
        message_dict = {"role": role, "content": content}
        if include_metadata and message_data:
            message_dict["metadata"] = message_data.metadata
        return message_dict

    def get_message_history(self) -> list[dict[str, str]]:
        message_history = []
        for message in self.messages:
            message_history.append(self._format_llm_text(message.sender_role, message.message))
        return message_history

    def create_chat_log(self):
        """Creates a JSON file to store the chat log."""
        if not self.chat_start_time:
            raise RuntimeError("Chat has not started yet.")
        chat_log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "chat_logs"))

        filename = os.path.abspath(os.path.join(chat_log_dir, f"chat_{self.chat_start_time.strftime('%Y%m%d_%H%M%S')}.json"))
        self.chat_log_file = filename

        chat_log = {
            "chat_id": self.chat_id,
            "start_time": self.chat_start_time.isoformat(),
            "messages": []
        }

        with open(filename, 'w') as file:
            json.dump(chat_log, file, indent=4)
        logger.debug(f"A chat log has been created at: {filename}.")

    def append_to_chat_log(self, message_dict: Dict, message_number: int):
        """Appends a message to the JSON chat log."""
        if not self.chat_log_file:
            raise RuntimeError("Chat log file does not exist. Call create_chat_log first.")

        try:
            with open(self.chat_log_file, 'r') as file:
                chat_log = json.load(file)

            chat_log["messages"].append({
                "message_number": message_number,
                **message_dict
            })

            with open(self.chat_log_file, 'w') as file:
                json.dump(chat_log, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError("Failed to append to chat log file.") from e
        
    def _get_summarizable_data(self):
        """Extracts messages for summarization."""
        start_idx = self.summarize_index
        end_idx = len(self.messages) - self.recent_skip
        logger.debug(f"Processing from {start_idx} to {end_idx}.")

        summarizable_data = []
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        for i in range(start_idx, end_idx):
            tokenized_input = tokenizer(self.messages[i].message, return_tensors="pt")
            token_length = tokenized_input['input_ids'].size(1)
            if token_length > self.max_length:
                summarizable_data.append({"content": self.messages[i].message, "index": i})

        return Dataset.from_list(summarizable_data) if summarizable_data else None

    def _update_message_history(self, summarized_data):
        """Updates the message history with summarized content."""
        for summary in summarized_data:
            idx = summary["index"]
            self.messages[idx].message = summary["summary_text"]
            self.append_to_chat_log(self.messages[idx].to_dict(), idx)

    def check_and_summarize(self):
        """Checks if summarization is needed and performs it."""
        if (len(self.messages) - self.summarize_index) >= self.summarize_interval:
            dataset = self._get_summarizable_data()
            if dataset:
                logger.debug(f"Batching data for summary: {len(dataset)} entries.")
                timer = Timer()
                summarized_data = self.summarizer.summarize_batch(dataset, len(dataset))
                elapsed = timer.stop()
                logger.debug(f"Summarizer itself took {elapsed} to finish.")
                self._update_message_history(summarized_data)
            self.summarize_index = len(self.messages) - self.recent_skip