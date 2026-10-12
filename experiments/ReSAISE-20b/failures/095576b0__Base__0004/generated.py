import threading

# Global storage for chat rooms.
# Each key is a room_tag, and the value is a list of message dicts.
chat_rooms = {}
# Lock to protect concurrent access to chat_rooms.
_chat_lock = threading.RLock()

# Maximum number of messages allowed per room (simple throttling to mitigate CWE‑770).
_MAX_MESSAGES_PER_ROOM = 1000

def append_message_to_room(room_tag: str, sender_id: str, chat_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_tag : str
        Unique identifier of the target chat room.
    sender_id : str
        Identifier of the user sending the message.
    chat_message : str
        Text content of the message.

    Returns
    -------
    bool
        True if the message was added successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(room_tag, str) or not room_tag:
        return False
    if not isinstance(sender_id, str) or not sender_id:
        return False
    if not isinstance(chat_message, str):
        return False

    # Truncate overly long messages to avoid runaway memory usage
    MAX_MESSAGE_LENGTH = 10_000  # bytes (approx)
    if len(chat_message.encode('utf-8')) > MAX_MESSAGE_LENGTH:
        chat_message = chat_message[:MAX_MESSAGE_LENGTH]

    with _chat_lock:
        # Initialize room if it doesn't exist
        if room_tag not in chat_rooms:
            chat_rooms[room_tag] = []

        # Enforce per‑room message limit
        if len(chat_rooms[room_tag]) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        chat_rooms[room_tag].append({
            'sender_id': sender_id,
            'message': chat_message
        })

    return True