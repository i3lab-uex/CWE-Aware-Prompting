#!/usr/bin/env python3
"""
Chat message handling module.

This module defines a thread‑safe function for adding messages to chat rooms.
Each chat room is represented as a list of message dictionaries.  A global
dictionary `chat_rooms` holds all rooms, and a single lock protects concurrent
access to the structure.

The implementation respects the following safety considerations:

* **CWE‑664** – The lock is acquired only for the minimal critical section
  needed to modify the data structure.  The lock is released immediately
  after the update, ensuring that resources (the lock) are not held longer
  than necessary.
* **Input validation** – The function checks that all arguments are strings,
  raising `ValueError` otherwise.  This guards against type errors and
  accidental injection of non‑string data.
* **Message limit** – A configurable maximum number of messages per room
  (`MAX_MESSAGES_PER_ROOM`) is enforced.  When the limit would be exceeded,
  the message is rejected and `False` is returned.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Any

# Global storage for chat rooms.
chat_rooms: Dict[str, List[Dict[str, str]]] = {}

# Lock to protect concurrent access to `chat_rooms`.
_chat_lock = threading.RLock()

# Maximum number of messages allowed per chat room.
MAX_MESSAGES_PER_ROOM: int = 1000


def _validate_string(value: Any, name: str) -> None:
    """Ensure that a value is a non‑empty string."""
    if not isinstance(value, str):
        raise ValueError(f"'{name}' must be a string")
    if not value:
        raise ValueError(f"'{name}' cannot be empty")


def send_message_to_chat(
    chat_room_id: str,
    sender: str,
    chat_message: str
) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Unique identifier for the target chat room.
    sender : str
        Unique identifier for the message sender.
    chat_message : str
        The actual text content of the message.

    Returns
    -------
    bool
        True if the message was successfully added; False if rejected due to
        exceeding the per‑room message limit.

    Raises
    ------
    ValueError
        If any argument is not a non‑empty string.
    """
    # Validate inputs first (outside the lock).
    _validate_string(chat_room_id, "chat_room_id")
    _validate_string(sender, "sender")
    _validate_string(chat_message, "chat_message")

    # Prepare the message payload.
    new_entry = {
        "sender": sender,
        "message": chat_message
    }

    with _chat_lock:
        # Retrieve or create the room's message list.
        room = chat_rooms.setdefault(chat_room_id, [])

        # Enforce the maximum message limit.
        if len(room) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message.
        room.append(new_entry)

    return True