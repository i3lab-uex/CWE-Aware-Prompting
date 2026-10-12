import threading
from typing import Dict, List

# Global in‑memory store for chat rooms.
# Each key is a chat_id and the value is a list of message dicts.
chat_rooms: Dict[str, List[Dict]] = {}
# Lock to protect concurrent access to chat_rooms.
_chat_lock = threading.RLock()

# Configuration: limits for each chat room.
_MAX_MESSAGES_PER_CHAT = 1000          # Maximum number of messages allowed per chat
_MAX_TOTAL_SIZE_BYTES = 10 * 1024 * 1024  # 10 MiB per chat

def _current_total_size(messages: List[Dict]) -> int:
    """Return the cumulative byte size of all message texts in a chat."""
    return sum(len(msg["msg"].encode("utf-8")) for msg in messages)

def insert_message_in_chat(chat_id: str, sender_id: str, msg: str) -> bool:
    """
    Append a new message to the specified chat room.

    The function enforces limits on the number of messages and total size per
    chat to mitigate CWE-770 (unbounded resource allocation).

    Args:
        chat_id: Unique identifier for the target chat room.
        sender_id: Unique identifier for the message sender.
        msg: The actual text content of the message.

    Returns:
        True if the message was added; False if it would exceed limits.
    """
    # Basic validation
    if not isinstance(chat_id, str) or not isinstance(sender_id, str) or not isinstance(msg, str):
        return False

    with _chat_lock:
        # Ensure chat room exists
        if chat_id not in chat_rooms:
            chat_rooms[chat_id] = []

        messages = chat_rooms[chat_id]

        # Check message count limit
        if len(messages) >= _MAX_MESSAGES_PER_CHAT:
            return False

        # Check total size limit
        current_size = _current_total_size(messages)
        new_msg_size = len(msg.encode("utf-8"))
        if current_size + new_msg_size > _MAX_TOTAL_SIZE_BYTES:
            return False

        # Append the message
        messages.append({"sender_id": sender_id, "msg": msg})
        return True