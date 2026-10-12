import re
from typing import List

def transform_user_text(text_input: str) -> List[str]:
    """
    Extract words from a user-provided string using regular expressions.

    Parameters
    ----------
    text_input : str
        The raw input string from which words will be extracted.

    Returns
    -------
    List[str]
        A list containing all the words found in ``text_input``.

    Raises
    ------
    ValueError
        If ``text_input`` is not a string, or if any error occurs during
        regular expression compilation/execution.
    """
    # Validate input type early to avoid ambiguous errors later
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string")

    try:
        # Compile the regex once; this also checks for syntax errors
        word_pattern = re.compile(r"\b\w+\b")
    except re.error as exc:
        # Wrap regex errors in a ValueError for consistency
        raise ValueError(f"Invalid regular expression: {exc}") from exc

    try:
        # Find all word tokens in the input string
        words = word_pattern.findall(text_input)
    except Exception as exc:
        # Catch unexpected runtime errors and re-raise as ValueError
        raise ValueError(f"Error during word extraction: {exc}") from exc

    return words