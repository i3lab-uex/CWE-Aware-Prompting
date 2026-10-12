#!/usr/bin/env python3
"""
Chat message insertion module.

This module provides a thread‑safe helper for appending messages to chat rooms.
It enforces a hard limit on the number of stored messages per room and protects
the shared data structure with a lock to prevent race conditions.
"""

from __future__ import annotations

import datetime
import threading
from typing import Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Global storage for chat rooms.  Each entry maps a `chat_id` to a list of
# messages.  A message is represented as a tuple:
#
#   (timestamp: datetime.datetime, sender_id: str, msg: str)
#
# The global dictionary is protected by a lock to avoid concurrent modification.
# --------------------------------------------------------------------------- #
chat_rooms: Dict[str, List[Tuple[datetime.datetime, str, str]]] = {}
_chat_lock = threading.RLock()

# Maximum number of messages that a single chat room can retain.
MAX_MESSAGES_PER_CHAT = 1_000


def insert_message_in_chat(chat_id: str, sender_id: str, msg: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_id : str
        Unique identifier for the target chat room.
    sender_id : str
        Unique identifier of the message sender.
    msg : str
        The actual text content of the message.

    Returns
    -------
    bool
        ``True`` if the message was successfully added.
        ``False`` if the room already reached its maximum capacity.

    Notes
    -----
    * The function is fully thread‑safe; it acquires a re‑entrant lock
      before modifying the global ``chat_rooms`` dictionary.
    * Messages are stored with a UTC timestamp for consistency across
      distributed systems.
    * No exceptions are raised; invalid inputs (e.g., empty strings) are
      treated as valid messages.
    """
    # Normalise inputs (strip whitespace) – this prevents accidental
    # storage of messages that are effectively empty.
    chat_id = chat_id.strip()
    sender_id = sender_id.strip()
    msg = msg.strip()

    if not chat_id:
        # Invalid chat identifier – silently reject.
        return False

    now = datetime.datetime.utcnow()

    with _chat_lock:
        # Retrieve or create the message list for this chat room.
        msgs = chat_rooms.setdefault(chat_id, [])

        if len(msgs) >= MAX_MESSAGES_PER_CHAT:
            # Exceeded the maximum allowed messages – reject.
            return False

        # Append the new message tuple.
        msgs.append((now, sender_id, msg))

    return True