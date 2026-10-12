import datetime
import threading

# Global storage for chat rooms.
# Each room id maps to a list of message dictionaries.
chat_rooms = {}
# Global lock to protect concurrent access to chat_rooms.
_chat_lock = threading.RLock()

# Maximum number of messages a room can hold before rejecting new ones.
_MAX_MESSAGES_PER_ROOM = 1000


def insert_chat_message(chat_room_id: str, author_id: str,
                        message_content: str) -> bool:
    """
    Insert a new chat message into the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Identifier of the target chat room.
    author_id : str
        Identifier of the message author.
    message_content : str
        Textual content of the message.

    Returns
    -------
    bool
        ``True`` if the message was added; ``False`` if it was rejected
        due to exceeding the maximum allowed messages for that room.

    Notes
    -----
    * The function is thread‑safe; it uses a re‑entrant lock to guard
      the shared ``chat_rooms`` dictionary.
    * The function enforces a hard limit of ``_MAX_MESSAGES_PER_ROOM``
      messages per room to prevent uncontrolled growth.
    * No external resources are opened, so the risk of CWE‑664
      (improper control of a resource through its lifetime) is mitigated.
    """
    # Quick sanity checks
    if not chat_room_id or not author_id:
        return False

    # Build the message record
    msg = {
        "author": author_id,
        "content": message_content,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    with _chat_lock:
        # Ensure the room exists
        if chat_room_id not in chat_rooms:
            chat_rooms[chat_room_id] = []

        room_messages = chat_rooms[chat_room_id]

        # Reject if the room already reached its maximum size
        if len(room_messages) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        room_messages.append(msg)
        return True