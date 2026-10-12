import threading
from typing import Dict, List

# Global storage for chat rooms. Each room ID maps to a list of message dicts.
chat_rooms: Dict[str, List[Dict[str, str]]] = {}
# Lock to protect concurrent access to chat_rooms.
_chat_lock = threading.RLock()

# Maximum number of messages allowed per room (simple limit to avoid resource exhaustion).
_MAX_MESSAGES_PER_ROOM = 10_000


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
        True if the message was successfully added, False if it was rejected due to exceeding limits.
    """
    # Basic validation: ensure all inputs are strings and not empty
    if not isinstance(chat_room_id, str) or not chat_room_id:
        return False
    if not isinstance(sender, str) or not sender:
        return False
    if not isinstance(chat_message, str):
        return False

    # Truncate overly long messages to prevent excessive memory usage
    MAX_MESSAGE_LENGTH = 10_000  # characters
    if len(chat_message) > MAX_MESSAGE_LENGTH:
        chat_message = chat_message[:MAX_MESSAGE_LENGTH]

    with _chat_lock:
        # Retrieve or create the message list for this room
        messages = chat_rooms.setdefault(chat_room_id, [])

        # Enforce per-room message limit
        if len(messages) >= _MAX_MESSAGES_PER_ROOM:
            # If the limit is reached, reject the new message
            return False

        # Append the new message as a dictionary
        messages.append({
            "sender": sender,
            "message": chat_message,
        })

    return True