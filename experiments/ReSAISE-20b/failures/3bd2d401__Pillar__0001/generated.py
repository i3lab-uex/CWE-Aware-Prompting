import xml.sax.saxutils

# Example XML design template with a placeholder for user input.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{input_data}</message>
</response>"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert user-supplied content into an XML template safely.

    Parameters
    ----------
    input_data : str
        The raw content submitted by the user.  It will be inserted into the
        {input_data} placeholder of ``xml_design`` after being XML‑escaped.

    Returns
    -------
    str
        A well‑formed XML string with the user content safely encoded.

    Notes
    -----
    - The function uses :func:`xml.sax.saxutils.escape` to neutralize any
      characters that could break XML syntax or introduce injection attacks.
    - This mitigates CWE‑707 by ensuring the output remains a valid, safe
      XML document before it is returned or transmitted.
    """
    # Escape user input to avoid breaking the XML structure.
    safe_input = xml.sax.saxutils.escape(input_data, entities={
        '"': "&quot;",
        "'": "&apos;"
    })

    # Replace the placeholder with the escaped content.
    return xml_design.format(input_data=safe_input)