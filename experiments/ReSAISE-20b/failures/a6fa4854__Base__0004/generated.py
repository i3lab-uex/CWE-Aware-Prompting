import threading

# Global storage for chat rooms.
# Each key is a room identifier; the value is a list of message tuples (user, text).
chat_rooms: dict[str, list[tuple[str, str]]] = {}

# Lock to protect concurrent access to `chat_rooms`.
_chat_lock = threading.Lock()

# Maximum number of messages a chat room may hold.
_MAX_MESSAGES_PER_ROOM: int = 1000


def post_msg_in_chat(chat_room: str, user: str, new_message: str) -> bool:
    """
    Append a message to the specified chat room.

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
        True if the message was successfully added, False if the room is at capacity.

    Notes
    -----
    - The function enforces a hard limit of ``_MAX_MESSAGES_PER_ROOM`` messages per room
      to mitigate CWE-770 (resource exhaustion).
    - Thread safety is ensured via a global lock.
    """
    if not isinstance(chat_room, str) or not isinstance(user, str) or not isinstance(new_message, str):
        # Defensive check: only accept string types.
        return False

    with _chat_lock:
        # Initialize the room if it doesn't exist yet.
        messages = chat_rooms.setdefault(chat_room, [])

        # Enforce the message limit.
        if len(messages) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.
        messages.append((user, new_message))
    return True