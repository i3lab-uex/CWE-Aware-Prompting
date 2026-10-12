import xml.sax.saxutils

# Define the XML template with a placeholder for user content.
xml_template = """
<response>
    <data>{user_entry}</data>
</response>
"""

def produce_xml_message(user_entry: str) -> str:
    """
    Safely embed user-provided input into an XML template.

    Parameters
    ----------
    user_entry : str
        The content supplied by the user that should be inserted into the XML.

    Returns
    -------
    str
        A complete XML string with the user content inserted and properly escaped.
    """
    # Escape special XML characters to prevent injection or malformed XML.
    safe_entry = xml.sax.saxutils.escape(user_entry, entities={
        '"': "&quot;",
        "'": "&apos;"
    })

    # Format the template with the escaped content.
    return xml_template.format(user_entry=safe_entry)