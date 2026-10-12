import re

def handle_user_data(input_string: str) -> list:
    """
    Split the user-provided string into individual words using a regular expression.

    Parameters
    ----------
    input_string : str
        The string provided by the user.

    Returns
    -------
    list
        A list of words extracted from ``input_string``.

    Raises
    ------
    ValueError
        If the input is not a string or if any error occurs during processing.
    """
    # Validate that the input is indeed a string
    if not isinstance(input_string, str):
        raise ValueError("input_string must be a string")

    try:
        # Use a compiled pattern that matches word characters.
        # The pattern is static and not influenced by user input,
        # mitigating potential injection or denial‑of‑service risks.
        word_pattern = re.compile(r"\b\w+\b", flags=re.UNICODE)
        words = word_pattern.findall(input_string)
    except re.error as exc:
        # Any regex compilation or execution error is converted to ValueError
        raise ValueError(f"Regular expression processing failed: {exc}") from exc
    except Exception as exc:
        # Catch-all for unforeseen runtime errors
        raise ValueError(f"Unexpected error during processing: {exc}") from exc

    return words