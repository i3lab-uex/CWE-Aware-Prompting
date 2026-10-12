import threading

# Global dictionary mapping room identifiers to a list of message dicts.
chat_rooms = {}
# A lock to guard concurrent access to chat_rooms.
_chat_lock = threading.Lock()

# Maximum number of messages allowed per room (CWE‑770 mitigation).
_MAX_MESSAGES_PER_ROOM = 1000

def log_chat_message(target_room: str, author_identifier: str, text_message: str) -> bool:
    """
    Append a message to the specified chat room's conversation log.

    Parameters
    ----------
    target_room : str
        Identifier of the chat room.
    author_identifier : str
        Unique identifier for the message author.
    text_message : str
        The textual content of the message.

    Returns
    -------
    bool
        True if the message was added; False if the room exceeded its message limit.

    Notes
    -----
    - Thread‑safe: uses a global lock to serialize modifications.
    - Enforces a hard cap on the number of messages per room to mitigate CWE‑770.
    """
    # Normalise input (basic validation)
    if not all(isinstance(x, str) and x for x in (target_room, author_identifier, text_message)):
        return False

    with _chat_lock:
        # Create the room entry if it does not exist
        messages = chat_rooms.setdefault(target_room, [])

        # Enforce the message limit
        if len(messages) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        messages.append({
            "author": author_identifier,
            "message": text_message,
            # Timestamp could be added here if needed
        })

    return True