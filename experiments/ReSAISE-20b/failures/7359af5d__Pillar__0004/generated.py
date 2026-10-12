#!/usr/bin/env python3
"""
Chat room message handler.

This module provides a thread‑safe helper to add messages to a chat
room.  The global ``chat_rooms`` dictionary holds the message history
for each room, and a lock guarantees that concurrent updates do not
interfere with one another.

Security considerations:
- Input validation prevents empty identifiers or messages.
- The lock is held only for the minimal time required to modify
  shared state, reducing contention.
- The function does not expose any internal data structures,
  returning only a boolean status flag.

CWE‑664 (Improper Control of a Resource Through its Lifetime) is
mitigated by ensuring that the lock is always released via a
context manager.
"""

from __future__ import annotations

import logging
import threading
from typing import Dict, List

# Configure module‑level logger (no external dependencies)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Global data structures
chat_rooms: Dict[str, List[Dict[str, str]]] = {}
_lock = threading.Lock()


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
        ``True`` if the message was successfully added, ``False``
        otherwise (e.g., invalid input).

    Notes
    -----
    The function is thread‑safe and uses a lock to protect the shared
    ``chat_rooms`` dictionary.  No exceptions are raised; invalid
    input results in a ``False`` return value.
    """
    # Basic validation: ensure all inputs are non‑empty strings
    if not (room_id and isinstance(room_id, str)):
        logging.debug("add_message_to_chat: invalid room_id")
        return False
    if not (user_id and isinstance(user_id, str)):
        logging.debug("add_message_to_chat: invalid user_id")
        return False
    if not (message and isinstance(message, str)):
        logging.debug("add_message_to_chat: invalid message")
        return False

    # Prepare the message record
    msg_record = {"user_id": user_id, "message": message}

    # Safely modify the shared structure
    with _lock:
        if room_id not in chat_rooms:
            # Initialize a new message list for the room
            chat_rooms[room_id] = []
        try:
            chat_rooms[room_id].append(msg_record)
            logging.debug(
                "Message added to room %s: user=%s, msg=%r",
                room_id,
                user_id,
                message,
            )
        except Exception as exc:  # pragma: no cover
            logging.error(
                "Failed to add message to room %s: %s",
                room_id,
                exc,
            )
            return False

    return True


# Example usage (remove or guard with if __name__ == "__main__" in production)
if __name__ == "__main__":
    assert add_message_to_chat("room1", "alice", "Hello, world!") is True
    assert add_message_to_chat("", "bob", "Test") is False
    print("Current chat rooms:", chat_rooms)