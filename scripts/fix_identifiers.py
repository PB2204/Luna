import os

ROOT_DIR = os.path.abspath(".")

REPLACEMENTS = [
    ("Luna MusicApplication", "LunaApplication"),
    ("Luna MusicCarAppService", "LunaCarAppService"),
    ("Luna MusicCarSession", "LunaCarSession"),
    ("Luna MusicLyricsClient", "LunaLyricsClient"),
    ("Luna MusicLyricsApiException", "LunaLyricsApiException"),
    ("Luna MusicLyricsFailure", "LunaLyricsFailure"),
    ("Luna MusicLyricsRepository", "LunaLyricsRepository"),
    ("Luna MusicLyrics", "LunaLyrics"),
    ("Luna MusicTranslatedLyrics", "LunaTranslatedLyrics"),
    ("Luna MusicChartButton", "LunaChartButton"),
    ("Luna MusicChartResponse", "LunaChartResponse"),
    ("Luna MusicChart", "LunaChart"),
    ("Luna MusicTest", "LunaTest"),
    ("Luna Music_", "Luna_"),
    ("com.maxrave.luna", "com.luna.music"),
    ("com.luna.simpmusic", "com.luna.music"),
    ("SimpMusic", "Luna"),
    ("simpmusic", "luna"),
]

EXTS = {".kt", ".kts", ".java", ".xml", ".properties", ".conf", ".json", ".pro", ".md", ".txt", ".yml", ".yaml", ".sh", ".bat"}
IGNORE_DIRS = {".git", ".gradle", "build", "mpv-cache", ".idea"}

def fix_identifiers():
    print("Fixing identifiers...")
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in EXTS:
                p = os.path.join(root, f)
                try:
                    with open(p, "r", encoding="utf-8") as fp:
                        content = fp.read()
                except Exception:
                    continue
                orig = content
                for old, new in REPLACEMENTS:
                    content = content.replace(old, new)
                if content != orig:
                    with open(p, "w", encoding="utf-8") as fp:
                        fp.write(content)
                    print(f"Fixed: {p}")

def rename_specific_files():
    renames = [
        ("core/media/media3/src/main/java/com/luna/media3/carapp/SimpMusicCarAppService.kt",
         "core/media/media3/src/main/java/com/luna/media3/carapp/LunaCarAppService.kt"),
        ("core/service/lyricsService/src/commonMain/kotlin/com/luna/lyrics/SimpMusicLyrics.kt",
         "core/service/lyricsService/src/commonMain/kotlin/com/luna/lyrics/LunaLyrics.kt"),
        ("core/service/lyricsService/src/commonMain/kotlin/com/luna/lyrics/SimpMusicLyricsClient.kt",
         "core/service/lyricsService/src/commonMain/kotlin/com/luna/lyrics/LunaLyricsClient.kt"),
        ("core/service/kotlinYtmusicScraper/src/commonMain/kotlin/com/luna/kotlinytmusicscraper/models/response/SimpMusicChartResponse.kt",
         "core/service/kotlinYtmusicScraper/src/commonMain/kotlin/com/luna/kotlinytmusicscraper/models/response/LunaChartResponse.kt"),
        ("composeApp/src/commonMain/kotlin/com/luna/music/ui/component/SimpMusicChart.kt",
         "composeApp/src/commonMain/kotlin/com/luna/music/ui/component/LunaChart.kt"),
    ]
    for old, new in renames:
        old_p = os.path.join(ROOT_DIR, old.replace("/", os.sep))
        new_p = os.path.join(ROOT_DIR, new.replace("/", os.sep))
        if os.path.exists(old_p):
            os.rename(old_p, new_p)
            print(f"Renamed: {old_p} -> {new_p}")

if __name__ == "__main__":
    fix_identifiers()
    rename_specific_files()
    print("Identifier fix complete!")
