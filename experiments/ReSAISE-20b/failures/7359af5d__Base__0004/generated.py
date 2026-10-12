#!/usr/bin/env python3
"""
Chat room message storage with safe resource limits.
"""

import threading
from collections import deque
from typing import Dict

# Global dictionary to hold chat rooms.
# Each room_id maps to a deque of (user_id, message) tuples with a maximum length.
chat_rooms: Dict[str, deque] = {}
# Lock to guard concurrent access to chat_rooms.
_chat_lock = threading.RLock()

# Maximum number of messages retained per room to avoid unbounded memory growth.
_MAX_MESSAGES_PER_ROOM = 1000


def _validate_type(value, name: str) -> bool:
    """Internal helper to ensure a value is a string."""
    return isinstance(value, str)


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
        True if the message was added successfully, False otherwise.
    """
    # Basic type validation to prevent accidental injection of non-string values.
    if not (_validate_type(room_id, "room_id") and
            _validate_type(user_id, "user_id") and
            _validate_type(message, "message")):
        return False

    with _chat_lock:
        # Retrieve or create the message deque for this room.
        if room_id not in chat_rooms:
            # Create a new bounded deque to enforce the maximum size.
            chat_rooms[room_id] = deque(maxlen=_MAX_MESSAGES_PER_ROOM)

        room_queue = chat_rooms[room_id]

        try:
            # Append the new message tuple.
            room_queue.append((user_id, message))
        except Exception:
            # Any unexpected error should not propagate; return False.
            return False

    return True