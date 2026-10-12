import xml.sax.saxutils as saxutils

# Predefined XML template with a placeholder for user content
xml_template = """
<message>
    <header>Welcome</header>
    <body>{content_insert}</body>
</message>
"""

def generate_xml_message(content_insert: str) -> str:
    """
    Safely embed user-supplied content into a predefined XML template.

    Parameters
    ----------
    content_insert : str
        The text supplied by the user to be inserted into the XML structure.

    Returns
    -------
    str
        The constructed XML response with the user content properly escaped.
    """
    # Escape special XML characters to avoid breaking structure or introducing
    # malicious payloads (CWE-707).
    safe_content = saxutils.escape(content_insert, entities={"'": "&apos;", '"': "&quot;"})
    return xml_template.format(content_insert=safe_content)