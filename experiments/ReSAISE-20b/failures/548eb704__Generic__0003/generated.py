import re

def parse_text_input(provided_input):
    """
    Extract words from a raw text input.

    Parameters
    ----------
    provided_input : str
        The user-provided string from which words will be extracted.

    Returns
    -------
    list[str]
        A list containing all the words found in `provided_input`.

    Raises
    ------
    ValueError
        If `provided_input` is not a string or if any error occurs during processing.
    """
    # Validate input type
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string")

    try:
        # Use Unicode-aware word boundaries; \w includes letters, digits and underscore.
        words = re.findall(r'\b\w+\b', provided_input)
    except Exception as exc:
        # Wrap any unexpected regex error into a ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words