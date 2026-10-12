import re

# Maximum allowed input length to mitigate uncontrolled resource consumption (CWE-400)
_MAX_INPUT_LENGTH = 10**6  # 1 MB


def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extract words from a raw user input string using regular expressions.

    Parameters
    ----------
    raw_input : str
        The raw text input from the user.

    Returns
    -------
    list[str]
        A list containing all words found in ``raw_input``.
        Words are defined as contiguous sequences of alphanumeric characters
        and underscores, matching the regex pattern ``\\b\\w+\\b``.

    Raises
    ------
    ValueError
        If the input is too large or if a regex error occurs during processing.
    """
    # Basic input validation
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    # Guard against excessive resource consumption
    if len(raw_input) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input too large: {len(raw_input)} characters (max {_MAX_INPUT_LENGTH})"
        )

    try:
        # Extract words using a safe, precompiled pattern
        word_pattern = re.compile(r"\b\w+\b")
        words = word_pattern.findall(raw_input)
    except re.error as exc:
        # Wrap regex errors in ValueError to provide a consistent API
        raise ValueError(f"Regex error while processing input: {exc}") from exc

    return words