import xml.sax.saxutils

def create_xml_output(input_content: str) -> str:
    """
    Construct an XML string by safely inserting user-supplied content
    into a predefined template.

    Args:
        input_content (str): Text supplied by the user to be inserted
                             into the XML structure.

    Returns:
        str: The fully formed XML string with the user content escaped.
    """
    # Define the template with a placeholder for the input
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '    <content>{input_content}</content>\n'
        '</response>'
    )

    # Escape special XML characters in the user input
    safe_content = xml.sax.saxutils.escape(input_content, entities={"'": "&apos;", "\"": "&quot;"})

    # Format the template with the escaped content
    return xml_template.format(input_content=safe_content)