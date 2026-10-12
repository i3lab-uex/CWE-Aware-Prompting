#!/usr/bin/env python3
"""
Chat room message appender with basic size limits and thread safety.

The function `append_message_to_room` adds a message to the in‑memory history
of a chat room.  To mitigate CWE‑770 (unbounded resource allocation) each
room is capped at a configurable maximum number of messages.  If the limit
is exceeded the message is rejected and `False` is returned.

Author: <your name>
"""

from __future__ import annotations

import threading
from typing import Dict, List

# --------------------------------------------------------------------------- #
# Global chat rooms storage
# --------------------------------------------------------------------------- #

# Mapping from room tag to a list of (sender_id, message) tuples.
chat_rooms: Dict[str, List[tuple[str, str]]] = {}

# Lock to serialize access to the global `chat_rooms` dictionary.
_chat_lock = threading.RLock()

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Maximum number of messages stored per chat room.
MAX_MESSAGES_PER_ROOM = 1000

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def append_message_to_room(room_tag: str, sender_id: str, chat_message: str) -> bool:
    """
    Append a message to the specified chat room.

    Parameters
    ----------
    room_tag : str
        Unique identifier of the target chat room.
    sender_id : str
        Identifier of the user sending the message.
    chat_message : str
        The text content to be added.

    Returns
    -------
    bool
        ``True`` if the message was stored, ``False`` if it was rejected due to
        exceeding `MAX_MESSAGES_PER_ROOM`.

    Notes
    -----
    - The function is thread‑safe.
    - Input strings are not validated for length or content; callers should
      enforce any domain‑specific checks (e.g., profanity filters).
    - No exception is raised; errors are silently handled and a ``False`` is
      returned if the message cannot be stored.
    """
    # Basic sanity checks: ensure all inputs are strings
    if not isinstance(room_tag, str) or not isinstance(sender_id, str) or not isinstance(chat_message, str):
        return False

    # Use a re‑entrant lock to protect shared data.
    with _chat_lock:
        # Create the room if it does not exist yet
        if room_tag not in chat_rooms:
            chat_rooms[room_tag] = []

        room_history = chat_rooms[room_tag]

        # Enforce the per‑room message limit
        if len(room_history) >= MAX_MESSAGES_PER_ROOM:
            # Reject the new message; could also implement eviction if desired.
            return False

        # Append the new message as a tuple (sender_id, chat_message)
        room_history.append((sender_id, chat_message))

    return True

# --------------------------------------------------------------------------- #
# Example usage (for local testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simple test scenario
    assert append_message_to_room("room1", "userA", "Hello!") is True
    assert len(chat_rooms["room1"]) == 1

    # Fill the room to its limit
    for i in range(MAX_MESSAGES_PER_ROOM - 1):
        append_message_to_room("room1", f"user{i}", "msg")

    # Next message should be rejected
    assert append_message_to_room("room1", "userX", "overflow") is False
    print(f"Room 'room1' contains {len(chat_rooms['room1'])} messages (limit: {MAX_MESSAGES_PER_ROOM}).")