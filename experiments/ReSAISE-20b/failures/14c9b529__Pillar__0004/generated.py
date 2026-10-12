import threading

# Global repository for all chat rooms.
# Each key is a room identifier and each value is a list of messages
# where a message is represented as a tuple (author_identifier, text_message).
chat_rooms: dict[str, list[tuple[str, str]]] = {}

# Lock to protect concurrent access to chat_rooms.
_chat_lock = threading.RLock()

# Maximum number of messages a room may hold before rejecting new ones.
MAX_MESSAGES_PER_ROOM = 1000


def log_chat_message(target_room: str, author_identifier: str,
                     text_message: str) -> bool:
    """
    Append a new message to the conversation log of a specified chat room.

    Parameters
    ----------
    target_room : str
        Identifier for the chat room.
    author_identifier : str
        Unique identifier of the message author.
    text_message : str
        The content of the message.

    Returns
    -------
    bool
        True if the message was added successfully, False if the room has
        reached its maximum capacity and the message is rejected.

    Notes
    -----
    - The function is thread‑safe; it uses a re‑entrant lock to protect
      concurrent modifications of the global ``chat_rooms`` dictionary.
    - No exceptions are raised; invalid input is handled gracefully
      by treating it as a normal message.
    """
    # Ensure the inputs are strings to avoid accidental type errors
    target_room = str(target_room)
    author_identifier = str(author_identifier)
    text_message = str(text_message)

    with _chat_lock:
        # Initialize room if it does not exist
        if target_room not in chat_rooms:
            chat_rooms[target_room] = []

        room_messages = chat_rooms[target_room]

        # Reject the message if the room has reached its capacity
        if len(room_messages) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        room_messages.append((author_identifier, text_message))
        return True