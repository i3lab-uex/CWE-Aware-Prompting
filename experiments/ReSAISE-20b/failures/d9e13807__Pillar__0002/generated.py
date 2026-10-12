import threading
from typing import Dict, List

# Global storage for chat rooms. Each room maps to a list of message tuples:
# (sender_id, message_text)
chat_rooms: Dict[str, List[tuple]] = {}

# Global lock to protect concurrent access to `chat_rooms`
_chat_lock = threading.RLock()

# Maximum number of messages allowed per chat room
_MAX_MESSAGES_PER_ROOM: int = 1000


def send_message_to_chat(chat_room_id: str, sender: str, chat_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Unique identifier for the target chat room.
    sender : str
        Unique identifier for the message sender.
    chat_message : str
        The actual text content of the message.

    Returns
    -------
    bool
        True if the message was added successfully; False if the chat room
        has reached its maximum allowed number of messages.
    """
    # Basic validation: ensure all arguments are strings
    if not isinstance(chat_room_id, str) or not isinstance(sender, str) or not isinstance(chat_message, str):
        return False

    # Normalise whitespace to avoid abuse (e.g., many newlines)
    chat_message = chat_message.strip()
    if not chat_message:
        return False

    with _chat_lock:
        # Create the room list if it does not exist
        messages = chat_rooms.setdefault(chat_room_id, [])

        # Enforce the maximum message limit
        if len(messages) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        messages.append((sender, chat_message))
        return True