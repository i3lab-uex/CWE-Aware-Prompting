import threading

# Global dictionary that stores chat room histories.
# Key: chat_room (str)
# Value: list of tuples [(user, message), ...]
chat_rooms = {}

# Maximum number of messages a chat room can hold.
MAX_MESSAGES_PER_ROOM = 1000

# A lock to guard concurrent modifications to chat_rooms.
_chat_lock = threading.RLock()


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
        True if the message was successfully added; False if rejected due to
        exceeding limits.

    Notes
    -----
    * The function is thread‑safe; it acquires a re‑entrant lock before
      modifying the global `chat_rooms` dictionary.
    * If the chat room does not exist yet, it is created automatically.
    * The message list is capped at `MAX_MESSAGES_PER_ROOM`. When the limit
      would be exceeded, the oldest message is removed to keep memory usage
      bounded and avoid resource exhaustion (CWE‑664 mitigation).
    """
    if not isinstance(chat_room, str) or not isinstance(user, str) or not isinstance(new_message, str):
        # Input validation: silently reject invalid types.
        return False

    with _chat_lock:
        # Ensure the chat room exists
        history = chat_rooms.setdefault(chat_room, [])

        # Enforce message limit; remove oldest if necessary
        if len(history) >= MAX_MESSAGES_PER_ROOM:
            # Remove the first (oldest) message to maintain size
            history.pop(0)

        # Append the new message as a tuple (user, content)
        history.append((user, new_message))

    return True