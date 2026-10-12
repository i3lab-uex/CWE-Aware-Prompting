import threading
from typing import Dict, List

# Global data store for chat rooms.
# Each key is a room id and the value is a list of message dictionaries.
chat_rooms: Dict[str, List[Dict]] = {}

# Lock to protect concurrent access to the chat_rooms structure.
_chat_lock = threading.RLock()

# Maximum number of messages allowed in a single chat room.
_MAX_MESSAGES_PER_ROOM = 1000

def insert_chat_message(
    chat_room_id: str,
    author_id: str,
    message_content: str
) -> bool:
    """
    Insert a new chat message into the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Unique identifier for the target chat room.
    author_id : str
        Unique identifier of the message author.
    message_content : str
        Textual content of the message.

    Returns
    -------
    bool
        True if the message was inserted successfully; False if insertion failed
        because the room has reached its maximum capacity.
    """
    # Basic validation of inputs to avoid malformed data.
    if not isinstance(chat_room_id, str) or not chat_room_id:
        return False
    if not isinstance(author_id, str) or not author_id:
        return False
    if not isinstance(message_content, str):
        return False

    # Truncate message content to a reasonable length (e.g., 10,000 characters)
    MAX_MESSAGE_LENGTH = 10_000
    if len(message_content) > MAX_MESSAGE_LENGTH:
        message_content = message_content[:MAX_MESSAGE_LENGTH]

    with _chat_lock:
        # Retrieve or create the room's message list.
        messages = chat_rooms.setdefault(chat_room_id, [])

        # Enforce the maximum number of messages.
        if len(messages) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.  Using a simple dict keeps the structure
        # flexible for future extensions (e.g., timestamps, metadata).
        messages.append({
            "author_id": author_id,
            "content": message_content
        })

    return True