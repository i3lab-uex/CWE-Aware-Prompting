import xml.sax.saxutils as saxutils

def create_xml_output(user_input: str) -> str:
    """
    Embed user input safely into an XML template.

    Parameters
    ----------
    user_input : str
        Raw string provided by the user that will be inserted into the XML.

    Returns
    -------
    str
        A complete XML document with the user input properly escaped.
    """
    # Define the template with a placeholder
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<root>\n'
        '  <message>{user_input}</message>\n'
        '</root>'
    )

    # Escape special XML characters to prevent injection (CWE‑74)
    safe_input = saxutils.escape(user_input, {"'": "&apos;", '"': '&quot;'})

    # Format the template with the escaped input
    return xml_template.format(user_input=safe_input)