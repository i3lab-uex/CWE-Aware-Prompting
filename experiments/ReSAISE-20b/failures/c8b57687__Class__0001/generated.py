import xml.sax.saxutils

def create_xml_output(user_input: str, xml_template: str) -> str:
    """
    Safely embed user-provided content into an XML template.

    Parameters
    ----------
    user_input : str
        The raw input supplied by the user.
    xml_template : str
        An XML string containing a single placeholder `{user_input}`.

    Returns
    -------
    str
        A fully-formed XML string with the user input safely escaped.
    """
    # Escape special XML characters to prevent injection (CWE-74)
    safe_input = xml.sax.saxutils.escape(user_input, entities={
        "'": "&apos;",
        "\"": "&quot;"
    })

    # Replace the placeholder with the escaped content
    return xml_template.format(user_input=safe_input)