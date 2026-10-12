import re

def parse_text_input(provided_input):
    """
    Parse a raw text input and extract individual words.

    Args:
        provided_input (str): Raw user-provided text.

    Returns:
        list[str]: A list of extracted words in the order they appear.

    Raises:
        ValueError: If the input is not a string or if regex processing fails.
    """
    # Validate input type
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    try:
        # Compile the regex pattern once per call (safe for small inputs)
        word_pattern = re.compile(r"\b\w+\b", flags=re.UNICODE)
    except re.error as exc:
        # Re-raise a ValueError with context
        raise ValueError(f"Failed to compile regex pattern: {exc}") from exc

    try:
        # Find all word matches
        words = word_pattern.findall(provided_input)
    except re.error as exc:
        # Handle any runtime regex errors
        raise ValueError(f"Regex matching failed: {exc}") from exc

    return words