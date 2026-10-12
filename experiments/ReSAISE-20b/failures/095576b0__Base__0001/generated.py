import threading

# Global storage for chat rooms.
# Each room_tag maps to a list of message dicts: {"sender_id": ..., "text": ...}
chat_rooms = {}
# Lock to protect concurrent access to chat_rooms
_chat_lock = threading.RLock()

# Configuration: maximum number of messages per room before rejecting new ones.
_MAX_MESSAGES_PER_ROOM = 1000

def append_message_to_room(room_tag: str, sender_id: str, chat_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_tag : str
        Unique identifier of the target chat room.
    sender_id : str
        Unique identifier of the user sending the message.
    chat_message : str
        Text content of the message to be added.

    Returns
    -------
    bool
        True if the message was successfully added, False if rejected due to
        exceeding the maximum number of messages per room.
    """
    # Basic input validation (avoid empty identifiers)
    if not isinstance(room_tag, str) or not room_tag:
        return False
    if not isinstance(sender_id, str) or not sender_id:
        return False
    if not isinstance(chat_message, str):
        return False

    with _chat_lock:
        # Create the room if it does not exist
        if room_tag not in chat_rooms:
            chat_rooms[room_tag] = []

        # Enforce message limit
        if len(chat_rooms[room_tag]) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        chat_rooms[room_tag].append(
            {"sender_id": sender_id, "text": chat_message}
        )
        return True