import re

# Maximum number of words allowed to prevent uncontrolled resource consumption.
MAX_WORDS = 10_000

def transform_user_text(text_input: str) -> list[str]:
    """
    Parse a user-provided string, extracting individual words and compiling them into a list.

    Args:
        text_input: Raw text input from the user. Must be a string.

    Returns:
        A list of words extracted from `text_input`.

    Raises:
        ValueError: If the input is not a string, is empty after stripping,
                    or if the number of extracted words exceeds MAX_WORDS.
    """
    # Validate input type
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    # Strip leading/trailing whitespace
    stripped = text_input.strip()
    if not stripped:
        raise ValueError("Input string is empty or contains only whitespace")

    # Extract words using a simple regex. This pattern captures sequences of
    # alphanumeric characters and underscores as "words".
    words = re.findall(r"\b\w+\b", stripped)

    # Check for uncontrolled resource consumption
    if len(words) > MAX_WORDS:
        raise ValueError(f"Too many words ({len(words)}); limit is {MAX_WORDS}")

    return words