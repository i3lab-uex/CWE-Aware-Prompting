import datetime
from typing import Dict, List, Tuple
import threading

# Global storage for chat rooms.
# Each room ID maps to a list of message tuples:
# (timestamp, author_identifier, text_message)
chat_rooms: Dict[str, List[Tuple[datetime.datetime, str, str]]] = {}

# Global lock to protect access to the chat_rooms dictionary.
_chat_lock = threading.RLock()

# Configuration: maximum number of messages allowed per room.
_MAX_MESSAGES_PER_ROOM = 1000


def log_chat_message(
    target_room: str, author_identifier: str, text_message: str
) -> bool:
    """
    Append a new message to the conversation log of `target_room`.

    Parameters
    ----------
    target_room : str
        Identifier for the chat room.
    author_identifier : str
        Unique identifier of the message author.
    text_message : str
        The content of the message.

    Returns
    -------
    bool
        True if the message was appended successfully, False if it was rejected
        due to exceeding the per‑room message limit.
    """
    # Validate input types (basic safety check)
    if not isinstance(target_room, str) or not target_room:
        return False
    if not isinstance(author_identifier, str):
        return False
    if not isinstance(text_message, str):
        return False

    # Normalize the room key to avoid accidental duplicates
    room_key = target_room.strip()

    with _chat_lock:
        # Create the room if it doesn't exist
        if room_key not in chat_rooms:
            chat_rooms[room_key] = []

        # Enforce the message limit
        if len(chat_rooms[room_key]) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message with a UTC timestamp
        timestamp = datetime.datetime.utcnow()
        chat_rooms[room_key].append((timestamp, author_identifier, text_message))

    return True