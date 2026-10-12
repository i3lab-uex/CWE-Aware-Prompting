#!/usr/bin/env python3
"""
Chat room message logger.

This module provides a thread‑safe function to append messages to a chat
room's conversation log.  It enforces a maximum number of stored messages per
room to avoid uncontrolled growth of the in‑memory data structure.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Tuple

# Global repository of chat rooms.
# Each key is a room identifier and the value is a list of (author, text) tuples.
chat_rooms: Dict[str, List[Tuple[str, str]]] = {}

# Configuration constants
MAX_MESSAGES_PER_ROOM: int = 1_000  # maximum messages kept per room

# A global lock to protect concurrent access to `chat_rooms`.
_chat_lock = threading.RLock()


def log_chat_message(
    target_room: str,
    author_identifier: str,
    text_message: str,
) -> bool:
    """
    Append a message to the conversation log of `target_room`.

    Parameters
    ----------
    target_room : str
        Identifier of the chat room.
    author_identifier : str
        Unique identifier of the message author.
    text_message : str
        Textual content of the message.

    Returns
    -------
    bool
        ``True`` if the message was added to the log.
        ``False`` if the message would exceed the maximum size limit.

    Notes
    -----
    - The function is fully thread‑safe; it uses a re‑entrant lock to guard
      modifications of the global ``chat_rooms`` dictionary.
    - If a room does not exist, it is created automatically.
    - When the number of messages in a room reaches ``MAX_MESSAGES_PER_ROOM``,
      new messages are rejected and the function returns ``False``.
    - No exception is raised; all errors result in a ``False`` return value.
    """
    if not isinstance(target_room, str) or not isinstance(author_identifier, str) or not isinstance(text_message, str):
        # Invalid input types – reject silently.
        return False

    with _chat_lock:
        room_log = chat_rooms.setdefault(target_room, [])

        if len(room_log) >= MAX_MESSAGES_PER_ROOM:
            # Reached capacity – reject the new message.
            return False

        # Append the new message tuple.
        room_log.append((author_identifier, text_message))
        return True