import re

def parse_text_input(provided_input):
    """
    Parse a raw text input string and extract individual words.

    Parameters
    ----------
    provided_input : str
        The raw text input from the user.

    Returns
    -------
    list of str
        A list containing the extracted words in order of appearance.

    Raises
    ------
    ValueError
        If the input is not a string or if an error occurs during parsing.
    """
    # Validate input type
    if not isinstance(provided_input, str):
        raise ValueError("Input must be a string.")

    try:
        # Use a regular expression to match word characters.
        # \b ensures we capture whole words; \w+ matches alphanumeric and underscore.
        words = re.findall(r'\b\w+\b', provided_input)
    except Exception as exc:
        # Any unexpected exception during regex processing is wrapped in ValueError
        raise ValueError(f"Failed to parse input: {exc}") from exc

    return words