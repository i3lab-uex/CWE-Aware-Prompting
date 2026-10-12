import re

def analyze_user_string(input_text: str) -> list:
    """
    Split the given input string into individual words and return them as a list.

    Parameters
    ----------
    input_text : str
        The string provided by the user to be analyzed.

    Returns
    -------
    list
        A list of words extracted from the input string. Words are defined as sequences of
        alphanumeric characters and underscores (i.e., matches the regex \w+).

    Raises
    ------
    ValueError
        If `input_text` is not a string, or if it cannot be processed (e.g., empty input).
    """
    # Validate the type of the input
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string.")

    # Strip leading/trailing whitespace; empty or whitespace-only strings are invalid
    stripped = input_text.strip()
    if not stripped:
        raise ValueError("Input string is empty or contains only whitespace.")

    # Use a compiled regex pattern for efficiency and clarity
    word_pattern = re.compile(r"\b\w+\b")

    # Find all non-overlapping matches
    words = word_pattern.findall(stripped)

    if not words:
        raise ValueError("No valid words found in the input string.")

    return words