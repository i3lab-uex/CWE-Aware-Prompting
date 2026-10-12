import html

# Example template for the user profile display.
# It should contain placeholders for name, biography and status.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{full_name}</h2>
    <section class="about-me">{about_me}</section>
    <footer class="status-update">Status: {status_update}</footer>
</div>
"""

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a sanitized user profile string for safe web display.

    Parameters
    ----------
    full_name : str
        The user's self-provided name.
    about_me : str
        A user-authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The formatted and HTML‑escaped profile string ready for rendering.

    Raises
    ------
    ValueError
        If any argument is not a string or is empty after stripping.
    """
    # Basic type and emptiness checks
    for name, value in (
        ("full_name", full_name),
        ("about_me", about_me),
        ("status_update", status_update),
    ):
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string.")
        if not value.strip():
            raise ValueError(f"{name} cannot be empty or whitespace only.")

    # Escape user input to neutralize XSS and other injection vectors.
    safe_name = html.escape(full_name.strip(), quote=True)
    safe_about_me = html.escape(about_me.strip(), quote=False)
    # For status, allow simple formatting like line breaks but still escape.
    safe_status_update = html.escape(status_update.strip(), quote=False)

    # Format the profile using the template.
    formatted_profile = PROFILE_FORMAT.format(
        full_name=safe_name,
        about_me=safe_about_me.replace("\n", "<br>"),
        status_update=safe_status_update
    )

    return formatted_profile.strip()