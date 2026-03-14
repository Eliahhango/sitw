#!/usr/bin/env python3
"""
Customize ALL pages of the downloaded profilez.xyz/ronaldcortez site
to match EliTechWiz's credentials from https://www.elitechwiz.site/
Then serve on localhost:8080.
"""

import http.server
import os
import pathlib
import re
import shutil
import socketserver

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE      = pathlib.Path(r"c:\Users\hango\Desktop\Site downloader\downloaded_site\profilez.xyz")
SRC_DIR   = BASE / "ronaldcortez"
DEST_DIR  = BASE / "elitechwiz"
PORT      = 8080

# ── EliTechWiz credentials ─────────────────────────────────────────────────────
NAME          = "EliTechWiz"
EMAIL         = "contact@elitechwiz.com"
PHONE         = "+255 688 164 510"
WHATSAPP      = "255742631101"
GITHUB_URL    = "https://github.com/Eliahhango"
YOUTUBE_URL   = "https://youtube.com/@eliahhango"
PROFILE_PHOTO = "https://files.catbox.moe/qgbtyt.png"

BIO = (
    "I am EliTechWiz, a visionary technologist, hacker, and creative mind, driven by "
    "innovation and the pursuit of digital excellence. My expertise spans cybersecurity, "
    "software development, UI/UX design, graphics and architectural design, and more. "
    "With a passion for turning complex problems into elegant solutions, I merge technology, "
    "design, and strategy to create impactful digital experiences."
)

SOCIAL_LINKS_HTML = f'''<ul class="social-links">
                                                        <li><a href="{GITHUB_URL}" target="_blank"><i class="fab fa-github"></i></a></li>
                                                        <li><a href="{YOUTUBE_URL}" target="_blank"><i class="fab fa-youtube"></i></a></li>
                                                        <li><a href="mailto:{EMAIL}" target="_blank"><i class="fas fa-envelope"></i></a></li>
                                                    </ul>'''


