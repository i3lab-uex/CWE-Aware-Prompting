import re

def parse_user_input(text: str) -> list[str]:
    """
    Splits the input string into words using regular expressions.

    Args:
        text: The user-provided input string.

    Returns:
        A list of words extracted from the input.

    Raises:
        ValueError: If the input is not a string or if regex processing fails.
    """
    # Validate input type
    if not isinstance(text, str):
        raise ValueError(f"Expected a string, got {type(text).__name__}")

    try:
        # Use regex to capture word tokens (alphanumeric + underscore)
        words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    except Exception as exc:
        # Wrap any regex-related exception into ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words