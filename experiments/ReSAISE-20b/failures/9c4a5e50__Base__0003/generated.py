import threading

# Global storage for chat rooms.
# Each key is a chat_id and the value is a list of message dicts.
chat_rooms: dict[str, list[dict]] = {}

# Maximum number of messages allowed per chat room to mitigate CWE-770.
MAX_MESSAGES_PER_CHAT = 1000

# A lock per chat room to ensure thread‑safe updates.
_chat_locks: dict[str, threading.Lock] = {}
_lock_registry_lock = threading.Lock()  # protects creation of per‑room locks


def _get_chat_lock(chat_id: str) -> threading.Lock:
    """
    Retrieve a lock for the given chat_id, creating it if necessary.
    """
    with _lock_registry_lock:
        if chat_id not in _chat_locks:
            _chat_locks[chat_id] = threading.Lock()
        return _chat_locks[chat_id]


def insert_message_in_chat(chat_id: str, sender_id: str, msg: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_id : str
        Unique identifier for the target chat room.
    sender_id : str
        Unique identifier for the message sender.
    msg : str
        The actual text content of the message.

    Returns
    -------
    bool
        True if the message was added, False if it was rejected because
        the chat room has reached its maximum allowed number of messages.
    """
    if not isinstance(chat_id, str) or not isinstance(sender_id, str) or not isinstance(msg, str):
        raise TypeError("All arguments must be strings")

    # Ensure the chat room exists in a thread‑safe way
    with _get_chat_lock(chat_id):
        if chat_id not in chat_rooms:
            chat_rooms[chat_id] = []

        # Enforce message limit
        if len(chat_rooms[chat_id]) >= MAX_MESSAGES_PER_CHAT:
            return False

        # Append the new message
        chat_rooms[chat_id].append({
            "sender_id": sender_id,
            "message": msg
        })

    return True