import xml.sax.saxutils

def build_xml_response(content_to_add: str) -> str:
    """
    Construct an XML response by inserting the supplied content into a
    predefined template. The user-supplied content is properly escaped to
    avoid XML injection or malformed documents.

    Parameters:
        content_to_add (str): The text supplied by the user that will be
                              inserted into the XML structure.

    Returns:
        str: The fully constructed XML response with escaped user content.
    """
    # Predefined template containing a placeholder for the user content
    xml_template = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<response>\n"
        "    <message>{content_to_add}</message>\n"
        "</response>"
    )

    # Escape special XML characters in the user-provided content
    escaped_content = xml.sax.saxutils.escape(content_to_add, {"'": "&apos;", "\"": "&quot;"})

    # Format the template with the escaped content
    return xml_template.format(content_to_add=escaped_content)