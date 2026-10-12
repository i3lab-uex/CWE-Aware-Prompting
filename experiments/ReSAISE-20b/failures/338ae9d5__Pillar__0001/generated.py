import xml.sax.saxutils as saxutils

# Predefined XML template containing a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{input_content}</content>
</response>"""

def create_xml_output(input_content: str) -> str:
    """
    Construct an XML response by inserting the supplied user content into a
    predefined template, ensuring that the content is properly escaped to
    avoid XML injection or malformed documents.

    Parameters:
        input_content (str): The text supplied by the user to be inserted into
                             the XML structure.

    Returns:
        str: The constructed XML response with the user content safely escaped.
    """
    # Escape special XML characters to prevent injection or malformed XML.
    safe_content = saxutils.escape(input_content, entities={"'": "&apos;", "\"": "&quot;"})
    # Insert the escaped content into the template.
    return xml_template.format(input_content=safe_content)