import threading
from collections import defaultdict
from typing import Dict, List

# Global dictionary to store chat room messages.
# Each key is a room_id and the value is a list of message dictionaries.
chat_rooms: Dict[str, List[Dict[str, str]]] = defaultdict(list)

# Lock to ensure thread‑safe updates.
_chat_rooms_lock = threading.Lock()


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
    if not all(isinstance(x, str) and x.strip() for x in (room_id, user_id, message)):
        return False

    # Construct the message entry.
    msg_entry = {
        "user_id": user_id,
        "message": message,
        # Include a timestamp for ordering; using epoch seconds.
        "timestamp": str(int(threading.get_ident()))  # simple unique-ish placeholder
    }

    try:
        with _chat_rooms_lock:
            chat_rooms[room_id].append(msg_entry)
        return True
    except Exception:
        # Any unexpected exception should not propagate.
        return False