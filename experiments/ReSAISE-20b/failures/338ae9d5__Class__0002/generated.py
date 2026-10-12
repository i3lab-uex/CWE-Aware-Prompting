import xml.sax.saxutils

def create_xml_output(input_content: str) -> str:
    """
    Create an XML response by inserting user-supplied content into a predefined
    XML template. The function escapes special XML characters in the input to
    prevent injection attacks (CWE-74).

    Args:
        input_content: The raw text supplied by the user.

    Returns:
        A string containing the complete XML document with the escaped content
        safely embedded.
    """
    # Predefined template containing a placeholder for the user content.
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '    <message>{input_content}</message>\n'
        '</response>'
    )

    # Escape special XML characters in the user input.
    safe_content = xml.sax.saxutils.escape(input_content, entities={"'": "&apos;", "\"": "&quot;"})

    # Insert the escaped content into the template.
    return xml_template.format(input_content=safe_content)