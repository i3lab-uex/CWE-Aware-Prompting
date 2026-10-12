import xml.sax.saxutils

# XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_content}</content>
</response>"""

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by safely embedding user-provided content into a template.

    Parameters
    ----------
    user_content : str
        The raw text supplied by the user that will be inserted into the XML.

    Returns
    -------
    str
        The fully-formed XML string with the user content safely escaped.

    Notes
    -----
    - The function uses :func:`xml.sax.saxutils.escape` to neutralize
      characters that could break the XML structure (e.g., &, <, >,
      ", and ').
    - No other external libraries are required.
    """
    # Escape XML special characters to prevent injection or malformed XML
    safe_content = xml.sax.saxutils.escape(user_content, {"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_content=safe_content)