import re

# Regular expression pattern to split on any non‑word character.
_SPLIT_PATTERN = re.compile(r'\W+', flags=re.UNICODE)

# Maximum number of words allowed to be returned.
_MAX_WORDS = 10_000


def process_user_input(user_input: str) -> list[str]:
    """
    Split the given user input into individual words.

    The function uses a regular expression to split on any non‑word
    characters (i.e. anything that is not a letter, digit or underscore).
    Leading and trailing separators are ignored.

    Parameters
    ----------
    user_input : str
        The string to process. It must be a Unicode string.

    Returns
    -------
    list[str]
        A list of words extracted from the input. The order of words
        is preserved.

    Raises
    ------
    ValueError
        If the input cannot be processed (e.g. non‑string, or if the
        resulting word count exceeds :data:`_MAX_WORDS`).

    Notes
    -----
    * The function guards against excessive memory consumption by
      limiting the number of words that can be returned. This mitigates
      CWE‑770 (allocation of resources without limits or throttling).
    * The regular expression is precompiled to avoid repeated
      compilation overhead.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    # Perform the split; filter out empty strings caused by leading/trailing separators.
    words = [w for w in _SPLIT_PATTERN.split(user_input) if w]

    # Enforce the maximum word count.
    if len(words) > _MAX_WORDS:
        raise ValueError(f"Input contains too many words ({len(words)} > {_MAX_WORDS})")

    return words