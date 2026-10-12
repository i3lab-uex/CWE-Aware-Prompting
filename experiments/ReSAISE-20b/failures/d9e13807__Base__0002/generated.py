import threading
from collections import deque
from typing import Dict, Deque

# Global storage for chat rooms.
# Each room maps to a deque of (sender, message) tuples.
chat_rooms: Dict[str, Deque[tuple]] = {}
# Lock to protect concurrent access to chat_rooms.
_chat_lock = threading.RLock()

# Configuration: maximum number of messages retained per room
_MAX_MESSAGES_PER_ROOM = 1000

def _ensure_room_exists(chat_room_id: str) -> None:
    """Create the room's deque if it does not exist."""
    with _chat_lock:
        if chat_room_id not in chat_rooms:
            # Use deque for efficient FIFO removal when limit is exceeded
            chat_rooms[chat_room_id] = deque(maxlen=_MAX_MESSAGES_PER_ROOM)

def send_message_to_chat(chat_room_id: str, sender: str, chat_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Unique identifier for the target chat room.
    sender : str
        Unique identifier of the message sender.
    chat_message : str
        The actual text content of the message.

    Returns
    -------
    bool
        True if the message was successfully added, False if it was rejected
        because the room has reached its configured maximum capacity.

    Notes
    -----
    - Messages are stored in a deque with a fixed ``maxlen`` to prevent
      unbounded memory growth (CWE‑770 mitigation).
    - The function is thread‑safe via a re‑entrant lock.
    """
    if not isinstance(chat_room_id, str) or not isinstance(sender, str) or not isinstance(chat_message, str):
        # Defensive programming: reject non‑string inputs.
        return False

    _ensure_room_exists(chat_room_id)

    with _chat_lock:
        room = chat_rooms[chat_room_id]
        if len(room) >= _MAX_MESSAGES_PER_ROOM:
            # The deque will automatically discard the oldest message if we append,
            # but to honor the "rejection" requirement we return False instead.
            return False
        room.append((sender, chat_message))
    return True