import os
import re
import shutil

ROOT_DIR = os.path.abspath(".")

# Replacements in files (ordered carefully so specific ones match first)
TEXT_REPLACEMENTS = [
    # Generated resources package
    ("simpmusic.composeapp.generated.resources", "luna.composeapp.generated.resources"),
    
    # Packages
    ("com.maxrave.simpmusic.composeapp", "com.luna.music.composeapp"),
    ("com.maxrave.simpmusic", "com.luna.music"),
    ("com.maxrave.common", "com.luna.common"),
    ("com.maxrave.logger", "com.luna.logger"),
    ("com.maxrave.data", "com.luna.data"),
    ("com.maxrave.domain", "com.luna.domain"),
    ("com.maxrave.media3", "com.luna.media3"),
    ("com.maxrave.media_jvm_ui", "com.luna.media_jvm_ui"),
    ("com.maxrave.kotlinytmusicscraper", "com.luna.kotlinytmusicscraper"),
    ("com.maxrave.ktorext", "com.luna.ktorext"),
    ("com.maxrave.spotify", "com.luna.spotify"),
    ("com.simpmusic.media_jvm", "com.luna.media_jvm"),
    ("org.simpmusic.aiservice", "com.luna.aiservice"),
    ("org.simpmusic.autoeq", "com.luna.autoeq"),
    ("org.simpmusic.cast", "com.luna.cast"),
    ("org.simpmusic.crashlytics", "com.luna.crashlytics"),
    ("org.simpmusic.discord", "com.luna.discord"),
    ("org.simpmusic.lastfm", "com.luna.lastfm"),
    ("org.simpmusic.listentogether", "com.luna.listentogether"),
    ("org.simpmusic.loginsync", "com.luna.loginsync"),
    ("org.simpmusic.lyrics", "com.luna.lyrics"),
    
    # App Names and Branding in strings/configs
    ("SimpMusic Dev", "Luna Dev"),
    ("SimpMusic Playback Notification", "Luna Music Playback Notification"),
    ("SimpMusic Charts", "Luna Music Charts"),
    ("SimpMusic Lyrics", "Luna Lyrics"),
    ("SimpMusic Wrapped", "Luna Wrapped"),
    ("Downloads/SimpMusic", "Downloads/Luna"),
    ("SimpMusic", "Luna Music"),
    ("simpmusic://", "luna://"),
    ("simpmusic.org", "luna-music.app"),
    ("simpmusic", "luna"),
    
    # Developer / Author info
    ("maxrave-dev", "luna-music"),
    ("maxrave.dev", "luna-music.app"),
    ("Tuan Minh Nguyen Duc", "Luna Team"),
]

# File extensions to process
EXTENSIONS = {
    ".kt", ".kts", ".java", ".xml", ".properties", ".conf", ".json", 
    ".pro", ".md", ".txt", ".yml", ".yaml", ".sh", ".bat", ".gradle"
}

IGNORE_DIRS = {".git", ".gradle", "build", "mpv-cache", ".idea"}

def process_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()
        except Exception:
            return
            
    original_content = content
    
    for old_text, new_text in TEXT_REPLACEMENTS:
        content = content.replace(old_text, new_text)
        
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

def move_package_dir(base_src_dir, old_rel_pkg, new_rel_pkg):
    old_full_path = os.path.join(base_src_dir, old_rel_pkg.replace(".", os.sep))
    new_full_path = os.path.join(base_src_dir, new_rel_pkg.replace(".", os.sep))
    
    if os.path.exists(old_full_path) and old_full_path != new_full_path:
        os.makedirs(new_full_path, exist_ok=True)
        # Move all contents
        for item in os.listdir(old_full_path):
            src_item = os.path.join(old_full_path, item)
            dst_item = os.path.join(new_full_path, item)
            if os.path.exists(dst_item):
                if os.path.isdir(dst_item):
                    shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                    shutil.rmtree(src_item)
                else:
                    os.remove(dst_item)
                    shutil.move(src_item, dst_item)
            else:
                shutil.move(src_item, dst_item)
        
        # Clean up empty old dirs
        curr = old_full_path
        while curr != base_src_dir and os.path.exists(curr) and not os.listdir(curr):
            os.rmdir(curr)
            curr = os.path.dirname(curr)
        print(f"Moved package: {old_full_path} -> {new_full_path}")

def rebrand_all_files():
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in EXTENSIONS or file in {"gradlew", "LICENSE"}:
                filepath = os.path.join(root, file)
                process_file_content(filepath)

def rebrand_directories():
    print("Moving package directories...")
    # Find all source roots (src/.../kotlin, src/.../java)
    source_roots = []
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        base_name = os.path.basename(root)
        if base_name in ("kotlin", "java") and "src" in root:
            source_roots.append(root)
            
    package_mappings = [
        ("com.maxrave.simpmusic", "com.luna.music"),
        ("com.maxrave.common", "com.luna.common"),
        ("com.maxrave.logger", "com.luna.logger"),
        ("com.maxrave.data", "com.luna.data"),
        ("com.maxrave.domain", "com.luna.domain"),
        ("com.maxrave.media3", "com.luna.media3"),
        ("com.maxrave.media_jvm_ui", "com.luna.media_jvm_ui"),
        ("com.maxrave.kotlinytmusicscraper", "com.luna.kotlinytmusicscraper"),
        ("com.maxrave.ktorext", "com.luna.ktorext"),
        ("com.maxrave.spotify", "com.luna.spotify"),
        ("com.simpmusic.media_jvm", "com.luna.media_jvm"),
        ("org.simpmusic.aiservice", "com.luna.aiservice"),
        ("org.simpmusic.autoeq", "com.luna.autoeq"),
        ("org.simpmusic.cast", "com.luna.cast"),
        ("org.simpmusic.crashlytics", "com.luna.crashlytics"),
        ("org.simpmusic.discord", "com.luna.discord"),
        ("org.simpmusic.lastfm", "com.luna.lastfm"),
        ("org.simpmusic.listentogether", "com.luna.listentogether"),
        ("org.simpmusic.loginsync", "com.luna.loginsync"),
        ("org.simpmusic.lyrics", "com.luna.lyrics"),
    ]
    
    for s_root in source_roots:
        for old_pkg, new_pkg in package_mappings:
            move_package_dir(s_root, old_pkg, new_pkg)
            
    # Move Room schemas folder
    old_schema = os.path.join(ROOT_DIR, "core", "data", "schemas", "com.maxrave.data.db.MusicDatabase")
    new_schema = os.path.join(ROOT_DIR, "core", "data", "schemas", "com.luna.data.db.MusicDatabase")
    if os.path.exists(old_schema) and not os.path.exists(new_schema):
        shutil.move(old_schema, new_schema)
        print(f"Moved schema: {old_schema} -> {new_schema}")

if __name__ == "__main__":
    rebrand_all_files()
    rebrand_directories()
    print("Rebranding script complete!")
