#!/usr/bin/env python3
"""
Chat message handling module.

This module implements a simple in‑memory chat room history with safety checks
to prevent uncontrolled resource growth (CWE‑770).  Each room is limited to a
maximum number of stored messages.  A thread lock protects concurrent writes.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Tuple

# Global dictionary mapping room_id to a list of messages.
# Each message is stored as a tuple: (user_id, message_text)
chat_rooms: Dict[str, List[Tuple[str, str]]] = {}

# Lock to ensure thread‑safe updates to chat_rooms.
_chat_lock = threading.Lock()

# Maximum number of messages retained per room (capped to prevent unlimited growth).
_MAX_MESSAGES_PER_ROOM = 10_000


def add_message_to_chat(room_id: str, user_id: str, message: str) -> bool:
    """
    Add a new message to the specified chat room.

    Parameters
    ----------
    room_id : str
        Identifier of the chat room.
    user_id : str
        Identifier of the user sending the message.
    message : str
        The content of the message.

    Returns
    -------
    bool
        True if the message was added successfully, False otherwise.
    """
    # Basic validation: ensure inputs are non‑empty strings.
    if not all(isinstance(arg, str) and arg for arg in (room_id, user_id, message)):
        return False

    # Use the lock to protect shared data.
    with _chat_lock:
        room = chat_rooms.setdefault(room_id, [])

        # Enforce message limit per room.
        if len(room) >= _MAX_MESSAGES_PER_ROOM:
            # Optionally, drop the oldest message to make room for the new one.
            # This keeps history bounded without rejecting messages outright.
            # Uncomment the following line if you prefer to drop oldest messages:
            # room.pop(0)
            return False

        # Append the new message.
        room.append((user_id, message))
    return True