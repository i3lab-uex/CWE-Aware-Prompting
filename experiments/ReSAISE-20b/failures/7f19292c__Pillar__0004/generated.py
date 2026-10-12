#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chat room message appender.

This module exposes a single public function, :func:`append_message_to_chat`,
which inserts a new message into the conversation history of a given chat
room.  The implementation guards against uncontrolled growth by enforcing a
maximum message count per room and protects concurrent access with a
thread‑synchronisation primitive.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated by
ensuring that the resource (the message list for each room) is never left in an
inconsistent or partially updated state.  All modifications are performed
under a lock and the list is never exposed directly to callers.

"""

from __future__ import annotations

import datetime
import threading
from typing import Dict, List, Any

# Global data structures ----------------------------------------------------

# Mapping from room code to its conversation history.
chat_rooms: Dict[str, List[Dict[str, Any]]] = {}

# Mapping from room code to a lock protecting that room's message list.
_room_locks: Dict[str, threading.Lock] = {}

# Maximum number of messages allowed per room.  Messages beyond this limit
# are silently rejected to keep the resource bounded.
_MAX_MESSAGES_PER_ROOM: int = 1000


# Helper functions ----------------------------------------------------------

def _get_room_lock(room_code: str) -> threading.Lock:
    """
    Return a lock object for the given room, creating one if necessary.
    The creation is protected by a global lock to avoid race conditions during
    first access.

    Parameters
    ----------
    room_code : str
        The identifier of the chat room.

    Returns
    -------
    threading.Lock
        A lock guarding access to the room's message list.
    """
    # Global lock for initializing per‑room locks.
    global _global_lock
    with _global_lock:
        if room_code not in _room_locks:
            _room_locks[room_code] = threading.Lock()
        return _room_locks[room_code]


# Global lock used only during the creation of per‑room locks.
_global_lock = threading.Lock()


# Public API ---------------------------------------------------------------

def append_message_to_chat(room_code: str, user_identifier: str,
                           msg_text: str) -> bool:
    """
    Append a message to the conversation history of the specified chat room.

    The function performs minimal validation: it checks that the target room
    exists and that the message count does not exceed :data:`_MAX_MESSAGES_PER_ROOM`.
    All modifications are performed under a lock to prevent race conditions
    in concurrent environments.

    Parameters
    ----------
    room_code : str
        Identifier of the target chat room.
    user_identifier : str
        Unique identifier of the message author.
    msg_text : str
        Textual content of the message.

    Returns
    -------
    bool
        ``True`` if the message was appended successfully,
        ``False`` if the room does not exist or the message limit is reached.
    """
    # Basic sanity checks
    if not isinstance(room_code, str) or not room_code:
        return False
    if not isinstance(user_identifier, str) or not user_identifier:
        return False
    if not isinstance(msg_text, str):
        return False

    # Acquire the lock for this room to guard against concurrent modifications.
    lock = _get_room_lock(room_code)
    with lock:
        if room_code not in chat_rooms:
            # Room does not exist – message cannot be appended.
            return False

        room_history = chat_rooms[room_code]

        if len(room_history) >= _MAX_MESSAGES_PER_ROOM:
            # Reached the configured message limit.
            return False

        # Construct the new message record with a UTC timestamp.
        message = {
            "user": user_identifier,
            "text": msg_text,
            "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
        }

        # Append the message to the room's history.
        room_history.append(message)

    return True


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example usage: create a room and add messages.
    chat_rooms["room123"] = []

    assert append_message_to_chat("room123", "alice", "Hello, world!") is True
    assert len(chat_rooms["room123"]) == 1

    # Exceeding the limit test (using a small limit for demonstration).
    _MAX_MESSAGES_PER_ROOM = 1
    assert append_message_to_chat("room123", "bob", "Another message") is False