#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chat room message insertion module.

This module defines the `insert_message_in_channel` function, which safely
appends a new message to a chat room while respecting per‑room limits and
avoiding race conditions.  It protects the shared `chat_rooms` resource using a
threading lock to prevent improper control of the resource through its
lifetime (CWE‑664).
"""

from __future__ import annotations

import datetime
import threading
from typing import Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Global storage for chat rooms.
#   * Key: channel name (str)
#   * Value: tuple of (list_of_messages, lock_for_this_channel)
#
# Each message is a dictionary:
#   {
#       "participant_id": str,
#       "body": str,
#       "timestamp": datetime.datetime
#   }
#
# The lock ensures that concurrent inserts into the same channel are serialized.
# --------------------------------------------------------------------------- #

MAX_MESSAGES_PER_CHANNEL = 10_000  # Adjust as needed for your system

chat_rooms: Dict[str, Tuple[List[dict], threading.Lock]] = {}
_global_lock = threading.Lock()  # protects creation of new channel entries


def _get_or_create_channel(channel_name: str) -> Tuple[List[dict], threading.Lock]:
    """
    Retrieve the message list and lock for a channel, creating them if necessary.
    This helper is thread‑safe.
    """
    with _global_lock:
        if channel_name not in chat_rooms:
            # Create a new channel entry with its own lock
            chat_rooms[channel_name] = ([], threading.Lock())
        return chat_rooms[channel_name]


def insert_message_in_channel(channel_name: str, participant_id: str, msg_body: str) -> bool:
    """
    Append a new message to the specified chat room.

    Parameters
    ----------
    channel_name : str
        Unique identifier for the target chat room.
    participant_id : str
        Identifier of the user sending the message.
    msg_body : str
        The textual content of the message.

    Returns
    -------
    bool
        True if the message was successfully added, False if it was rejected
        because the channel has reached its maximum capacity.

    Notes
    -----
    * The function is thread‑safe and prevents race conditions on the global
      `chat_rooms` dictionary.
    * No exceptions are raised; invalid inputs simply result in a rejection
      (False return value).
    """
    # Basic input validation
    if not all(isinstance(arg, str) for arg in (channel_name, participant_id, msg_body)):
        return False

    # Retrieve channel resources
    messages, lock = _get_or_create_channel(channel_name)

    with lock:
        # Enforce channel message limit
        if len(messages) >= MAX_MESSAGES_PER_CHANNEL:
            return False

        # Construct the message payload
        message = {
            "participant_id": participant_id,
            "body": msg_body,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }

        messages.append(message)
        return True


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    assert insert_message_in_channel("room1", "user123", "Hello, world!") is True
    # Fill the channel to its limit for demonstration
    for _ in range(MAX_MESSAGES_PER_CHANNEL):
        insert_message_in_channel("room1", "user456", "spam")
    # Next insertion should fail
    assert insert_message_in_channel("room1", "user789", "too many") is False
    print(f"Room 'room1' has {len(chat_rooms['room1'][0])} messages.")