import threading
from datetime import datetime
from typing import Dict, List

# Global dictionary to store chat room messages.
# Each key is a room_id and the value is a list of message dictionaries.
chat_rooms: Dict[str, List[Dict]] = {}

# A lock to ensure thread‑safe updates to chat_rooms.
_chat_lock = threading.Lock()


def add_message_to_chat(room_id: str, user_id: str, message: str) -> bool:
    """
    Add a new message to the specified chat room.

    Parameters
    ----------
    room_id : str
        Identifier of the chat room.
    user_id : str
        Identifier of the user sending the message.
    message : str
        The content of the message.

    Returns
    -------
    bool
        True if the message was added successfully, False otherwise.
    """
    # Basic validation: ensure inputs are non‑empty strings.
    if not all(isinstance(arg, str) and arg for arg in (room_id, user_id, message)):
        return False

    # Construct the message record.
    msg_record = {
        "user_id": user_id,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    try:
        with _chat_lock:
            # Create the room if it doesn't exist.
            if room_id not in chat_rooms:
                chat_rooms[room_id] = []

            # Append the new message.
            chat_rooms[room_id].append(msg_record)
        return True
    except Exception:
        # In a real system we might log the exception.
        return False