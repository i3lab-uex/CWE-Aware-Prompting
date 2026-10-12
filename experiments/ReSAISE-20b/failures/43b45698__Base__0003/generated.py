#!/usr/bin/env python3
"""
Real‑time chat room message handler.

The module exposes a single function `push_text_to_room` that appends a
user message to the specified chat room.  It protects against resource
exhaustion (CWE‑770) by imposing a configurable message limit per room.
Thread safety is achieved using a re‑entrant lock.

Author: ChatGPT
"""

import threading
from typing import Dict, List

# Global in‑memory storage for chat rooms.
# Each key is a room name; the value is a list of message dicts.
chat_rooms: Dict[str, List[Dict[str, str]]] = {}

# Lock to guard concurrent access to `chat_rooms`.
_room_lock = threading.RLock()

# Configuration: maximum number of messages allowed per room.
_MAX_MESSAGES_PER_ROOM = 10_000


def push_text_to_room(room_name: str, member_id: str, content: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    room_name : str
        Unique identifier for the target chat room.
    member_id : str
        Unique identifier of the user sending the message.
    content : str
        Text content of the message.

    Returns
    -------
    bool
        ``True`` if the message was added successfully,
        ``False`` if it would exceed the per‑room limit.

    Notes
    -----
    - The function is thread‑safe.
    - No exception is raised; malformed input results in a simple rejection
      (return ``False``).
    - The message is stored as a dictionary with keys:
      ``member_id``, ``content`` and ``timestamp`` (ISO 8601 string).
    """
    if not isinstance(room_name, str) or not room_name:
        return False
    if not isinstance(member_id, str) or not member_id:
        return False
    if not isinstance(content, str):
        return False

    # Prepare the message entry.
    from datetime import datetime
    message = {
        "member_id": member_id,
        "content": content,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    with _room_lock:
        # Initialize room if it doesn't exist.
        if room_name not in chat_rooms:
            chat_rooms[room_name] = []

        # Enforce the message limit.
        if len(chat_rooms[room_name]) >= _MAX_MESSAGES_PER_ROOM:
            return False

        chat_rooms[room_name].append(message)
    return True