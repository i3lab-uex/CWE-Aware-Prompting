#!/usr/bin/env python3
"""
Chat room message handler.

This module provides a thread‑safe function to add messages to chat rooms
while preventing uncontrolled resource consumption (CWE‑400).  Each room has a
fixed maximum number of stored messages and each message is limited in length.
"""

from __future__ import annotations

import threading
from typing import Dict, List

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

MAX_MESSAGES_PER_ROOM: int = 1000          # Maximum number of messages kept per room
MAX_MESSAGE_LENGTH: int = 10_000           # Maximum characters allowed in a single message

# --------------------------------------------------------------------------- #
# Global state
# --------------------------------------------------------------------------- #

# A mapping from room_id to a list of (user_id, message) tuples.
chat_rooms: Dict[str, List[tuple[str, str]]] = {}

# Lock to guard concurrent access to `chat_rooms`.
_chat_lock = threading.Lock()


def add_message_to_chat(room_id: str, user_id: str, message: str) -> bool:
    """
    Add a message to the specified chat room.

    Parameters
    ----------
    room_id : str
        Identifier of the chat room.
    user_id : str
        Identifier of the user sending the message.
    message : str
        Content of the message.

    Returns
    -------
    bool
        ``True`` if the message was successfully added, otherwise ``False``.

    Notes
    -----
    - If `room_id` or `user_id` is an empty string, the message is rejected.
    - Messages longer than :data:`MAX_MESSAGE_LENGTH` are truncated to that
      length before storage.
    - Each room keeps at most :data:`MAX_MESSAGES_PER_ROOM` messages; older
      entries are discarded in a FIFO manner.
    """
    # Basic input validation
    if not room_id or not user_id:
        return False

    # Enforce message size limit
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH]

    with _chat_lock:
        # Retrieve or create the room's message list
        messages = chat_rooms.setdefault(room_id, [])

        # Append new message
        messages.append((user_id, message))

        # Trim to the maximum allowed length
        if len(messages) > MAX_MESSAGES_PER_ROOM:
            # Remove oldest messages (FIFO)
            del messages[:len(messages) - MAX_MESSAGES_PER_ROOM]

    return True


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simple demo to illustrate functionality
    assert add_message_to_chat("room1", "alice", "Hello!")
    assert add_message_to_chat("room1", "bob", "Hi, Alice.")
    # Attempt to add a message with empty room_id
    assert not add_message_to_chat("", "charlie", "Oops")
    # Verify stored messages
    print(chat_rooms)