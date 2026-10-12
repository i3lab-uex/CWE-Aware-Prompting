import threading
from collections import defaultdict

# Global dictionary mapping room tags to a list of messages.
# Each message is stored as a tuple (sender_id, chat_message).
chat_rooms = defaultdict(list)

# Lock to ensure thread‑safe access to the global structure.
_chat_rooms_lock = threading.RLock()

# Maximum number of messages allowed per chat room before rejecting new ones.
_MAX_MESSAGES_PER_ROOM = 10_000


def append_message_to_room(room_tag: str, sender_id: str, chat_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_tag : str
        Unique identifier for the target chat room.
    sender_id : str
        Unique identifier of the user sending the message.
    chat_message : str
        The text content to be appended.

    Returns
    -------
    bool
        True if the message was added successfully, False if the room has reached its
        maximum capacity.

    Notes
    -----
    - The function enforces a hard limit on the number of messages per room to avoid
      uncontrolled memory growth (CWE‑770 mitigation).
    - Thread safety is ensured via a re‑entrant lock.
    """
    if not isinstance(room_tag, str) or not isinstance(sender_id, str) \
       or not isinstance(chat_message, str):
        # Defensive check: ignore malformed input.
        return False

    with _chat_rooms_lock:
        current_count = len(chat_rooms[room_tag])
        if current_count >= _MAX_MESSAGES_PER_ROOM:
            # Reject the message to prevent unlimited resource allocation.
            return False

        # Append the new message as a tuple. Using a tuple keeps the data immutable.
        chat_rooms[room_tag].append((sender_id, chat_message))
        return True