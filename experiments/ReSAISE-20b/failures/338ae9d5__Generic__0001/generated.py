import xml.sax.saxutils

# Define the XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{input_content}</content>
</response>"""

def create_xml_output(input_content: str) -> str:
    """
    Create an XML response by inserting the user-supplied content into a pre-defined
    template. The input is XML‑escaped to avoid malformed documents.

    Args:
        input_content (str): Text supplied by the user to be inserted into the XML.

    Returns:
        str: The constructed XML string with the escaped user content.
    """
    # Escape special XML characters to prevent injection and malformed output
    safe_content = xml.sax.saxutils.escape(input_content, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(input_content=safe_content)