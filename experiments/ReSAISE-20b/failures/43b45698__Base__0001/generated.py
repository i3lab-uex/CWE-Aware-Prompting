import threading

# Global dictionary mapping room names to lists of message dicts.
chat_rooms = {}
# Lock to ensure thread‑safe updates to the global structure.
_chat_lock = threading.RLock()

# Maximum number of messages allowed per room before rejecting new ones.
_MAX_MESSAGES_PER_ROOM = 1000


def push_text_to_room(room_name: str, member_id: str, content: str) -> bool:
    """
    Append a new text message to the specified chat room.

    Parameters
    ----------
    room_name : str
        Unique identifier for the target chat room.
    member_id : str
        Unique identifier for the user sending the message.
    content : str
        The text of the message.

    Returns
    -------
    bool
        True if the message was stored; False if the room has reached its
        maximum capacity.

    Notes
    -----
    * The function is thread‑safe via a re‑entrant lock.
    * Each message is stored as a dictionary containing the sender ID,
      content, and a timestamp.
    * The function enforces a hard limit on the number of messages per room
      to mitigate CWE‑770 (uncontrolled resource allocation).
    """
    # Basic validation: ensure non-empty strings.
    if not room_name or not member_id or content is None:
        return False

    with _chat_lock:
        # Create the room list if it does not exist.
        messages = chat_rooms.setdefault(room_name, [])

        # Enforce message count limit per room.
        if len(messages) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message with a simple timestamp.
        import time
        messages.append({
            'member_id': member_id,
            'content': content,
            'timestamp': time.time()
        })
    return True