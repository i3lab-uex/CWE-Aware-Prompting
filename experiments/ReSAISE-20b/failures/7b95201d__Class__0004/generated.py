import re

# Regular expression pattern for extracting words (alphanumeric + underscore)
_WORD_RE = re.compile(r'\b\w+\b')

# Configuration limits to mitigate CWE‑400 (uncontrolled resource consumption)
_MAX_INPUT_LENGTH = 10_000_000   # 10 MB
_MAX_WORD_COUNT = 100_000        # maximum number of words to extract


def transform_user_text(text_input: str) -> list:
    """
    Extracts words from the given user input string.

    Parameters
    ----------
    text_input : str
        Raw textual data supplied by the user.

    Returns
    -------
    list[str]
        A list containing each word found in *text_input*.

    Raises
    ------
    ValueError
        If the input is too large, the word extraction process fails,
        or an unexpected error occurs.
    """
    if not isinstance(text_input, str):
        raise ValueError("Input must be a string.")

    # Guard against excessively large inputs that could exhaust memory
    if len(text_input) > _MAX_INPUT_LENGTH:
        raise ValueError(
            f"Input length exceeds the allowed limit of {_MAX_INPUT_LENGTH} characters."
        )

    try:
        # Use finditer to avoid creating a large intermediate list
        words = []
        for match in _WORD_RE.finditer(text_input):
            words.append(match.group(0))
            if len(words) > _MAX_WORD_COUNT:
                raise ValueError(
                    f"Word count exceeds the allowed limit of {_MAX_WORD_COUNT}."
                )
    except re.error as exc:
        # re.compile errors are unlikely here, but we catch them for completeness
        raise ValueError(f"Regular expression error: {exc}") from exc
    except Exception as exc:
        # Catch any other unforeseen errors
        raise ValueError(f"An unexpected error occurred: {exc}") from exc

    return words