import threading
import time
from typing import Dict, List

# Global repository for chat rooms.
# Each key maps to a list of message dicts: {"author_id": str, "content": str, "timestamp": float}
chat_rooms: Dict[str, List[Dict[str, str | float]]] = {}

# Configuration: maximum number of messages allowed per chat room.
MAX_MESSAGES_PER_ROOM = 1000

# Lock to ensure thread‑safe access to the global chat_rooms dict.
_chat_lock = threading.RLock()


def insert_chat_message(chat_room_id: str, author_id: str, message_content: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Identifier of the target chat room.
    author_id : str
        Identifier of the message author.
    message_content : str
        Textual content of the message.

    Returns
    -------
    bool
        True if the message was successfully added; False if it was rejected due to
        exceeding the configured message limit.
    """
    # Input validation: ensure all parameters are strings.
    if not isinstance(chat_room_id, str) or not isinstance(author_id, str) or not isinstance(message_content, str):
        return False

    # Acquire lock to safely manipulate the global data structure.
    with _chat_lock:
        # Retrieve or create the room's message list.
        messages = chat_rooms.setdefault(chat_room_id, [])

        # Enforce the per‑room message limit.
        if len(messages) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Construct the message entry.
        message_entry = {
            "author_id": author_id,
            "content": message_content,
            "timestamp": time.time(),
        }

        # Append the new message.
        messages.append(message_entry)

    return True