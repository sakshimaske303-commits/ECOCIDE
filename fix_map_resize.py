import os

RESIZE_SCRIPT = """
<script>
window.addEventListener('load', function() {
    setTimeout(function() {
        if (typeof map !== 'undefined' && map.updateSize) {
            map.updateSize();
        }
    }, 300);
});
</script>
"""

MAP_FOLDERS = [
    "kherson_flood_extent_webmap",
]

STATIC_DIR = "dashboard/static"


def inject_resize_fix(folder_name):
    index_path = os.path.join(STATIC_DIR, folder_name, "index.html")
    if not os.path.exists(index_path):
        print(f"NOT FOUND: {index_path}")
        return
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "map.updateSize" in content:
        print(f"Already patched: {folder_name}")
        return
    content = content.replace("</body>", RESIZE_SCRIPT + "</body>")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Patched: {folder_name}")


def main():
    for folder in MAP_FOLDERS:
        inject_resize_fix(folder)


if __name__ == "__main__":
    main()