import threading

# Global dictionary storing chat room histories.
# Each key is a `room_id` and the value is a list of message dicts:
#   {"user_id": ..., "message": ...}
chat_rooms = {}
_chat_lock = threading.RLock()


def add_message_to_chat(room_id: str, user_id: str, message: str) -> bool:
    """
    Add a new message to the specified chat room's history.

    Parameters
    ----------
    room_id : str
        Identifier of the chat room.
    user_id : str
        Identifier of the user sending the message.
    message : str
        The content of the message.

    Returns
    -------
    bool
        True if the message was added successfully, False otherwise.
    """
    # Basic validation: ensure all arguments are non-empty strings
    if not (room_id and isinstance(room_id, str)):
        return False
    if not (user_id and isinstance(user_id, str)):
        return False
    if not (message is not None and isinstance(message, str)):
        return False

    # Truncate overly long messages to prevent abuse (e.g., 10,000 chars)
    MAX_MESSAGE_LENGTH = 10_000
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH]

    # Create the message record
    msg_record = {"user_id": user_id, "message": message}

    # Thread‑safe update of the global chat_rooms dictionary
    try:
        with _chat_lock:
            if room_id not in chat_rooms:
                # Initialize a new message list for the room
                chat_rooms[room_id] = []
            chat_rooms[room_id].append(msg_record)
        return True
    except Exception:
        # In a production system we would log the exception.
        return False