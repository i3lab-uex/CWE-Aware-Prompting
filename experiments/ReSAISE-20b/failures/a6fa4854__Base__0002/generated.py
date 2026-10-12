#!/usr/bin/env python3
"""
A thread‑safe implementation of a chat message posting function that protects
against unbounded memory consumption (CWE‑770).
"""

from __future__ import annotations

import threading
from typing import Dict, List

# Global storage for chat rooms. Each room maps to a list of (user, message) tuples.
chat_rooms: Dict[str, List[tuple]] = {}
# A lock to guard concurrent modifications to the global structure.
_chat_lock = threading.RLock()

# Maximum number of messages allowed per chat room. Adjust as needed.
_MAX_MESSAGES_PER_ROOM = 10_000


def post_msg_in_chat(chat_room: str, user: str, new_message: str) -> bool:
    """
    Append a message to the specified chat room.

    Parameters
    ----------
    chat_room : str
        Identifier for the target chat room.
    user : str
        Identifier of the message sender.
    new_message : str
        Text content of the message.

    Returns
    -------
    bool
        True if the message was added successfully, False if the room has reached its
        maximum capacity and the message is rejected.
    """
    # Basic input validation to avoid storing empty messages or None values.
    if not all(isinstance(x, str) and x for x in (chat_room, user, new_message)):
        return False

    with _chat_lock:
        # Lazily create the room if it does not exist.
        if chat_room not in chat_rooms:
            chat_rooms[chat_room] = []

        # Enforce the per‑room message limit.
        if len(chat_rooms[chat_room]) >= _MAX_MESSAGES_PER_ROOM:
            return False

        # Append the new message as a tuple for future extensibility.
        chat_rooms[chat_room].append((user, new_message))
        return True