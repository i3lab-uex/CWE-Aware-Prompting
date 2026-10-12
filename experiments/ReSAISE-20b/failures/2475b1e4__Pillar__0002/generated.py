import xml.sax.saxutils as saxutils

# Pre‑defined XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{content_to_add}</content>
</response>"""

def build_xml_response(content_to_add: str) -> str:
    """
    Construct an XML response by inserting user-supplied content into a template.

    Parameters
    ----------
    content_to_add : str
        Text supplied by the user to be inserted into the XML structure.

    Returns
    -------
    str
        The constructed XML response that integrates the input from the user into the
        appropriate section of the template. The content is properly escaped to avoid
        XML injection and ensure well‑formedness.
    """
    # Escape special XML characters to prevent injection or malformed XML
    escaped_content = saxutils.escape(content_to_add, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(content_to_add=escaped_content)