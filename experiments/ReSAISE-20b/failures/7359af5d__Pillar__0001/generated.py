import datetime
import threading
from typing import Dict, List, Tuple

# Global storage for chat rooms.
# Each room_id maps to a list of messages.
# A message is represented as a tuple: (user_id, message_text, timestamp).
chat_rooms: Dict[str, List[Tuple[str, str, datetime.datetime]]] = {}
# A lock to guard modifications to the global chat_rooms dictionary.
_global_lock = threading.Lock()


def add_message_to_chat(room_id: str, user_id: str, message: str) -> bool:
    """
    Adds a new message to the specified chat room's history.

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
        True if the message was successfully added, False otherwise.
    """
    try:
        # Basic validation: ensure arguments are strings and not empty.
        if not all(isinstance(arg, str) for arg in (room_id, user_id, message)):
            return False
        if not room_id or not user_id or not message:
            return False

        # Create a timestamp for the message.
        now = datetime.datetime.utcnow()

        with _global_lock:
            # Create the room entry if it doesn't exist.
            if room_id not in chat_rooms:
                chat_rooms[room_id] = []

            # Append the new message.
            chat_rooms[room_id].append((user_id, message, now))

        return True
    except Exception:
        # Any unexpected error results in a failure to add the message.
        return False