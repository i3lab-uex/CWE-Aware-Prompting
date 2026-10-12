import re

def analyze_user_string(input_text):
    """
    Splits the provided input string into individual words using regular expressions.

    Parameters
    ----------
    input_text : str
        The string supplied by the user to be tokenised.

    Returns
    -------
    list[str]
        A list containing all words extracted from ``input_text``.

    Raises
    ------
    ValueError
        If ``input_text`` is not a string or if an error occurs during processing.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    try:
        # Use a Unicode-aware pattern to capture words
        words = re.findall(r"\b\w+\b", input_text, flags=re.UNICODE)
        return words
    except re.error as exc:
        # Re-raise as ValueError to match the specified API
        raise ValueError(f"Regular expression error: {exc}") from exc