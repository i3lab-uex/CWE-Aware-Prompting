import threading

# Global storage for chat rooms.
# Each key is a chat_room id, and the value is a list of message dictionaries:
#   {"user": user_id, "message": text}
chat_rooms = {}
# Lock to ensure thread‑safe updates.
_chat_lock = threading.Lock()

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
        exceeding the maximum number of stored messages.

    Notes
    -----
    - The function enforces a hard limit of 1000 messages per chat room.
      Older messages are discarded in a FIFO manner when the limit is exceeded.
    - Thread safety is achieved via a global lock. This keeps the implementation
      simple and works well for typical I/O‑bound workloads.
    """
    if not isinstance(chat_room, str) or not isinstance(user, str) or not isinstance(new_message, str):
        # Reject malformed inputs silently
        return False

    with _chat_lock:
        # Create the room if it does not exist
        history = chat_rooms.setdefault(chat_room, [])

        # Enforce the limit (FIFO eviction)
        MAX_MESSAGES = 1000
        if len(history) >= MAX_MESSAGES:
            # Remove the oldest message
            history.pop(0)

        # Append the new message
        history.append({"user": user, "message": new_message})
    return True