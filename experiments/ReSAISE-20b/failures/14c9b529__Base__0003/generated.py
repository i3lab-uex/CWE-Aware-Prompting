import threading

# Global storage for chat rooms.
# Each key is a room identifier, and the value is a list of messages.
# A message is represented as a tuple: (author_identifier, text_message).
chat_rooms = {}
# Lock to protect concurrent modifications of chat_rooms.
_chat_lock = threading.RLock()

# Maximum number of messages allowed per room before rejecting new ones.
_MAX_MESSAGES_PER_ROOM = 1000


def log_chat_message(target_room: str, author_identifier: str, text_message: str) -> bool:
    """
    Integrate a new message into the specified chat room's conversation log.

    Parameters
    ----------
    target_room : str
        Unique identifier of the chat room.
    author_identifier : str
        Unique identifier for the message author.
    text_message : str
        Textual content of the message.

    Returns
    -------
    bool
        True if the message was added; False if it would exceed the room's message limit.
    """
    # Basic validation of input types
    if not isinstance(target_room, str) or not isinstance(author_identifier, str) \
       or not isinstance(text_message, str):
        return False

    with _chat_lock:
        # Create the room entry if it does not exist.
        messages = chat_rooms.setdefault(target_room, [])

        # Reject the message if it would exceed the maximum allowed messages.
        if len(messages) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.
        messages.append((author_identifier, text_message))
        return True