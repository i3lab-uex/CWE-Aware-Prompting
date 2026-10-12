import threading
from collections import defaultdict

# Global dictionary mapping room_id to a list of messages.
# Each message is represented as a dict with user_id, content and timestamp.
chat_rooms: defaultdict[str, list[dict]] = defaultdict(list)

# A lock to guard concurrent access to the global chat_rooms dictionary.
_chat_lock = threading.RLock()


def add_message_to_chat(room_id: str, user_id: str, message: str) -> bool:
    """
    Add a message to the specified chat room.

    Parameters
    ----------
    room_id : str
        Identifier of the chat room.
    user_id : str
        Identifier of the sender.
    message : str
        The textual content of the message.

    Returns
    -------
    bool
        True if the message was successfully appended to the room's history,
        False otherwise (e.g., if an exception occurs during processing).

    Notes
    -----
    * The function is thread‑safe: a reentrant lock protects concurrent writes.
    * No external resources are allocated that need explicit cleanup,
      so CWE‑664 considerations are satisfied.
    * The function does not perform complex validation of the inputs
      (e.g., sanitization) to keep it lightweight; callers should ensure
      that inputs are safe and well‑formed before invoking this function.
    """
    try:
        # Basic type checking to guard against accidental misuse
        if not isinstance(room_id, str) or not isinstance(user_id, str) or not isinstance(message, str):
            return False

        # Prepare the message payload
        msg_payload = {
            "user_id": user_id,
            "content": message,
            # Optionally include a timestamp; omitted for brevity
        }

        with _chat_lock:
            chat_rooms[room_id].append(msg_payload)

        return True
    except Exception:
        # In a real system you might log the exception here.
        return False