def apply_global_replacements(html: str, filename: str) -> str:
    """Replacements that apply to every HTML file across the site."""

    # ── 1. Page title  ─────────────────────────────────────────────────────────
    html = re.sub(
        r'<title>\s*Ronald\s*-\s*(.*?)\s*</title>',
        lambda m: f'<title>{NAME} - {m.group(1).strip()}</title>',
        html
    )

    # ── 2. Favicon ─────────────────────────────────────────────────────────────
    html = re.sub(
        r'href="https://profilez\.xyz/assets/front/img/user/[^"]+"\s+type="image/png"',
        f'href="{PROFILE_PHOTO}" type="image/png"',
        html
    )

    # ── 3. Primary accent colour ────────────────────────────────────────────────
    html = html.replace("--color-primary: #4402FF", "--color-primary: #0B0840")

    # ── 4. Navbar logo image (lazy-loaded) ─────────────────────────────────────
    html = re.sub(
        r'(<img\s+)class="lazy"\s+data-src="https://profilez\.xyz/assets/front/img/user/[^"]+"\s+alt="logo"',
        rf'\1src="{PROFILE_PHOTO}" alt="logo" '
        r'style="width:45px;height:45px;border-radius:50%;object-fit:cover;"',
        html
    )

    # ── 5. All URLs: ronaldcortez → elitechwiz ──────────────────────────────────
    html = html.replace("profilez.xyz/ronaldcortez", "profilez.xyz/elitechwiz")
    html = html.replace('value="ronaldcortez"', 'value="elitechwiz"')
    html = html.replace('"ronaldcortez"', '"elitechwiz"')
    html = html.replace(">ronaldcortez<", ">elitechwiz<")
    html = html.replace("by\n                                            ronaldcortez",
                        "by\n                                            elitechwiz")
    html = re.sub(r'\bronaldcortez\b', 'elitechwiz', html)  # catch any remaining

    # ── 6. Hero name ────────────────────────────────────────────────────────────
    html = re.sub(r'Ronald\s*\n?\s*Cortez', NAME, html)
    html = html.replace("Ronald Cortez", NAME)

    # ── 7. Animated roles (hero only) ───────────────────────────────────────────
    html = re.sub(
        r'<span class="cd-words-wrapper">.*?</span>\s*</p>',
        f'''<span class="cd-words-wrapper">
                                                        <b class="is-visible">Cybersecurity Expert </b>
                                                        <b class="">Software Developer</b>
                                                        <b class="">UI/UX Designer</b>
                                    </span>
                        </p>''',
        html,
        flags=re.DOTALL
    )

    # ── 8. Hero section background image ────────────────────────────────────────
    html = re.sub(
        r'data-bg="https://profilez\.xyz/assets/front/img/user/home_settings/[^"]+"',
        f'style="background-image:url(\'{PROFILE_PHOTO}\');"',
        html
    )

    # ── 9. About / home_settings images ─────────────────────────────────────────
    html = re.sub(
        r'data-src="https://profilez\.xyz/assets/front/img/user/home_settings/[^"]+"',
        f'src="{PROFILE_PHOTO}"',
        html
    )
    html = re.sub(
        r'class="lazy"\s+src="' + re.escape(PROFILE_PHOTO) + '"',
        f'src="{PROFILE_PHOTO}"',
        html
    )

    # ── 10. About heading & bio ──────────────────────────────────────────────────
    html = html.replace("I HAVE 20 YEARS OF EXPERIENCE", "Visionary Technologist &amp; Creative Mind")
    html = re.sub(r'Lorem ipsum dolor sit amet.*?scelerisque', BIO, html, flags=re.DOTALL)

    # ── 11. Skills ───────────────────────────────────────────────────────────────
    html = re.sub(
        r'data-percent="80"(\s+data-bar-color="#F78058">)\s*<span>80</span>',
        r'data-percent="90"\1\n                                    <span>90</span>',
        html
    )
    html = html.replace('<p class="title">SOCIAL MARKETING</p>', '<p class="title">CYBERSECURITY</p>')
    html = re.sub(
        r'data-percent="60"(\s+data-bar-color="#31F0F7">)\s*<span>60</span>',
        r'data-percent="85"\1\n                                    <span>85</span>',
        html
    )
    html = html.replace('<p class="title">WEB DEVELOPMENT</p>', '<p class="title">SOFTWARE DEVELOPMENT</p>')
    html = re.sub(
        r'data-percent="75"(\s+data-bar-color="#F72EBB">)\s*<span>75</span>',
        r'data-percent="80"\1\n                                    <span>80</span>',
        html
    )

    # ── 12. Service names (nav links + headings + page-level) ────────────────────
    html = re.sub(r'>web development</a>', '>Cybersecurity &amp; Pen Testing</a>', html, flags=re.IGNORECASE)
    html = re.sub(r'>social media marketing</a>', '>Software Development</a>', html, flags=re.IGNORECASE)
    html = re.sub(r'>ui/ux design</a>', '>UI/UX Design</a>', html, flags=re.IGNORECASE)
    html = re.sub(r'>web development<', '>Cybersecurity &amp; Pen Testing<', html, flags=re.IGNORECASE)
    html = re.sub(r'>social media marketing<', '>Software Development<', html, flags=re.IGNORECASE)
    html = re.sub(r'>ui/ux design<', '>UI/UX Design<', html, flags=re.IGNORECASE)
    # Page h1/h2 headings in service detail pages
    html = re.sub(r'<h1>\s*web development\s*</h1>', '<h1>Cybersecurity &amp; Pen Testing</h1>', html, flags=re.IGNORECASE)
    html = re.sub(r'<h1>\s*social media marketing\s*</h1>', '<h1>Software Development</h1>', html, flags=re.IGNORECASE)
    html = re.sub(r'<h1>\s*ui/ux design\s*</h1>', '<h1>UI/UX Design</h1>', html, flags=re.IGNORECASE)
    html = re.sub(r'<h3[^>]*>\s*web development\s*</h3>', '<h3 class="title mt-3">Cybersecurity &amp; Pen Testing</h3>', html, flags=re.IGNORECASE)
    html = re.sub(r'<h3[^>]*>\s*social media marketing\s*</h3>', '<h3 class="title mt-3">Software Development</h3>', html, flags=re.IGNORECASE)
    html = re.sub(r'<h3[^>]*>\s*ui/ux design\s*</h3>', '<h3 class="title mt-3">UI/UX Design</h3>', html, flags=re.IGNORECASE)

    # ── 13. Stats counters ───────────────────────────────────────────────────────
    html = re.sub(
        r'<span class="counter">18</span>(.*?)<h6 class="title">YEARS OF EXPERIENCE</h6>',
        r'<span class="counter">6</span>\1<h6 class="title">YEARS OF EXPERIENCE</h6>',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<span class="counter">985</span>(.*?)<h6 class="title">SATISFIED CUSTOMER</h6>',
        r'<span class="counter">50</span>\1<h6 class="title">HAPPY CLIENTS</h6>',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<span class="counter">235</span>(.*?)<h6 class="title">PROJECTS COMPLETED</h6>',
        r'<span class="counter">30</span>\1<h6 class="title">PROJECTS COMPLETED</h6>',
        html, flags=re.DOTALL
    )
    html = re.sub(
        r'<span class="counter">789</span>(.*?)<h6 class="title">TOTAL COUNTRIES</h6>',
        r'<span class="counter">10</span>\1<h6 class="title">COUNTRIES REACHED</h6>',
        html, flags=re.DOTALL
    )

    # ── 14. Portfolio / project titles ──────────────────────────────────────────
    portfolio_map = {
        r'Web App':           'SecureAuth Platform',
        r'UI UX':             'DataViz Dashboard',
        r'It has survived':   'Architectural Visualization',
        r'simply dummy text': 'Network Intrusion Detection',
        r'unknown printer':   'Portfolio Website',
        r'Why do we use it':  'Security Audit Tool',
    }
    for old, new in portfolio_map.items():
        html = re.sub(old, new, html, flags=re.IGNORECASE)

    # Project filter categories
    html = html.replace('<li data-filter=".cat-75">ui/ux design</li>', '<li data-filter=".cat-75">UI/UX Design</li>')
    html = html.replace('<li data-filter=".cat-76">web development</li>', '<li data-filter=".cat-76">Cybersecurity</li>')
    html = html.replace('<li data-filter=".cat-77">social media marketing</li>', '<li data-filter=".cat-77">Software Dev</li>')

    # Portfolio breadcrumb / page heading
    html = re.sub(r'<title>\s*EliTechWiz\s*-\s*web-app\s*</title>', f'<title>{NAME} - SecureAuth Platform</title>', html, flags=re.IGNORECASE)
    html = re.sub(r'<title>\s*EliTechWiz\s*-\s*ui-ux\s*</title>', f'<title>{NAME} - DataViz Dashboard</title>', html, flags=re.IGNORECASE)
    html = re.sub(r'<title>\s*EliTechWiz\s*-\s*unknown-printer\s*</title>', f'<title>{NAME} - Portfolio Website</title>', html, flags=re.IGNORECASE)
    html = re.sub(r'<title>\s*EliTechWiz\s*-\s*simply-dummy-text\s*</title>', f'<title>{NAME} - Network Intrusion Detection</title>', html, flags=re.IGNORECASE)
    html = re.sub(r'<title>\s*EliTechWiz\s*-\s*it-has-survived\s*</title>', f'<title>{NAME} - Architectural Visualization</title>', html, flags=re.IGNORECASE)
    html = re.sub(r'<title>\s*EliTechWiz\s*-\s*why-do-we-use-it\s*</title>', f'<title>{NAME} - Security Audit Tool</title>', html, flags=re.IGNORECASE)

    # ── 15. Testimonials ─────────────────────────────────────────────────────────
    html = html.replace('<h5 class="name">Darlene Robertson</h5>', '<h5 class="name">sirtheprogrammer</h5>')
    html = html.replace('<span class="title">Business man</span>',
                        '<span class="title">Lead Developer @ codeskytz</span>', 1)
    html = re.sub(
        r'Maecenas tempus tellus eget condtum rhoncus sem quam semper libero siamet adipiscing sem neque sed',
        "EliTechWiz's development skill is exceptional. The project was delivered on time and exceeded our expectations in every way. A true professional.",
        html, count=1
    )

    # ── 16. Contact info everywhere ──────────────────────────────────────────────
    html = re.sub(r'pefen68316@iucake\.com', EMAIL, html)
    html = re.sub(r'01365899882', WHATSAPP, html)
    html = re.sub(r'phone: "[^"]+"', f'phone: "{WHATSAPP}"', html)
    # Phone number in visible text
    html = re.sub(r'\+\d{2,3}\s?\d{3,4}\s?\d{3,4}\s?\d{3,4}', PHONE, html)
    # Generic "example.com" social links in footer
    html = re.sub(r'href="http://example\.com/"', f'href="{GITHUB_URL}"', html)

    # ── 17. Footer social links block ────────────────────────────────────────────
    m = re.search(r'<ul class="social-links">.*?</ul>', html, flags=re.DOTALL)
    if m:
        html = html[:m.start()] + SOCIAL_LINKS_HTML + html[m.end():]

    # ── 18. Footer email ─────────────────────────────────────────────────────────
    html = re.sub(
        r'href="mailto:[^"]+">(?:[^<]+)</a>',
        f'href="mailto:{EMAIL}">{EMAIL}</a>',
        html
    )

    # ── 19. Footer "Stay Connected" email input placeholder ──────────────────────
    html = html.replace('placeholder="Enter Your Email"', 'placeholder="Enter Your Email"')  # keep as-is (functional)

    # ── 20. Footer copyright ─────────────────────────────────────────────────────
    html = re.sub(r'Copyright \d+\s*\n?\s*All Rights Reserved', f'© 2026 {NAME}. All Rights Reserved.', html)

    # ── 21. Meta tags ────────────────────────────────────────────────────────────
    html = re.sub(
        r'<meta name="description" content="">',
        f'<meta name="description" content="{NAME} - Cybersecurity Expert, Software Architect &amp; Creative Designer.">',
        html, count=1
    )
    html = re.sub(
        r'<meta name="keywords" content="">',
        '<meta name="keywords" content="cybersecurity, software development, UI/UX design, EliTechWiz, penetration testing, ethical hacking">',
        html, count=1
    )

    # ── 22. Blog author names ────────────────────────────────────────────────────
    html = re.sub(r'\bby\s+elitechwiz\b', f'by elitechwiz', html)  # already replaced above via ronaldcortez

    # ── 23. Contact form action stays pointing to profilez (it's a live form)
    #        but swap hidden username field
    html = html.replace('name="username" value="elitechwiz"', 'name="username" value="elitechwiz"')  # already done

    return html


