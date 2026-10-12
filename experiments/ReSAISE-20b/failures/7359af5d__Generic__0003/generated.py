import threading
from typing import Dict, List, Any

# Global storage for chat rooms and their message histories.
# Each room_id maps to a list of messages, where each message is a dict
# containing user_id, content, and a timestamp.
chat_rooms: Dict[str, List[Dict[str, Any]]] = {}

# Lock to ensure thread-safe modifications of chat_rooms.
_chat_lock = threading.Lock()


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
        Content of the message.

    Returns
    -------
    bool
        True if the message was successfully added, False otherwise.
    """
    # Basic validation to avoid storing empty messages or invalid IDs
    if not (room_id and user_id and message):
        return False

    # Acquire lock to safely modify the global dictionary
    with _chat_lock:
        if room_id not in chat_rooms:
            # Room does not exist; cannot add message
            return False

        # Append the new message with minimal metadata.
        chat_rooms[room_id].append(
            {"user_id": user_id, "message": message}
        )
    return True