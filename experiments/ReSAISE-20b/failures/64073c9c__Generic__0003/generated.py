# -*- coding: utf-8 -*-
"""
Utility to generate an XML message by inserting user supplied content
into a predefined template. The function escapes the inserted text
to avoid breaking the XML structure.
"""

from xml.sax.saxutils import escape

# Example template containing a placeholder for the user content.
# In real usage, replace this with the actual XML structure you need.
XML_TEMPLATE = """
<message>
    <header>
        <title>Response</title>
    </header>
    <body>
        {content_insert}
    </body>
</message>
"""


def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML message by inserting the supplied content into a
    predefined template. The inserted text is escaped to ensure it does
    not corrupt the XML.

    Args:
        content_insert (str): Text supplied by the user to be inserted
                              into the XML structure.

    Returns:
        str: The complete XML message with the user content embedded.
    """
    # Escape special XML characters in the user-supplied content
    safe_content = escape(content_insert, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped content
    return XML_TEMPLATE.format(content_insert=safe_content)