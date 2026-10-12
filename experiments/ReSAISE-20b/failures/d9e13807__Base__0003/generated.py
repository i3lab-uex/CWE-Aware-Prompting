#!/usr/bin/env python3
"""
Chat message handling module.

Implements a safe, bounded chat room storage that protects against unbounded
resource consumption (CWE‑770).  Each chat room keeps a list of message tuples.
Messages longer than ``MAX_MESSAGE_LENGTH`` are truncated, and rooms that
exceed ``MAX_MESSAGES_PER_ROOM`` will reject new messages.
"""

from collections import defaultdict
import threading

# --------------------------------------------------------------------------- #
# Configuration – adjust as needed for the target deployment environment.
# --------------------------------------------------------------------------- #

MAX_MESSAGE_LENGTH = 1024          # maximum characters per message
MAX_MESSAGES_PER_ROOM = 1000       # maximum stored messages per chat room

# --------------------------------------------------------------------------- #
# Global storage
# --------------------------------------------------------------------------- #

# A thread‑safe dictionary that maps chat_room_id -> list of (sender, message)
chat_rooms: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)

# A lock to protect concurrent modifications of chat_rooms
_chat_lock = threading.Lock()


def send_message_to_chat(chat_room_id: str, sender: str, chat_message: str) -> bool:
    """
    Append a message to the specified chat room.

    Parameters
    ----------
    chat_room_id : str
        Unique identifier for the target chat room.
    sender : str
        Unique identifier of the message sender.
    chat_message : str
        The text content of the message.

    Returns
    -------
    bool
        ``True`` if the message was added; ``False`` if rejected due to limits.
    """
    # Basic validation
    if not isinstance(chat_room_id, str) or not chat_room_id:
        return False
    if not isinstance(sender, str) or not sender:
        return False
    if not isinstance(chat_message, str):
        return False

    # Enforce message size limit
    if len(chat_message) > MAX_MESSAGE_LENGTH:
        chat_message = chat_message[:MAX_MESSAGE_LENGTH]

    with _chat_lock:
        # Enforce per‑room message count limit
        if len(chat_rooms[chat_room_id]) >= MAX_MESSAGES_PER_ROOM:
            return False

        # Append the message
        chat_rooms[chat_room_id].append((sender, chat_message))
        return True


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simulate adding messages
    for i in range(5):
        success = send_message_to_chat("room1", f"user{i}", f"Hello #{i}")
        print(f"Message {i} added: {success}")

    # Attempt to exceed limit
    for i in range(MAX_MESSAGES_PER_ROOM + 10):
        send_message_to_chat("room2", "userX", f"Msg {i}")

    print(f"Room1 has {len(chat_rooms['room1'])} messages.")
    print(f"Room2 has {len(chat_rooms['room2'])} messages (should be capped at {MAX_MESSAGES_PER_ROOM}).")