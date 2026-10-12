import threading

# Global storage for all chat rooms: {room_code: [message_dict, ...]}
chat_rooms = {}

# Configuration constants
MAX_MESSAGES_PER_ROOM = 1000     # maximum number of messages stored per room
MAX_MESSAGE_LENGTH   = 500       # maximum characters allowed in a single message

# Lock to protect concurrent access to chat_rooms
_chat_lock = threading.Lock()


def append_message_to_chat(room_code: str, user_identifier: str, msg_text: str) -> bool:
    """
    Append a message to the specified chat room.

    Parameters
    ----------
    room_code : str
        Unique identifier of the target chat room.
    user_identifier : str
        Unique identifier of the message author.
    msg_text : str
        The content of the message to be appended.

    Returns
    -------
    bool
        True if the message was added successfully, False if rejected due to limits.

    Notes
    -----
    * The function is thread‑safe via a global lock.
    * Messages longer than MAX_MESSAGE_LENGTH are truncated before storage.
    * If the room already contains MAX_MESSAGES_PER_ROOM messages, the new message is rejected.
    """
    if not isinstance(room_code, str) or not isinstance(user_identifier, str) or not isinstance(msg_text, str):
        # Invalid input types – treat as rejection
        return False

    # Enforce message length limit
    if len(msg_text) > MAX_MESSAGE_LENGTH:
        msg_text = msg_text[:MAX_MESSAGE_LENGTH]

    with _chat_lock:
        # Create room if it does not exist
        if room_code not in chat_rooms:
            chat_rooms[room_code] = []

        # Reject if limit reached
        if len(chat_rooms[room_code]) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append new message
        chat_rooms[room_code].append(
            {
                "user": user_identifier,
                "text": msg_text,
                "timestamp": None  # placeholder; could be datetime.utcnow() if needed
            }
        )
    return True