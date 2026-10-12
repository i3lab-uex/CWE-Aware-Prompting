import threading

# Global storage for chat rooms.
# Each key is a chat_id and the value is a list of message dicts.
chat_rooms: dict[str, list[dict]] = {}
# Lock to guard concurrent access to chat_rooms.
_chat_lock = threading.RLock()

# Maximum number of messages a single chat room may hold before rejecting new ones.
_MAX_MESSAGES_PER_CHAT = 1000

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
        True if the message was successfully added, False if it was rejected
        because the chat room already contains _MAX_MESSAGES_PER_CHAT messages.
    """
    if not isinstance(chat_id, str) or not isinstance(sender_id, str) or not isinstance(msg, str):
        # Defensive check – reject malformed inputs.
        return False

    with _chat_lock:
        # Retrieve or create the message list for this chat room.
        messages = chat_rooms.setdefault(chat_id, [])

        # Enforce the maximum message limit to prevent uncontrolled resource consumption.
        if len(messages) >= _MAX_MESSAGES_PER_CHAT:
            return False

        # Append the new message.
        messages.append({
            "sender_id": sender_id,
            "msg": msg,
            # Optional: timestamp could be added here for ordering.
        })

    return True