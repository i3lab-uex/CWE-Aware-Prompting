import re

# Maximum number of words to allow in the output list.
# This helps guard against excessive memory usage (CWE‑770).
MAX_WORDS = 10_000

def parse_text_input(provided_input: str) -> list[str]:
    """
    Extract words from the provided input string and return them as a list.

    Parameters
    ----------
    provided_input : str
        Raw text input from the user.

    Returns
    -------
    list[str]
        List of words found in `provided_input`.

    Raises
    ------
    ValueError
        If the input is not a string, if it is empty or only whitespace,
        or if extracting words would produce more than MAX_WORDS entries.
    """
    # Basic type and content checks
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string.")
    if not provided_input.strip():
        raise ValueError("Input cannot be empty or only whitespace.")

    # Use a simple regex to find word boundaries.
    words = re.findall(r"\b\w+\b", provided_input)

    # Enforce a limit on the number of words to avoid excessive allocation.
    if len(words) > MAX_WORDS:
        raise ValueError(
            f"Input contains {len(words)} words, which exceeds "
            f"the allowed maximum of {MAX_WORDS}."
        )

    return words