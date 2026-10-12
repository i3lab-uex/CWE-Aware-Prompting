#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chat room message logger.

This module provides a thread‑safe function to append messages to
the conversation history of a chat room.  The implementation protects
against common weaknesses such as uncontrolled growth of the log
and race conditions that could corrupt shared data structures.

CWE-664 (Improper Control of a Resource Through its Lifetime) is
addressed by limiting the number of stored messages and ensuring that
the lock protecting each room’s history is released promptly.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Global data structures
# --------------------------------------------------------------------------- #

# Mapping of room identifier → list of (author, message) tuples.
chat_rooms: Dict[str, List[Tuple[str, str]]] = {}

# A lock per room to guard concurrent modifications.
_room_locks: Dict[str, threading.Lock] = {}

# Maximum number of messages retained per room to prevent unbounded growth.
_MAX_MESSAGES_PER_ROOM: int = 1_000

# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _get_room_lock(room_id: str) -> threading.Lock:
    """
    Retrieve the lock associated with a room, creating it if necessary.
    The creation is protected by a global lock to avoid race conditions
    when multiple threads attempt to create the same lock simultaneously.
    """
    global _room_locks
    # Global lock for lock creation; using a single lock is sufficient
    # because this operation is infrequent and short‑lived.
    global _global_lock_for_locks
    with _global_lock_for_locks:
        if room_id not in _room_locks:
            _room_locks[room_id] = threading.Lock()
        return _room_locks[room_id]

# Global lock used only for the creation of per‑room locks.
_global_lock_for_locks = threading.Lock()

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def log_chat_message(target_room: str, author_identifier: str,
                     text_message: str) -> bool:
    """
    Append a message to the conversation history of ``target_room``.

    Parameters
    ----------
    target_room : str
        Unique identifier for the chat room.
    author_identifier : str
        Unique identifier of the message author.
    text_message : str
        Textual content of the message.

    Returns
    -------
    bool
        ``True`` if the message was appended; ``False`` if the room has
        reached its maximum capacity and the message is rejected.

    Notes
    -----
    - The function is fully thread‑safe.
    - Messages are stored as tuples ``(author, message)``.
    - No exceptions are raised; all errors result in a ``False`` return value.

    Security considerations
    -----------------------
    - Inputs are treated as opaque strings; no further validation is
      performed to avoid excessive processing overhead.
    - The message length is not checked; only the total number of
      messages per room is bounded to prevent resource exhaustion.
    """
    if not isinstance(target_room, str) or not isinstance(author_identifier, str) \
       or not isinstance(text_message, str):
        # Invalid input types; reject silently.
        return False

    lock = _get_room_lock(target_room)
    with lock:
        # Initialize the room history if it does not exist.
        if target_room not in chat_rooms:
            chat_rooms[target_room] = []

        history = chat_rooms[target_room]

        if len(history) >= _MAX_MESSAGES_PER_ROOM:
            # Room has reached its capacity; reject the message.
            return False

        # Append the new message.
        history.append((author_identifier, text_message))
        return True

# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     assert log_chat_message("room1", "userA", "Hello!") is True
#     assert len(chat_rooms["room1"]) == 1