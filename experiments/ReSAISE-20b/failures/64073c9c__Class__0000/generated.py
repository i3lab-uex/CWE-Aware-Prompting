import xml.sax.saxutils

# Pre‑defined XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<message>
    <body>{content_insert}</body>
</message>"""

def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML message by safely inserting user content into the
    predefined template.

    Parameters
    ----------
    content_insert : str
        Text supplied by the user to be embedded within the <body> element.

    Returns
    -------
    str
        A complete XML document with the user content properly escaped.
    """
    # Escape characters that have special meaning in XML to avoid injection
    safe_content = xml.sax.saxutils.escape(content_insert, {"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(content_insert=safe_content)