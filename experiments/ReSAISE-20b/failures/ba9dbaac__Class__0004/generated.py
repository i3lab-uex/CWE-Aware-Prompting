import re

def extract_words_from_string(text: str) -> list:
    """
    Tokenize the input string into a list of words using regular expressions.

    Args:
        text (str): The raw user-provided string to be tokenized.

    Returns:
        list: A list of words extracted from the input text.

    Raises:
        ValueError: If the input is not a string, if it is too large,
                    or if an unexpected error occurs during processing.
    """
    # Basic type check
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Prevent uncontrolled resource consumption (CWE-400)
    MAX_LENGTH = 10_000_000  # 10 million characters
    if len(text) > MAX_LENGTH:
        raise ValueError(f"Input text exceeds the maximum allowed length of {MAX_LENGTH} characters")

    try:
        # Use a simple word pattern that captures alphanumeric sequences
        words = re.findall(r'\b\w+\b', text)
    except Exception as exc:
        # Wrap any regex-related errors in a ValueError
        raise ValueError(f"Failed to extract words: {exc}") from exc

    return words