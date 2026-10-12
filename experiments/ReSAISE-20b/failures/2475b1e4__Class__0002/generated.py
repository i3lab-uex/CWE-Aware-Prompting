import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_template = """
<response>
    <status>success</status>
    <data>{content_to_add}</data>
</response>
"""

def build_xml_response(content_to_add: str) -> str:
    """
    Construct an XML response by safely inserting user-provided content into a
    predefined template.

    Args:
        content_to_add: The raw text supplied by the user that will be inserted
                         into the <data> element of the XML.

    Returns:
        A string containing a well‑formed XML document with the user content
        properly escaped to prevent injection attacks (CWE‑74).

    Note:
        The function does not raise exceptions intentionally. If `content_to_add`
        contains characters that cannot be represented in UTF‑8, a UnicodeEncodeError
        may occur when the XML is serialized or transmitted downstream.
    """
    # Escape characters that are special in XML to prevent injection.
    safe_content = xml.sax.saxutils.escape(content_to_add, entities={
        '"': "&quot;",
        "'": "&apos;"
    })

    # Format the template with the escaped content.
    return xml_template.format(content_to_add=safe_content)