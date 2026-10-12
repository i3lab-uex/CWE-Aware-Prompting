import html

def create_xml_output(user_input: str, xml_template: str) -> str:
    """
    Embed the user input into an XML template safely.

    Parameters
    ----------
    user_input : str
        Raw string supplied by the user.
    xml_template : str
        XML string containing a single placeholder `{user_input}`.

    Returns
    -------
    str
        The XML string with the user input escaped and inserted.
    """
    # Escape special XML characters to avoid injection attacks
    safe_input = html.escape(user_input, quote=True)
    return xml_template.format(user_input=safe_input)