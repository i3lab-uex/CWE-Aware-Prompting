import threading
from datetime import datetime

# Global storage for all chat rooms.
# Each room maps to a list of message dictionaries.
chat_rooms: dict[str, list[dict]] = {}
# Lock to protect concurrent modifications to chat_rooms.
_chat_lock = threading.RLock()

# Configuration: maximum number of messages per room before rejecting new ones.
MAX_MESSAGES_PER_ROOM = 1000

def push_text_to_room(room_name: str, member_id: str, content: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_name : str
        Unique identifier of the target chat room.
    member_id : str
        Unique identifier of the user sending the message.
    content : str
        Text content of the message.

    Returns
    -------
    bool
        True if the message was added; False if rejected due to exceeding limits.
    """
    # Basic validation of inputs
    if not all(isinstance(arg, str) for arg in (room_name, member_id, content)):
        raise TypeError("All arguments must be strings")

    # Enforce a minimal length for content to avoid spam
    if not content.strip():
        return False

    with _chat_lock:
        # Retrieve or create the room's message list
        messages = chat_rooms.setdefault(room_name, [])

        # Reject if room already has the maximum allowed number of messages
        if len(messages) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Build the message record
        message = {
            "member_id": member_id,
            "content": content,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        # Append the message to the room
        messages.append(message)

    return True