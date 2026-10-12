import xml.sax.saxutils as saxutils

# Example XML template with a placeholder for user content.
xml_template = """
<response>
    <status>success</status>
    <data>{content_to_add}</data>
</response>
"""

def build_xml_response(content_to_add: str) -> str:
    """
    Builds an XML response by inserting the provided user content into a predefined template.
    
    Parameters
    ----------
    content_to_add : str
        The user-supplied text to be embedded in the XML structure.

    Returns
    -------
    str
        A well-formed XML string with the escaped user content safely inserted.
    
    Notes
    -----
    The function uses ``xml.sax.saxutils.escape`` to neutralize characters that could
    break XML structure or enable injection attacks. This mitigates CWE-707 risks by
    ensuring the resulting document remains well‑formed and safe for downstream consumers.
    """
    # Escape special XML characters in the user content
    escaped_content = saxutils.escape(content_to_add, {"'": "&apos;", "\"": "&quot;"})
    # Insert the escaped content into the template
    return xml_template.format(content_to_add=escaped_content)