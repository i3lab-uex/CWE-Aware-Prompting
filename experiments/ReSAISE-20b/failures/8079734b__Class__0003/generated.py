import re

# Maximum number of words allowed to prevent uncontrolled resource consumption (CWE-400)
_MAX_WORDS = 10_000

def extract_words_from_input(raw_input: str) -> list[str]:
    """
    Extracts words from a raw input string using regular expressions.

    Parameters
    ----------
    raw_input : str
        The user-provided text input.

    Returns
    -------
    list[str]
        A list of words extracted from the input string.

    Raises
    ------
    ValueError
        If the input is not a string, if it contains an excessive number of words,
        or if any unexpected error occurs during processing.
    """
    # Validate input type
    if not isinstance(raw_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use a simple word pattern that matches alphanumeric sequences.
        words = re.findall(r"\b\w+\b", raw_input)

        # Enforce a hard limit on the number of words to avoid resource exhaustion.
        if len(words) > _MAX_WORDS:
            raise ValueError(
                f"Input contains too many words ({len(words)}). "
                f"Maximum allowed is {_MAX_WORDS}."
            )

        return words
    except re.error as exc:
        # Re-raise regex errors as ValueError for consistency.
        raise ValueError(f"Regex error during word extraction: {exc}") from exc
    except Exception as exc:
        # Catch any other unexpected errors.
        raise ValueError(f"Unexpected error during word extraction: {exc}") from exc