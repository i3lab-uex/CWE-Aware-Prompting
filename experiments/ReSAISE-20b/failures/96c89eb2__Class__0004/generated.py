import re

# Maximum number of characters to process (preventing excessive memory usage)
_MAX_INPUT_LENGTH = 1_000_000

def split_text_into_words(input_text: str) -> list[str]:
    """
    Tokenize the provided text into individual words using a regular expression.

    Parameters
    ----------
    input_text : str
        The raw text to be tokenized. Must not exceed ``_MAX_INPUT_LENGTH`` characters.

    Returns
    -------
    list[str]
        A list containing all word tokens extracted from ``input_text``.

    Raises
    ------
    ValueError
        If the input is not a string, or if its length exceeds ``_MAX_INPUT_LENGTH``.
    """
    # Validate input type
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    # Prevent uncontrolled resource consumption
    if len(input_text) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input text too large ({len(input_text)} characters). "
            f"Maximum allowed is {_MAX_INPUT_LENGTH}."
        )

    # Use a Unicode-aware regex to capture words (letters, digits, underscore)
    # This will ignore punctuation and whitespace.
    word_pattern = re.compile(r"\b\w+\b", flags=re.UNICODE)

    try:
        words = word_pattern.findall(input_text)
    except re.error as exc:
        # Re-raise with a clearer message
        raise ValueError(f"Regular expression error: {exc}") from exc

    return words