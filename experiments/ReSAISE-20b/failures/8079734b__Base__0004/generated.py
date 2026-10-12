import re

# Define a reasonable maximum number of words to prevent resource exhaustion (CWE‑770).
_MAX_WORDS = 10_000


def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extract individual words from a raw user input string.

    Parameters
    ----------
    raw_input : str
        The raw text provided by the user.

    Returns
    -------
    list[str]
        A list of words found in ``raw_input``.

    Raises
    ------
    ValueError
        If the input is not a string, if it contains an excessive number of words,
        or if any other processing error occurs.
    """
    # Basic type check
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a Unicode-aware word pattern: \w includes letters, digits and underscore.
        # We also allow apostrophes inside words (e.g., "don't").
        word_pattern = re.compile(r"\b[\w']+\b", flags=re.UNICODE)

        words = word_pattern.findall(raw_input)

        # Enforce a maximum number of words to avoid memory exhaustion.
        if len(words) > _MAX_WORDS:
            raise ValueError(
                f"Input contains {len(words)} words, exceeding the maximum of {_MAX_WORDS}"
            )

        return words

    except re.error as exc:
        # Catch regex compilation or execution errors and wrap them in ValueError.
        raise ValueError(f"Regex error during word extraction: {exc}") from exc
    except Exception as exc:
        # Any other unexpected error is also wrapped.
        raise ValueError(f"Unexpected error during word extraction: {exc}") from exc