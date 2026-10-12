import xml.sax.saxutils

# Example XML template with a placeholder for user content.
xml_template = """
<response>
    <content>{input_content}</content>
</response>
"""

def create_xml_output(input_content: str) -> str:
    """
    Create an XML response by inserting the supplied user content into
    a predefined template. The content is escaped to avoid breaking XML.

    Args:
        input_content: Text supplied by the user that will be inserted
                       into the XML structure.

    Returns:
        A string containing the complete XML with the user content safely
        embedded.
    """
    # Escape special XML characters to maintain well‑formedness
    safe_content = xml.sax.saxutils.escape(input_content, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(input_content=safe_content)