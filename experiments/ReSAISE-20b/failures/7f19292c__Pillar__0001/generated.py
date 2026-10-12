import threading
from datetime import datetime

# Global data structures
chat_rooms = {}          # {room_code: [message_dict, ...]}
rooms_locks = {}         # {room_code: threading.Lock()}
MAX_MESSAGES_PER_ROOM = 1000   # Limit to prevent uncontrolled growth

# Helper to ensure a lock exists for a room
def _get_room_lock(room_code: str) -> threading.Lock:
    if room_code not in rooms_locks:
        # Create a new lock atomically
        with threading.Lock():
            if room_code not in rooms_locks:
                rooms_locks[room_code] = threading.Lock()
    return rooms_locks[room_code]

def append_message_to_chat(room_code: str, user_identifier: str, msg_text: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_code : str
        Unique identifier for the target chat room.
    user_identifier : str
        Identifier of the message author.
    msg_text : str
        Text content of the message.

    Returns
    -------
    bool
        True if the message was appended; False if the room is at capacity.
    """
    lock = _get_room_lock(room_code)
    with lock:
        # Initialize room if it doesn't exist
        if room_code not in chat_rooms:
            chat_rooms[room_code] = []

        # Enforce message limit
        if len(chat_rooms[room_code]) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Construct the message record
        message = {
            "user": user_identifier,
            "text": msg_text,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
        }

        chat_rooms[room_code].append(message)
    return True