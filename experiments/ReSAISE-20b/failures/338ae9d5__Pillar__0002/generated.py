import xml.sax.saxutils

def create_xml_output(input_content: str) -> str:
    """
    Construct an XML response by safely inserting user-supplied content into a predefined template.

    Parameters
    ----------
    input_content : str
        Text supplied by the user to be embedded in the XML structure.

    Returns
    -------
    str
        The complete XML string with the user content properly escaped.
    """
    # Predefined template containing a placeholder for the input content
    xml_template = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<response>\n"
        "  <content>{input_content}</content>\n"
        "</response>"
    )

    # Escape special XML characters to avoid injection or malformed XML
    safe_content = xml.sax.saxutils.escape(input_content, entities={"'": "&apos;", "\"": "&quot;"})

    # Format the template with the escaped content
    return xml_template.format(input_content=safe_content)