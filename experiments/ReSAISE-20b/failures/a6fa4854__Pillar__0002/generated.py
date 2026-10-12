import threading

# Global storage for chat rooms.
# Each key is a chat_room id and the value is a list of (user, message) tuples.
chat_rooms: dict[str, list[tuple[str, str]]] = {}

# Lock to guard concurrent access to chat_rooms.
_chat_lock = threading.Lock()

# Maximum number of messages allowed in a single chat room.
_MAX_MESSAGES_PER_ROOM = 1000


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
        True if the message was added successfully, False if it was rejected due to exceeding limits.
    """
    # Basic validation: ensure inputs are non-empty strings.
    if not isinstance(chat_room, str) or not chat_room:
        return False
    if not isinstance(user, str) or not user:
        return False
    if not isinstance(new_message, str):
        return False

    # Acquire the lock to maintain a consistent state of chat_rooms.
    with _chat_lock:
        # Initialize room if it does not exist yet.
        if chat_room not in chat_rooms:
            chat_rooms[chat_room] = []

        # Enforce the message limit.
        if len(chat_rooms[chat_room]) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.
        chat_rooms[chat_room].append((user, new_message))
    return True