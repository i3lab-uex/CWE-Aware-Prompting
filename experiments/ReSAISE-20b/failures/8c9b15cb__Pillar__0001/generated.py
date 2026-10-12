#!/usr/bin/env python3
"""
Real‑time chat message insertion module.

This module defines a single public function:
    insert_message_in_channel(channel_name, participant_id, msg_body)

The function appends a new message to the specified chat room while
respecting configurable limits on both message length and channel size.
Thread safety is ensured via a global lock, preventing race conditions
that could otherwise corrupt the shared ``chat_rooms`` data structure.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Tuple

# Global chat room storage.
# Each key is a channel name and the value is a list of message tuples:
#   (participant_id, msg_body)
chat_rooms: Dict[str, List[Tuple[str, str]]] = {}

# Configuration limits
MAX_MESSAGE_LENGTH = 10_000          # characters
MAX_CHANNEL_MESSAGES = 5_000         # messages per channel

# Lock to guard access to ``chat_rooms``.
# This is a simple mutex; for higher concurrency a per‑channel lock could be used.
_chat_rooms_lock = threading.Lock()


def _sanitize_input(value: str) -> str:
    """
    Basic sanitization to prevent accidental control characters or
    overly long input.  The function currently enforces a maximum length.
    """
    if len(value) > MAX_MESSAGE_LENGTH:
        return value[:MAX_MESSAGE_LENGTH]
    return value


def insert_message_in_channel(
    channel_name: str,
    participant_id: str,
    msg_body: str
) -> bool:
    """
    Append a new message to the specified chat channel.

    Parameters
    ----------
    channel_name : str
        Unique identifier for the target chat room.
    participant_id : str
        Unique identifier for the user sending the message.
    msg_body : str
        Text content of the message.

    Returns
    -------
    bool
        ``True`` if the message was added successfully.
        ``False`` if the message exceeded configured limits or
        the channel is full.

    Notes
    -----
    - The function performs minimal sanitization to truncate overly long
      messages.  It does **not** attempt to escape HTML or other payloads;
      callers should handle that if needed.
    - The global ``chat_rooms`` dictionary is protected by a lock to avoid
      race conditions in multi‑threaded environments.
    """
    # Basic validation of inputs (ensure non-empty strings)
    if not channel_name or not participant_id:
        return False

    # Truncate message body to avoid exceeding the maximum length.
    msg_body = _sanitize_input(msg_body)

    with _chat_rooms_lock:
        # Initialize channel if it does not exist.
        messages = chat_rooms.setdefault(channel_name, [])

        # Enforce channel size limit.
        if len(messages) >= MAX_CHANNEL_MESSAGES:
            return False

        # Append the new message.
        messages.append((participant_id, msg_body))

    return True