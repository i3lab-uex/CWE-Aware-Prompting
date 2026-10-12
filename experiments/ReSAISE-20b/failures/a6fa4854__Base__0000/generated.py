#!/usr/bin/env python3
"""
Chat message handling module.

This module defines a thread‑safe function for adding messages to a chat
room while preventing unbounded growth of the message history.

The implementation uses an in‑memory dictionary `chat_rooms` to store
messages per room.  Each message is a dict containing the sender,
the text, and a timestamp.

The function enforces a configurable maximum number of messages per
room (`MAX_MESSAGES_PER_ROOM`).  When the limit is reached, new
messages are rejected and `False` is returned.

Author: OpenAI ChatGPT
"""

import time
from typing import Dict, List
import threading

# Global storage for chat rooms.
# Keys: room identifiers (str)
# Values: list of message dicts
chat_rooms: Dict[str, List[Dict]] = {}

# Lock to guard concurrent access to `chat_rooms`.
_lock = threading.RLock()

# Configuration: maximum number of messages stored per room.
MAX_MESSAGES_PER_ROOM = 1000


def post_msg_in_chat(chat_room: str, user: str, new_message: str) -> bool:
    """
    Append a message to the specified chat room.

    Parameters
    ----------
    chat_room : str
        Unique identifier for the target chat room.
    user : str
        Unique identifier of the message sender.
    new_message : str
        The actual text content of the message.

    Returns
    -------
    bool
        True if the message was added successfully.
        False if the room has reached its message limit.

    Notes
    -----
    - The function is thread‑safe.
    - Messages are stored as dictionaries containing the user,
      message text, and a UTC timestamp.
    - If the room does not exist, it is created automatically.
    """
    if not isinstance(chat_room, str) or not chat_room:
        raise ValueError("chat_room must be a non-empty string")
    if not isinstance(user, str) or not user:
        raise ValueError("user must be a non-empty string")
    if not isinstance(new_message, str):
        raise ValueError("new_message must be a string")

    with _lock:
        room = chat_rooms.setdefault(chat_room, [])

        # Enforce the message limit.
        if len(room) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.
        room.append(
            {
                "user": user,
                "message": new_message,
                "timestamp": time.time(),  # seconds since epoch (UTC)
            }
        )
    return True