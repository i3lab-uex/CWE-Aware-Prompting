import threading

# Global storage for chat rooms: {room_id: [messages]}
chat_rooms = {}
# Lock to protect concurrent modifications
_chat_lock = threading.RLock()

# Maximum number of messages allowed per chat room to prevent resource exhaustion
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
        True if the message was added, False if it would exceed the room's limit.
    """
    # Basic input validation
    if not isinstance(chat_room, str) or not chat_room:
        return False
    if not isinstance(user, str) or not user:
        return False
    if not isinstance(new_message, str):
        return False

    # Truncate overly long messages to avoid memory blowup
    MAX_MESSAGE_LENGTH = 10_000  # characters
    if len(new_message) > MAX_MESSAGE_LENGTH:
        new_message = new_message[:MAX_MESSAGE_LENGTH]

    with _chat_lock:
        # Initialize room if it doesn't exist
        if chat_room not in chat_rooms:
            chat_rooms[chat_room] = []

        # Enforce message count limit
        if len(chat_rooms[chat_room]) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        chat_rooms[chat_room].append({
            "user": user,
            "message": new_message
        })
    return True