import threading

# Global storage for chat rooms and their message histories.
# Each key is a chat_room_id, value is a list of (sender, message) tuples.
chat_rooms: dict[str, list[tuple[str, str]]] = {}
# Lock to ensure thread‑safe updates to chat_rooms.
_chat_lock = threading.Lock()

# Maximum number of messages allowed per chat room before rejecting new ones.
_MAX_MESSAGES_PER_ROOM = 1000


def send_message_to_chat(chat_room_id: str, sender: str, chat_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Unique identifier for the target chat room.
    sender : str
        Unique identifier for the message sender.
    chat_message : str
        The actual text content of the message.

    Returns
    -------
    bool
        True if the message was added, False if it was rejected due to exceeding limits.
    """
    # Basic validation – reject empty identifiers or messages.
    if not chat_room_id or not sender or not chat_message:
        return False

    with _chat_lock:
        # Retrieve or create the message list for this room.
        messages = chat_rooms.setdefault(chat_room_id, [])

        # Enforce the maximum message limit.
        if len(messages) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.
        messages.append((sender, chat_message))
    return True