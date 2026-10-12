import xml.sax.saxutils

def build_xml_response(content_to_add: str) -> str:
    """
    Insert user supplied content into a predefined XML template.

    Parameters
    ----------
    content_to_add : str
        Text supplied by the user that will be inserted into the XML.

    Returns
    -------
    str
        The constructed XML string with the content safely escaped.
    """
    # Predefined template with a placeholder
    xml_template = (
        "<response>\n"
        "  <status>ok</status>\n"
        "  <data>{content_to_add}</data>\n"
        "</response>"
    )

    # Escape XML special characters to avoid injection or malformed XML
    escaped_content = xml.sax.saxutils.escape(content_to_add)

    # Format the template with the escaped content
    return xml_template.format(content_to_add=escaped_content)