import threading
from collections import deque
from typing import Dict, Deque

# Global repository of chat rooms.
# Each room maps to a deque of (author_identifier, text_message) tuples.
chat_rooms: Dict[str, Deque[tuple]] = {}
# A lock per room to ensure thread‑safe updates.
room_locks: Dict[str, threading.Lock] = {}

# Maximum number of messages retained per room.
MAX_MESSAGES_PER_ROOM = 1000

def _get_room_lock(room: str) -> threading.Lock:
    """
    Retrieve (or create) a lock for the specified room.
    This helper ensures that each room has its own dedicated lock,
    preventing race conditions in a concurrent environment.
    """
    if room not in room_locks:
        # Use double‑checked locking to avoid race conditions during lock creation.
        with threading.Lock():
            if room not in room_locks:
                room_locks[room] = threading.Lock()
    return room_locks[room]

def log_chat_message(target_room: str, author_identifier: str, text_message: str) -> bool:
    """
    Integrate an incoming message into the specified chat room's history.

    Parameters
    ----------
    target_room : str
        A unique identifier for the chat room.
    author_identifier : str
        Unique identifier of the message sender.
    text_message : str
        The content of the message.

    Returns
    -------
    bool
        True if the message was added; False if it exceeded the room's capacity.
    """
    # Basic validation of arguments (ensure they are strings).
    if not isinstance(target_room, str) or not isinstance(author_identifier, str) \
       or not isinstance(text_message, str):
        return False

    lock = _get_room_lock(target_room)

    with lock:
        # Create the room if it does not exist yet.
        if target_room not in chat_rooms:
            # Using deque with a fixed maxlen ensures we never exceed capacity.
            chat_rooms[target_room] = deque(maxlen=MAX_MESSAGES_PER_ROOM)

        room_queue = chat_rooms[target_room]

        # If the deque is full (maxlen reached), we reject the new message.
        if len(room_queue) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.
        room_queue.append((author_identifier, text_message))
        return True