"""Builds the blog from the text files in posts/.

To add a post: copy posts/_template.txt, rename it (e.g. 04-my-post.txt),
write your text, then run:  python3 build.py

Creates blog/index.html (the list) and blog/<slug>/index.html for every post,
so a post lives at biancacardona.com/blog/<slug>.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
POSTS = ROOT / "posts"
BLOG = ROOT / "blog"

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">'
)


def inline(text):
    """Escape HTML, then turn *words* into italics."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(text, quote=False))


def plain(text):
    return text.replace("*", "")


def body_to_html(body):
    blocks = [b for b in re.split(r"\n\s*\n", body.strip()) if b.strip()]
    out = []
    for block in blocks:
        lines = [l.rstrip() for l in block.strip("\n").split("\n")]
        if all(l.lstrip().startswith(">") for l in lines):
            parts = []
            for l in lines:
                l = l.lstrip()[1:].strip()
                if l.startswith("~"):
                    parts.append(f"<cite>{inline(l[1:].strip())}</cite>")
                else:
                    parts.append(f"<p>{inline(l)}</p>")
            out.append("<blockquote>" + "".join(parts) + "</blockquote>")
        else:
            out.append("<p>" + "<br>\n".join(inline(l.strip()) for l in lines) + "</p>")
    return "\n      ".join(out)


def page(title, prefix, main):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  {FONTS}
  <link rel="stylesheet" href="{prefix}styles.css">
</head>
<body>
  <header class="nav">
    <span class="logo">B.C.</span>
    <nav class="nav-links">
      <a href="{prefix}index.html">about</a>
      <a href="{prefix}projects.html">projects</a>
      <a href="{prefix}blog/" aria-current="page">blog</a>
      <a href="{prefix}hobbies.html">hobbies</a>
    </nav>
  </header>
{main}
</body>
</html>
"""


def load_posts():
    posts = []
    for f in sorted(POSTS.glob("*.txt")):
        if f.name.startswith("_"):
            continue
        first, _, rest = f.read_text(encoding="utf-8").partition("\n")
        if not first.lower().startswith("title:"):
            raise SystemExit(f"{f.name}: first line must start with 'title:'")
        slug = re.sub(r"^\d+[-_ ]*", "", f.stem).strip().lower().replace(" ", "-")
        posts.append({"title": first[6:].strip(), "slug": slug, "body": rest})
    return posts


def main():
    posts = load_posts()
    BLOG.mkdir(exist_ok=True)

    items = "\n".join(
        f'      <li><a href="{p["slug"]}/">{inline(p["title"])}</a></li>' for p in posts
    )
    index_main = f"""  <main class="blog">
    <h1>blog</h1>
    <ul class="post-list">
{items}
    </ul>
  </main>"""
    (BLOG / "index.html").write_text(page("blog | bianca cardona", "../", index_main), encoding="utf-8")

    for p in posts:
        d = BLOG / p["slug"]
        d.mkdir(exist_ok=True)
        post_main = f"""  <main class="post">
    <article>
      <h1>{inline(p["title"])}</h1>
      {body_to_html(p["body"])}
    </article>
    <a class="back" href="../">&larr; all posts</a>
  </main>"""
        title = f'{html.escape(plain(p["title"]), quote=False)} | bianca cardona'
        (d / "index.html").write_text(page(title, "../../", post_main), encoding="utf-8")

    print(f"built {len(posts)} posts:")
    for p in posts:
        print(f"  /blog/{p['slug']}")


if __name__ == "__main__":
    main()
