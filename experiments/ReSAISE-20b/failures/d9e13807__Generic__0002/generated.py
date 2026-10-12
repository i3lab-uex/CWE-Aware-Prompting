#!/usr/bin/env python3
"""
Chat message handling module.

This module provides a thread‑safe function to append messages to a chat room
history.  Each chat room is identified by a unique string key and stores its
messages as a list of dictionaries.  The function enforces a configurable
maximum number of messages per room to prevent unbounded memory usage.
"""

from __future__ import annotations

import threading
from datetime import datetime
from typing import Dict, List

# Global storage for chat rooms.  Each value is a list of message dicts.
chat_rooms: Dict[str, List[dict]] = {}

# Lock to protect concurrent access to `chat_rooms`.
_chat_lock = threading.RLock()

# Maximum number of messages retained per chat room.
_MAX_MESSAGES_PER_ROOM: int = 1000


def _validate_inputs(chat_room_id: str, sender: str, chat_message: str) -> None:
    """Validate function arguments."""
    if not isinstance(chat_room_id, str) or not chat_room_id:
        raise ValueError("chat_room_id must be a non-empty string")
    if not isinstance(sender, str) or not sender:
        raise ValueError("sender must be a non-empty string")
    if not isinstance(chat_message, str):
        raise ValueError("chat_message must be a string")
    # Basic content length check to avoid extremely long messages
    if len(chat_message) > 10_000:
        raise ValueError("chat_message is too long")


def send_message_to_chat(chat_room_id: str, sender: str, chat_message: str) -> bool:
    """
    Append a message to the specified chat room.

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
        ``True`` if the message was added successfully, ``False`` if it
        would exceed the per‑room limit.

    Notes
    -----
    - The function is thread‑safe.
    - Messages are stored as dictionaries containing ``sender``, ``message``,
      and a UTC timestamp.
    - If the chat room does not exist, it is created automatically.

    Raises
    ------
    ValueError
        If any argument fails validation.
    """
    _validate_inputs(chat_room_id, sender, chat_message)

    new_msg = {
        "sender": sender,
        "message": chat_message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    with _chat_lock:
        # Create room if it doesn't exist
        if chat_room_id not in chat_rooms:
            chat_rooms[chat_room_id] = []

        room_msgs = chat_rooms[chat_room_id]

        # Enforce maximum size
        if len(room_msgs) >= _MAX_MESSAGES_PER_ROOM:
            return False

        room_msgs.append(new_msg)
    return True