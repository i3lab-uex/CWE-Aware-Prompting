import xml.sax.saxutils

def create_xml_output(input_content: str) -> str:
    """
    Construct an XML response by inserting user-supplied content into a
    predefined template. The function safely escapes special XML characters
    to mitigate injection risks (CWE-74).

    Parameters:
        input_content (str): Text supplied by the user to be inserted into
                             the XML structure.

    Returns:
        str: The constructed XML response with user content safely escaped.
    """
    # Predefined template containing a placeholder for the input content
    xml_template = (
        "<response>\n"
        "  <message>{input_content}</message>\n"
        "</response>"
    )

    # Escape special XML characters in the user input
    safe_content = xml.sax.saxutils.escape(input_content)

    # Insert the escaped content into the template
    return xml_template.format(input_content=safe_content)