import collections
import datetime
import threading

# Maximum number of messages retained per chat room.
MAX_MESSAGES_PER_ROOM = 1000

# Global storage for all chat rooms. Each value is a deque with a fixed maximum length.
chat_rooms: dict[str, collections.deque[dict]] = {}
# Global lock to ensure thread‑safe access/modification of chat_rooms.
rooms_lock = threading.RLock()


def push_text_to_room(room_name: str, member_id: str, content: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_name : str
        Identifier of the target chat room.
    member_id : str
        Identifier of the user sending the message.
    content : str
        Text content of the message.

    Returns
    -------
    bool
        True if the message was added successfully, False otherwise.
    """
    # Basic validation: ensure non‑empty values and reasonable length
    if not (room_name and member_id and content):
        return False

    # Truncate overly long content to avoid abuse.
    if len(content) > 10_000:   # arbitrary but reasonable limit
        content = content[:10_000]

    message = {
        "member_id": member_id,
        "content": content,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    with rooms_lock:
        # Create a new deque for the room if it does not exist.
        if room_name not in chat_rooms:
            chat_rooms[room_name] = collections.deque(maxlen=MAX_MESSAGES_PER_ROOM)

        room_deque = chat_rooms[room_name]

        # The deque's maxlen automatically discards the oldest message when full.
        room_deque.append(message)

    # If we reach here, the message was appended successfully.
    return True