import threading
from typing import Dict, List

# Global storage for chat rooms: room_id -> list of messages
chat_rooms: Dict[str, List[Dict[str, str]]] = {}
# Lock to protect concurrent access to chat_rooms
_chat_lock = threading.RLock()


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
        True if the message was successfully added, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(room_id, str) or not room_id:
        return False
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(message, str):
        return False

    # Normalize message to avoid accidental injection of control characters
    sanitized_message = message.strip()

    # Prepare the message payload
    msg_payload = {
        "user_id": user_id,
        "message": sanitized_message,
    }

    # Thread‑safe update of the global chat_rooms dict
    with _chat_lock:
        if room_id not in chat_rooms:
            # Create a new list for the room if it doesn't exist
            chat_rooms[room_id] = []

        try:
            chat_rooms[room_id].append(msg_payload)
        except Exception:
            # Any unexpected error results in failure
            return False

    return True