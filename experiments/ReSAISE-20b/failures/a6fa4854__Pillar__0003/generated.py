import threading

# Global storage for chat rooms.
# Each key is a chat_room identifier and the value is a list of message dicts.
chat_rooms = {}
# Lock to protect concurrent access to chat_rooms
_chat_lock = threading.RLock()

# Configuration: maximum number of messages per room.
MAX_MESSAGES_PER_ROOM = 1000

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
        True if the message was added, False if it was rejected due to
        exceeding the maximum allowed messages for the room.

    Notes
    -----
    - The function is thread‑safe and protects the global `chat_rooms`
      dictionary from concurrent modifications.
    - It enforces a maximum number of messages per room to avoid
      unbounded growth (CWE‑664).
    """
    if not isinstance(chat_room, str) or not isinstance(user, str) \
       or not isinstance(new_message, str):
        raise TypeError("All arguments must be strings")

    # Basic sanitisation: strip leading/trailing whitespace
    chat_room = chat_room.strip()
    user = user.strip()
    new_message = new_message.strip()

    # Reject empty messages
    if not new_message:
        return False

    with _chat_lock:
        # Initialise room if it does not exist
        if chat_room not in chat_rooms:
            chat_rooms[chat_room] = []

        # Enforce message limit
        if len(chat_rooms[chat_room]) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        chat_rooms[chat_room].append({
            'user': user,
            'message': new_message
        })
    return True