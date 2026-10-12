import threading

# Global store for chat rooms: {channel_name: [(participant_id, msg_body), ...]}
chat_rooms = {}
# A lock to protect concurrent access to the global chat_rooms dictionary
_chat_lock = threading.RLock()

# Maximum number of messages retained per channel to avoid unbounded growth
_MAX_MESSAGES_PER_CHANNEL = 1000

def insert_message_in_channel(channel_name: str, participant_id: str, msg_body: str) -> bool:
    """
    Append a new message to the specified chat channel.

    Parameters
    ----------
    channel_name : str
        Unique identifier for the target chat room.
    participant_id : str
        Unique identifier of the user sending the message.
    msg_body : str
        Text content of the message.

    Returns
    -------
    bool
        True if the message was added, False if it was rejected due to exceeding limits.
    """
    # Basic validation
    if not channel_name or not participant_id:
        return False

    with _chat_lock:
        # Retrieve or create the channel's message list
        messages = chat_rooms.setdefault(channel_name, [])

        # Enforce per-channel message limit
        if len(messages) >= _MAX_MESSAGES_PER_CHANNEL:
            # Optionally, could remove oldest messages here to make space
            return False

        # Append the new message tuple
        messages.append((participant_id, msg_body))
    return True