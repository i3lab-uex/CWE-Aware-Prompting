import re

# Maximum number of words allowed in the input to avoid uncontrolled resource consumption.
MAX_WORDS = 10_000

def process_user_input(user_input: str) -> list:
    """
    Splits the user input into words using a regular expression and returns
    them as a list. Raises ValueError if the input is invalid or if the
    number of extracted words exceeds MAX_WORDS.

    Parameters:
        user_input (str): The raw string provided by the user.

    Returns:
        list[str]: A list of words extracted from `user_input`.

    Raises:
        ValueError: If the input is not a string, if it cannot be processed,
                    or if the word count exceeds MAX_WORDS.
    """
    # Validate type
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string.")

    # Strip leading/trailing whitespace to avoid creating empty words
    stripped_input = user_input.strip()

    # Use a simple word pattern; this avoids heavy regex backtracking
    try:
        words = re.findall(r'\b\w+\b', stripped_input)
    except Exception as exc:
        # Catch any regex-related errors and re‑raise as ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    # Enforce a limit on the number of words to protect against resource exhaustion
    if len(words) > MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)}); "
                         f"maximum allowed is {MAX_WORDS}.")

    return words