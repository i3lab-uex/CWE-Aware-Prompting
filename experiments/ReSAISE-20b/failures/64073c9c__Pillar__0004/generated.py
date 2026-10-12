import html

def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML message by inserting user supplied content into a predefined template.
    
    Parameters
    ----------
    content_insert : str
        Text supplied by the user to be inserted into the XML structure.
    
    Returns
    -------
    str
        The constructed XML response with the user content safely escaped.
    
    Notes
    -----
    * The function uses `html.escape` (which is suitable for XML escaping) to neutralize
      characters that could break well‑formedness or enable injection attacks.
    * The template contains a `{content_insert}` placeholder that is replaced with the
      escaped content.
    """
    xml_template = (
        "<message>\n"
        "  <header>\n"
        "    <title>Response</title>\n"
        "  </header>\n"
        "  <body>\n"
        "    {content_insert}\n"
        "  </body>\n"
        "</message>"
    )
    
    # Escape special XML characters in the user content
    safe_content = html.escape(content_insert, quote=True)
    
    # Format the template with the escaped content
    return xml_template.format(content_insert=safe_content)