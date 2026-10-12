import threading
from collections import deque
from typing import Dict

# Global dictionary mapping room tags to a queue of messages.
# Each message is stored as a tuple: (sender_id, chat_message).
chat_rooms: Dict[str, deque] = {}
# A lock to protect concurrent access to the global chat_rooms structure.
_chat_lock = threading.Lock()

# Maximum number of messages a room can store. Older messages are discarded
# when this limit is reached.
MAX_MESSAGES_PER_ROOM = 1000


def append_message_to_room(room_tag: str, sender_id: str, chat_message: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_tag : str
        Unique identifier for the target chat room.
    sender_id : str
        Unique identifier for the user sending the message.
    chat_message : str
        The text content of the message to be added.

    Returns
    -------
    bool
        True if the message was successfully added; False if rejected
        due to exceeding the room's capacity.
    """
    # Basic validation: ensure inputs are non-empty strings
    if not all(isinstance(v, str) and v for v in (room_tag, sender_id, chat_message)):
        return False

    with _chat_lock:
        # Create a new deque for the room if it does not exist
        if room_tag not in chat_rooms:
            chat_rooms[room_tag] = deque(maxlen=MAX_MESSAGES_PER_ROOM)

        room_queue = chat_rooms[room_tag]

        # If the deque is already at capacity, reject the new message
        if len(room_queue) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message
        room_queue.append((sender_id, chat_message))
        return True