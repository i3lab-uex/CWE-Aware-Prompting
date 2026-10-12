#!/usr/bin/env python3
"""
A simple in‑memory chat message store with basic safeguards against uncontrolled resource consumption.
"""

import threading
from datetime import datetime

# Global dictionary to hold chat rooms. Each room_id maps to a list of message dicts.
chat_rooms = {}
# Lock for thread‑safe access to the global chat_rooms dictionary.
_chat_lock = threading.RLock()

# Maximum number of messages retained per room to prevent unbounded memory usage.
_MAX_MESSAGES_PER_ROOM = 1_000


def _validate_input(value: str, name: str) -> bool:
    """
    Basic validation to ensure the input is a non‑empty string and does not contain
    suspicious characters that might lead to injection attacks or other issues.
    """
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if not stripped:
        return False
    # Reject strings that contain control characters or line breaks in the room_id/user_id.
    if name in ("room_id", "user_id"):
        if any(c in stripped for c in "\n\r\t"):
            return False
    # For the message itself we allow line breaks but strip leading/trailing whitespace.
    return True


def add_message_to_chat(room_id: str, user_id: str, message: str) -> bool:
    """
    Adds a new message to the specified chat room.

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
        True if the message was added successfully, False otherwise.
    """
    # Input validation
    if not (_validate_input(room_id, "room_id") and
            _validate_input(user_id, "user_id") and
            isinstance(message, str)):
        return False

    # Prepare the message payload
    msg_payload = {
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message.strip()
    }

    with _chat_lock:
        # Retrieve or create the room's history
        room_history = chat_rooms.setdefault(room_id, [])

        # Append the new message
        room_history.append(msg_payload)

        # Enforce maximum history size per room
        if len(room_history) > _MAX_MESSAGES_PER_ROOM:
            # Remove oldest messages to keep the size within limits
            del room_history[0 : len(room_history) - _MAX_MESSAGES_PER_ROOM]

    return True