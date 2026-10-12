import xml.sax.saxutils

def create_xml_output(user_input: str, xml_template: str) -> str:
    """
    Embed the user-provided input into an XML template safely.

    Parameters
    ----------
    user_input : str
        The string supplied by the user that will be inserted into the XML.
    xml_template : str
        An XML string containing a single placeholder `{user_input}` where the
        escaped user data should be inserted.

    Returns
    -------
    str
        A fully-formed XML string with the user input safely escaped.

    Notes
    -----
    The function uses ``xml.sax.saxutils.escape`` to neutralize the characters
    that have special meaning in XML (&, <, >, ", '), preventing injection
    attacks (CWE-74).  No other validation is performed; the caller should
    ensure that ``xml_template`` contains exactly one `{user_input}` placeholder.
    """
    # Escape special XML characters in the user input
    safe_input = xml.sax.saxutils.escape(user_input, {"'": "&apos;", '"': "&quot;"})

    # Insert the escaped input into the template
    try:
        return xml_template.format(user_input=safe_input)
    except KeyError as exc:
        raise ValueError("The XML template does not contain a `{user_input}` placeholder.") from exc