# ── Copy source folder to destination ─────────────────────────────────────────
if DEST_DIR.exists():
    shutil.rmtree(DEST_DIR)
shutil.copytree(SRC_DIR, DEST_DIR)
print(f"[COPY] {SRC_DIR} -> {DEST_DIR}")

# ── Process every HTML file ────────────────────────────────────────────────────
html_files = list(DEST_DIR.rglob("*.html"))
print(f"[INFO] Found {len(html_files)} HTML file(s) to process...\n")

for html_file in html_files:
    try:
        raw = html_file.read_text(encoding="utf-8", errors="replace")
        updated = apply_global_replacements(raw, html_file.name)
        html_file.write_text(updated, encoding="utf-8")
        rel = html_file.relative_to(DEST_DIR)
        print(f"  [OK] {rel}")
    except Exception as exc:
        print(f"  [ERR] {html_file.relative_to(DEST_DIR)}: {exc}")

print(f"\n✅ All {len(html_files)} pages customized.")
print(f"\n🌐 Starting local server on http://localhost:{PORT}/elitechwiz/")
print("   Press Ctrl+C to stop.\n")

# ── Serve the site ─────────────────────────────────────────────────────────────
serve_root = DEST_DIR.parent  # serves downloaded_site/profilez.xyz/
os.chdir(serve_root)

handler = http.server.SimpleHTTPRequestHandler
handler.extensions_map.update({
    ".css": "text/css",
    ".js": "application/javascript",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
})

with socketserver.TCPServer(("", PORT), handler) as httpd:
    httpd.serve_forever()
    r'Copyright \d+\s+All Rights Reserved',
