import xml.sax.saxutils

# Example XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{content_to_add}</message>
</response>"""

def build_xml_response(content_to_add: str) -> str:
    """
    Construct an XML response by inserting user-provided content into a predefined template.
    
    The function escapes special XML characters in the user-supplied text to prevent
    injection attacks (CWE-74). It does not perform any additional validation or
    sanitization beyond escaping, so callers should ensure that the content is
    appropriate for their context.
    
    Parameters:
        content_to_add (str): The text supplied by the user to be inserted into the XML structure.
    
    Returns:
        str: The constructed XML response with escaped user content.
    """
    # Escape special XML characters in the input to avoid injection.
    safe_content = xml.sax.saxutils.escape(content_to_add, entities={"'": "&apos;", '"': "&quot;"})
    return xml_template.format(content_to_add=safe_content)