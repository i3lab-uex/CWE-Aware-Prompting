import xml.sax.saxutils as sax

def create_xml_output(user_input: str, xml_template: str) -> str:
    """
    Embed user-provided input into an XML template safely.

    Parameters
    ----------
    user_input : str
        The content supplied by the user.
    xml_template : str
        An XML string containing a single placeholder `{user_input}`.

    Returns
    -------
    str
        The XML string with the user content inserted, with all special
        characters escaped to prevent injection or malformed XML.
    """
    # Escape user input for XML
    safe_input = sax.escape(user_input, {"'": "&apos;", '"': "&quot;"})
    return xml_template.format(user_input=safe_input)