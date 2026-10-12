import xml.sax.saxutils

def build_xml_response(content_to_add: str) -> str:
    """
    Construct an XML response by inserting the user-supplied content
    into a predefined template, while properly escaping special XML
    characters to prevent injection attacks (CWE-74).

    Parameters:
        content_to_add (str): Text supplied by the user to be inserted
                              into the XML structure.

    Returns:
        str: The constructed XML response with safe user content.
    """
    # Predefined XML template with a placeholder
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '    <content>{content_to_add}</content>\n'
        '</response>'
    )

    # Escape special XML characters in the user input
    safe_content = xml.sax.saxutils.escape(content_to_add, {"'": "&apos;", "\"": "&quot;"})

    # Insert the escaped content into the template
    return xml_template.format(content_to_add=safe_content)