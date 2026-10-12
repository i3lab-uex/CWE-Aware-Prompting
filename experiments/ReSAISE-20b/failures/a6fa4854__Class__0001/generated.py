import threading

# Global chat room storage.
# Each key is a chat_room id and the value is a list of (user, message) tuples.
chat_rooms = {}
# Lock to protect concurrent access to the global dictionary.
_chat_lock = threading.RLock()

# Maximum number of messages a chat room can hold to prevent uncontrolled memory growth.
_MAX_MESSAGES_PER_ROOM = 1000

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
        True if the message was successfully added, False if rejected due to exceeding limits.
    """
    # Basic validation of inputs
    if not isinstance(chat_room, str) or not chat_room:
        return False
    if not isinstance(user, str) or not user:
        return False
    if not isinstance(new_message, str):
        return False

    with _chat_lock:
        # Retrieve or create the message list for this chat room
        msgs = chat_rooms.setdefault(chat_room, [])

        # Enforce the maximum message limit per room
        if len(msgs) >= _MAX_MESSAGES_PER_ROOM:
            # Reject new message to avoid uncontrolled memory consumption
            return False

        # Append the new message as a tuple (user, message)
        msgs.append((user, new_message))
        return True