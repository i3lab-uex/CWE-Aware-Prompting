import threading
from typing import Dict, List

# Global dictionary to store chat room messages.
# Each key is a room_id and the value is a list of message dicts.
chat_rooms: Dict[str, List[Dict[str, str]]] = {}

# Lock to guard access to the global chat_rooms dictionary.
_chat_lock = threading.RLock()


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
    # Basic validation of inputs
    if not isinstance(room_id, str) or not room_id:
        return False
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(message, str):
        return False

    # Sanitize message to avoid potential injection attacks.
    # Here we simply escape HTML special characters.
    def _escape(s: str) -> str:
        return (
            s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#x27;")
        )

    safe_message = _escape(message)

    # Acquire the lock to ensure thread-safe manipulation of chat_rooms.
    with _chat_lock:
        if room_id not in chat_rooms:
            # Initialize a new message list for this room.
            chat_rooms[room_id] = []

        try:
            chat_rooms[room_id].append({
                "user_id": user_id,
                "message": safe_message
            })
        except Exception:
            # Any unforeseen error results in a False return value.
            return False

    return True