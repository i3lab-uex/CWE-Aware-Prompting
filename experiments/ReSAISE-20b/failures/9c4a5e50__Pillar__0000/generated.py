# -*- coding: utf-8 -*-
"""
Chat message insertion module.

This module defines `insert_message_in_chat`, which safely appends a new
message to the specified chat room.  It enforces a maximum number of
messages per room and uses a thread‑safe lock to avoid race conditions.
"""

from __future__ import annotations

import threading
from datetime import datetime
from typing import Dict, List, Tuple

# Global in‑memory storage for chat rooms.
# Each key is a chat_id and the value is a list of message tuples:
# (timestamp, sender_id, msg)
chat_rooms: Dict[str, List[Tuple[datetime, str, str]]] = {}

# Maximum number of messages retained per chat room.
_MAX_MESSAGES_PER_ROOM: int = 1000

# Lock to serialize access to the global `chat_rooms` dictionary.
_chat_lock = threading.RLock()


def insert_message_in_chat(chat_id: str, sender_id: str, msg: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    chat_id : str
        Unique identifier for the target chat room.
    sender_id : str
        Unique identifier for the message sender.
    msg : str
        The actual text content of the message.

    Returns
    -------
    bool
        ``True`` if the message was successfully added; ``False`` if the
        insertion would exceed the per‑room limit and therefore was rejected.

    Notes
    -----
    - Thread‑safe via a re‑entrant lock.
    - Does not raise exceptions; all errors are silently handled and
      result in ``False``.
    """
    # Basic validation: reject empty messages or identifiers
    if not all([chat_id, sender_id, msg]):
        return False

    try:
        with _chat_lock:
            # Retrieve or create the message list for this chat room
            messages = chat_rooms.setdefault(chat_id, [])

            # Enforce maximum message limit
            if len(messages) >= _MAX_MESSAGES_PER_ROOM:
                return False

            # Append the new message with a timestamp
            messages.append((datetime.utcnow(), sender_id, msg))
        return True

    except Exception:
        # Any unexpected exception is treated as a failure
        return False


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    assert insert_message_in_chat("room1", "user123", "Hello, world!") is True
    assert insert_message_in_chat("room1", "", "Missing sender") is False