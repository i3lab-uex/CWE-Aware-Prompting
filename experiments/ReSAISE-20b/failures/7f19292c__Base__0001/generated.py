#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A simple in‑memory chat room manager that safely appends messages to a
conversation log while guarding against unlimited growth (CWE‑770).

The module exposes the function `append_message_to_chat` which accepts
a room identifier, a user identifier and a message string.  If the
room exists and its history has not exceeded `MAX_MESSAGES_PER_ROOM`,
the new message is appended to the room's log and the function
returns `True`.  Otherwise it returns `False` without modifying the
log.

All state is kept in a global dictionary protected by a re‑entrant lock
to avoid race conditions in concurrent environments.
"""

from __future__ import annotations

import threading
from datetime import datetime
from typing import Dict, List, Tuple

# ----------------------------------------------------------------------
# Configuration constants
# ----------------------------------------------------------------------
MAX_MESSAGES_PER_ROOM: int = 1_000          # Maximum messages allowed per room
MESSAGE_LOG_MAX_LENGTH: int = MAX_MESSAGES_PER_ROOM

# ----------------------------------------------------------------------
# Global data structures
# ----------------------------------------------------------------------
# Mapping: room_code -> list of (timestamp, user_id, message_text)
chat_rooms: Dict[str, List[Tuple[datetime, str, str]]] = {}
# A lock to protect concurrent access to `chat_rooms`
_chat_lock: threading.RLock = threading.RLock()


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def append_message_to_chat(
    room_code: str,
    user_identifier: str,
    msg_text: str
) -> bool:
    """
    Append a new message to the conversation log of the specified chat room.

    Parameters
    ----------
    room_code : str
        Unique identifier for the target chat room.
    user_identifier : str
        Identifier of the message author.
    msg_text : str
        The textual content of the message.

    Returns
    -------
    bool
        ``True`` if the message was added successfully; ``False`` if the
        room has reached its maximum message capacity or if any of the
        inputs are invalid.
    """
    # Basic input validation – reject empty strings
    if not room_code or not user_identifier or msg_text is None:
        return False

    # Normalise inputs to avoid accidental key mismatches
    room_key = room_code.strip()
    user_id = user_identifier.strip()

    if not room_key or not user_id:
        return False

    # Acquire the lock to ensure thread safety
    with _chat_lock:
        room_log = chat_rooms.setdefault(room_key, [])

        # Enforce the message limit
        if len(room_log) >= MESSAGE_LOG_MAX_LENGTH:
            return False

        # Append the new message with a timestamp
        room_log.append((datetime.utcnow(), user_id, msg_text))
        return True


# ----------------------------------------------------------------------
# Optional helper functions (not required by the task but useful for testing)
# ----------------------------------------------------------------------
def get_chat_log(room_code: str) -> List[Tuple[datetime, str, str]]:
    """Retrieve the message history for a room (read‑only)."""
    with _chat_lock:
        return list(chat_rooms.get(room_code, []))


def clear_chat_room(room_code: str) -> None:
    """Remove all messages from a room."""
    with _chat_lock:
        chat_rooms.pop(room_code, None)


# ----------------------------------------------------------------------
# Unit test example (executed only when run as a script)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import unittest

    class TestAppendMessage(unittest.TestCase):
        def setUp(self):
            clear_chat_room("room1")

        def test_append_success(self):
            self.assertTrue(append_message_to_chat("room1", "alice", "Hello!"))
            log = get_chat_log("room1")
            self.assertEqual(len(log), 1)
            self.assertEqual(log[0][1], "alice")
            self.assertEqual(log[0][2], "Hello!")

        def test_limit_enforcement(self):
            for i in range(MAX_MESSAGES_PER_ROOM):
                self.assertTrue(append_message_to_chat("room1", f"user{i}", "msg"))
            # Next message should fail
            self.assertFalse(append_message_to_chat("room1", "userX", "overflow"))

        def test_invalid_inputs(self):
            self.assertFalse(append_message_to_chat("", "bob", "hi"))
            self.assertFalse(append_message_to_chat("room1", "", "hi"))
            self.assertFalse(append_message_to_chat("room1", "bob", None))

    unittest.main()