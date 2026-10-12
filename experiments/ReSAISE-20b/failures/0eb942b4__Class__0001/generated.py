import re

def analyze_user_string(input_text: str) -> list:
    """
    Splits a user-provided string into words and returns them as a list.

    Parameters
    ----------
    input_text : str
        The string to be analyzed.

    Returns
    -------
    list[str]
        A list of words extracted from `input_text`.

    Raises
    ------
    ValueError
        If the input is not a string, if it is empty after stripping,
        or if the number of words exceeds a safe threshold.
    """
    # Basic type and content validation
    if not isinstance(input_text, str):
        raise ValueError("input_text must be a string")

    stripped = input_text.strip()
    if not stripped:
        raise ValueError("input_text must contain non‑whitespace characters")

    # Extract words using a simple word boundary regex
    # This avoids memory blow‑up by not constructing large intermediate objects
    words = re.findall(r'\b\w+\b', stripped)

    # Safeguard against uncontrolled resource consumption
    MAX_WORDS = 10_000_000  # arbitrary but reasonable limit
    if len(words) > MAX_WORDS:
        raise ValueError(f"Too many words ({len(words)}). Refuse to process.")

    return words