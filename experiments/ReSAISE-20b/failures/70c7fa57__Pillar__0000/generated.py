import threading
from typing import Dict, List

# Global repository of chat rooms.
# Each room id maps to a list of message dicts.
chat_rooms: Dict[str, List[Dict]] = {}

# Lock per chat room to guard concurrent modifications.
_room_locks: Dict[str, threading.Lock] = {}

# Maximum number of messages a room may hold before rejecting new ones.
MAX_MESSAGES_PER_ROOM: int = 1000

def _get_room_lock(room_id: str) -> threading.Lock:
    """
    Retrieve or create a lock for the specified chat room.
    This function is thread‑safe and ensures that each room has exactly one lock instance.
    """
    if room_id not in _room_locks:
        # Use a temporary lock to guard the creation of a new lock.
        global _room_locks
        with threading.Lock():
            if room_id not in _room_locks:
                _room_locks[room_id] = threading.Lock()
    return _room_locks[room_id]


def insert_chat_message(chat_room_id: str, author_id: str, message_content: str) -> bool:
    """
    Insert a new chat message into the specified room.

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
        True if the message was successfully inserted; False if it exceeded limits.
    """
    # Basic validation
    if not isinstance(chat_room_id, str) or not isinstance(author_id, str) or not isinstance(message_content, str):
        return False

    # Ensure the room exists
    if chat_room_id not in chat_rooms:
        # Initialize a new empty list for the room
        chat_rooms[chat_room_id] = []

    lock = _get_room_lock(chat_room_id)

    with lock:
        # Enforce maximum message count
        if len(chat_rooms[chat_room_id]) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message as a dict; timestamps could be added if needed
        chat_rooms[chat_room_id].append({
            "author": author_id,
            "content": message_content
        })

    return True