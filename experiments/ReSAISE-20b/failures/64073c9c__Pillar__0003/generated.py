import xml.sax.saxutils

def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML response by inserting user-supplied content into a template.

    Parameters
    ----------
    content_insert : str
        Text supplied by the user to be embedded in the XML.

    Returns
    -------
    str
        The resulting XML string with the content safely escaped.
    """
    # Predefined template with a placeholder for user content
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<message>\n'
        '    <content>{content_insert}</content>\n'
        '</message>'
    )

    # Escape the user content to prevent XML injection and ensure well‑formedness
    safe_content = xml.sax.saxutils.escape(content_insert, entities={'"': "&quot;", "'": "&apos;"})

    # Format the template with the escaped content
    return xml_template.format(content_insert=safe_content)