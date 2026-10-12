import xml.sax.saxutils

# Template for the XML response.  The placeholder {user_content} will be
# replaced by the escaped user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_content}</content>
</response>"""


def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by embedding the supplied user content into
    a predefined template.

    The function escapes characters that have special meaning in XML
    (e.g., <, >, &, ", ') to prevent injection attacks (CWE-74).

    Args:
        user_content: The content supplied by the user.

    Returns:
        A string containing the XML response with the escaped user content.
    """
    # Escape special XML characters in the user content
    safe_content = xml.sax.saxutils.escape(user_content, {"'": "&apos;", '"': "&quot;"})

    # Construct the final XML response
    return xml_template.format(user_content=safe_content)