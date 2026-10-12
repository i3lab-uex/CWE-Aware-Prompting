import threading
from datetime import datetime

# Global dictionary to store chat room histories.
# Each key is a chat_room_id and the value is a list of message dicts.
chat_rooms = {}
# Maximum number of messages allowed per chat room.
MAX_MESSAGES_PER_ROOM = 1000
# Lock to ensure thread‑safe updates to chat_rooms.
_chat_lock = threading.RLock()


def send_message_to_chat(chat_room_id: str, sender: str, chat_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Unique identifier for the target chat room.
    sender : str
        Unique identifier for the message sender.
    chat_message : str
        The actual text content of the message.

    Returns
    -------
    bool
        True if the message was successfully added to the chat room,
        False if it was rejected due to exceeding limits.

    Notes
    -----
    * The function is thread‑safe.
    * Messages are stored as dictionaries containing the sender,
      timestamp (UTC), and content.
    * If a chat room does not exist yet, it is created automatically.
    * If the chat room already contains `MAX_MESSAGES_PER_ROOM` messages,
      new messages are rejected to avoid uncontrolled memory growth.
    """
    if not isinstance(chat_room_id, str) or not isinstance(sender, str) \
       or not isinstance(chat_message, str):
        # Input validation: silently reject invalid types.
        return False

    message = {
        "sender": sender,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "content": chat_message,
    }

    with _chat_lock:
        room = chat_rooms.setdefault(chat_room_id, [])
        if len(room) >= MAX_MESSAGES_PER_ROOM:
            # Reject new messages when limit is reached.
            return False
        room.append(message)
    return True