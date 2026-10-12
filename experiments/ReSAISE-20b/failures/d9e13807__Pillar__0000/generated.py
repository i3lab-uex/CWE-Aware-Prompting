import re
from threading import Lock

# Global storage for chat rooms.
# Each key is a chat_room_id and the value is a list of message dicts.
chat_rooms: dict[str, list[dict]] = {}
# Lock to guard concurrent access to chat_rooms.
_chat_lock = Lock()

# Maximum number of messages allowed per chat room.
_MAX_MESSAGES_PER_ROOM = 100

def _validate_string(value: str, name: str) -> bool:
    """
    Basic validation to ensure the string is non-empty and does not contain
    control characters that could break formatting or cause injection.
    """
    if not isinstance(value, str) or not value.strip():
        return False
    # Disallow carriage returns and line feeds to keep messages on a single line.
    if re.search(r'[\r\n]', value):
        return False
    return True

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
        True if the message was added successfully, False otherwise.
    """
    # Basic input validation to guard against malformed data.
    if not (_validate_string(chat_room_id, "chat_room_id") and
            _validate_string(sender, "sender") and
            _validate_string(chat_message, "chat_message")):
        return False

    with _chat_lock:
        # Create the room if it does not exist.
        if chat_room_id not in chat_rooms:
            chat_rooms[chat_room_id] = []

        room_messages = chat_rooms[chat_room_id]

        # Enforce the maximum message limit.
        if len(room_messages) >= _MAX_MESSAGES_PER_ROOM:
            # Optionally, we could remove the oldest message to make space,
            # but for this implementation we simply reject new messages.
            return False

        # Append the new message as a dictionary.
        room_messages.append({
            "sender": sender,
            "message": chat_message
        })

    return True