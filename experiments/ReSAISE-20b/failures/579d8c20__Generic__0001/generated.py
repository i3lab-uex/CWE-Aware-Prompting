import html

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML response by safely inserting user-provided content
    into a predefined template.

    Parameters
    ----------
    visitor_content : str
        Content supplied by the user that should be embedded in the page.

    Returns
    -------
    str
        The complete HTML page with the user content inserted, properly escaped
        to prevent script injection attacks.
    """
    # Define a minimal HTML template with a placeholder for user content
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Welcome Visitor</title>
    </head>
    <body>
        <h1>Hello, visitor!</h1>
        <div id="user-content">{user_content}</div>
    </body>
    </html>
    """

    # Escape the user content to neutralize any embedded scripts or markup
    safe_content = html.escape(visitor_content, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)