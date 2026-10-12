import threading

# Global dictionary holding conversation histories.
# Each key is a room identifier and the value is a list of message tuples:
# (author_identifier, text_message)
chat_rooms: dict[str, list[tuple[str, str]]] = {}
# Lock to protect concurrent access to chat_rooms
_chat_lock = threading.RLock()

# Maximum number of messages allowed per room before rejecting new ones.
_MAX_MESSAGES_PER_ROOM = 1000

def log_chat_message(
    target_room: str,
    author_identifier: str,
    text_message: str
) -> bool:
    """
    Append a message to the conversation log of ``target_room``.
    
    Parameters
    ----------
    target_room : str
        Identifier for the chat room.
    author_identifier : str
        Unique identifier of the message author.
    text_message : str
        The textual content to be logged.

    Returns
    -------
    bool
        ``True`` if the message was added successfully,
        ``False`` if the room has reached its message limit.

    Notes
    -----
    * The function enforces a hard cap on the number of messages per room to
      mitigate CWE-770 (unbounded resource allocation).
    * Thread safety is guaranteed by a re‑entrant lock.
    """
    if not isinstance(target_room, str) or not target_room:
        return False
    if not isinstance(author_identifier, str) or not author_identifier:
        return False
    if not isinstance(text_message, str):
        return False

    with _chat_lock:
        # Retrieve or create the room history
        room_history = chat_rooms.setdefault(target_room, [])

        # Enforce message limit
        if len(room_history) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        room_history.append((author_identifier, text_message))
    return True