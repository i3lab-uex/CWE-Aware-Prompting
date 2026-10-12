#!/usr/bin/env python3
"""
Chat message addition module.

The `send_message_to_chat` function safely appends a new message to the
history of a specified chat room while enforcing a hard limit on the
number of stored messages per room.  This mitigates CWE‑770 by preventing
unbounded memory consumption.

The module uses a global dictionary `chat_rooms` that maps each chat room
identifier to its list of message records.  A thread‑safe lock protects
concurrent modifications.
"""

from __future__ import annotations

import datetime
import threading
from typing import Dict, List

# --------------------------------------------------------------------------- #
# Global storage for chat rooms.  Each room maps to a list of message dicts.
# --------------------------------------------------------------------------- #
chat_rooms: Dict[str, List[Dict]] = {}
_lock = threading.RLock()

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
MAX_MESSAGES_PER_ROOM: int = 1000   # Maximum messages retained per chat room


def _current_timestamp() -> str:
    """Return the current UTC timestamp in ISO‑8601 format."""
    return datetime.datetime.utcnow().isoformat() + "Z"


def send_message_to_chat(chat_room_id: str, sender: str, chat_message: str) -> bool:
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

    Notes
    -----
    * The function is thread‑safe.
    * No exception is raised; failures are indicated by the return value.
    """
    if not isinstance(chat_room_id, str) or not isinstance(sender, str) or not isinstance(chat_message, str):
        # Defensive: reject malformed input silently.
        return False

    message_record = {
        "sender": sender,
        "content": chat_message,
        "timestamp": _current_timestamp(),
    }

    with _lock:
        room = chat_rooms.setdefault(chat_room_id, [])

        # Enforce the message limit
        if len(room) >= MAX_MESSAGES_PER_ROOM:
            return False

        room.append(message_record)
    return True