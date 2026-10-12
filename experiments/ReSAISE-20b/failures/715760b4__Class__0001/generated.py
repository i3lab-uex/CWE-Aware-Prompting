import xml.sax.saxutils

# XML template with a placeholder for user-provided content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_entry}</message>
</response>"""

def produce_xml_message(user_entry: str) -> str:
    """
    Embed the user-provided entry into an XML template safely.

    Parameters
    ----------
    user_entry : str
        Raw input supplied by the user. It will be escaped to prevent XML injection.

    Returns
    -------
    str
        A complete XML document containing the escaped user content.
    """
    # Escape special XML characters to avoid injection (CWE-74)
    safe_entry = xml.sax.saxutils.escape(user_entry, entities={"'": "&apos;", '"': "&quot;"})
    return xml_template.format(user_entry=safe_entry)