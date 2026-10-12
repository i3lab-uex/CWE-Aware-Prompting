import re

# Maximum allowed number of words to prevent uncontrolled memory usage (CWE‑400)
MAX_WORDS = 10_000

def analyze_user_string(input_text: str) -> list[str]:
    """
    Split the input string into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The string provided by the user.

    Returns
    -------
    list[str]
        A list of words extracted from `input_text`.

    Raises
    ------
    ValueError
        If the input is not a string, if it contains an excessive amount of words,
        or if any unexpected processing error occurs.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("Input must be a string")

    try:
        # Find all word tokens (alphanumeric and underscore)
        words = re.findall(r"\b\w+\b", input_text)

        # Prevent uncontrolled resource consumption
        if len(words) > MAX_WORDS:
            raise ValueError(
                f"Input contains too many words ({len(words)}); "
                f"maximum allowed is {MAX_WORDS}"
            )

        return words
    except Exception as exc:
        # Wrap any unexpected exception into ValueError for consistency
        raise ValueError(f"Failed to analyze input string: {exc}") from exc