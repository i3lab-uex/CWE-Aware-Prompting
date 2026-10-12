import time
from typing import Dict, List, Tuple
from threading import Lock

# Global storage for chat rooms.
# Each room maps to a list of (timestamp, user, message) tuples.
chat_rooms: Dict[str, List[Tuple[float, str, str]]] = {}

# Maximum number of messages a room can hold before rejecting new ones.
_MAX_MESSAGES_PER_ROOM = 1000

# Lock to protect concurrent access to chat_rooms.
_chat_lock = Lock()


def post_msg_in_chat(chat_room: str, user: str, new_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_room : str
        Unique identifier for the target chat room.
    user : str
        Unique identifier for the message sender.
    new_message : str
        The actual text content of the message.

    Returns
    -------
    bool
        True if the message was added successfully,
        False if it was rejected due to exceeding limits.

    Notes
    -----
    * Messages are stored with a UTC timestamp for ordering.
    * Thread‑safety is ensured via a global lock.
    * The function enforces an upper bound on message count per room
      to prevent uncontrolled memory growth (CWE‑664 mitigation).
    """
    if not isinstance(chat_room, str) or not isinstance(user, str) \
       or not isinstance(new_message, str):
        # Defensive programming: reject invalid input types.
        return False

    with _chat_lock:
        room = chat_rooms.setdefault(chat_room, [])

        # Enforce message count limit.
        if len(room) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message with a timestamp.
        room.append((time.time(), user, new_message))

    return True