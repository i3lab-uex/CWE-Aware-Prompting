import time
from threading import Lock

# Global storage for chat rooms.
# Each room maps to a list of message dicts.
chat_rooms: dict[str, list[dict]] = {}
# Lock to protect concurrent modifications to chat_rooms.
chat_rooms_lock = Lock()

# Maximum number of messages allowed per room. Adjust as needed.
MAX_MESSAGES_PER_ROOM: int = 1000


def push_text_to_room(room_name: str, member_id: str, content: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_name : str
        Identifier for the target chat room.
    member_id : str
        Identifier of the user sending the message.
    content : str
        Textual content of the message.

    Returns
    -------
    bool
        True if the message was added; False if it would exceed room limits.
    """
    # Basic validation to avoid storing empty or overly long messages
    if not content:
        return False

    # Truncate content to a reasonable maximum length (e.g., 10_000 characters)
    MAX_CONTENT_LENGTH = 10_000
    if len(content) > MAX_CONTENT_LENGTH:
        content = content[:MAX_CONTENT_LENGTH]

    with chat_rooms_lock:
        # Create the room entry if it does not exist.
        messages = chat_rooms.setdefault(room_name, [])

        # Reject the message if adding it would exceed the limit.
        if len(messages) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.
        messages.append({
            "member_id": member_id,
            "content": content,
            "timestamp": time.time()
        })

    return True