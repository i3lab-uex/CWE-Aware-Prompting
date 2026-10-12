import threading

# Global activity log and its maximum allowed size
activity_log = []
_MAX_LOG_SIZE = 10_000          # Arbitrary limit to prevent uncontrolled growth
_log_lock = threading.Lock()    # Protects concurrent access

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Append a user action record to the global activity_log.

    Args:
        user_identifier (str): Unique identifier for the user.
        event (str): Description of the action performed.

    Returns:
        bool: True if logged successfully, False if the log would exceed its
              configured maximum size.
    """
    # Validate inputs are strings (basic safety)
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        raise TypeError("user_identifier and event must be strings")

    # Create a record tuple (timestamp optional could be added)
    record = (user_identifier, event)

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject new entries once the log reaches its capacity
            return False

        activity_log.append(record)
        return True