import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def create_luna_art(size=1024, style="circle"):
    """
    Creates a high-resolution, modern artwork for Luna Music.
    Themes: Crescent Moon ('Luna'), Glowing Music Note, Celestial Gradient.
    """
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    center = size / 2.0
    
    # 1. Background
    bg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    
    if style == "circle":
        radius = size * 0.46
        # Multi-stop radial background gradient
        for r in range(int(radius), 0, -1):
            ratio = r / radius
            # Deep cosmic midnight blue
            red = int(12 + (30 - 12) * (1 - ratio)**1.5)
            green = int(16 + (45 - 16) * (1 - ratio)**1.5)
            blue = int(28 + (85 - 28) * (1 - ratio)**1.5)
            bg_draw.ellipse([center - r, center - r, center + r, center + r], fill=(red, green, blue, 255))
    elif style == "rounded":
        radius = size * 0.46
        corner = int(size * 0.22)
        # Rounded squircle
        bbox = [center - radius, center - radius, center + radius, center + radius]
        bg_draw.rounded_rectangle(bbox, radius=corner, fill=(14, 18, 32, 255))
        # Inner subtle gradient
        for r in range(int(radius), 0, -2):
            ratio = r / radius
            red = int(12 + (30 - 12) * (1 - ratio)**1.5)
            green = int(16 + (45 - 16) * (1 - ratio)**1.5)
            blue = int(28 + (85 - 28) * (1 - ratio)**1.5)
            bg_draw.ellipse([center - r, center - r, center + r, center + r], fill=(red, green, blue, 255))
    else: # transparent
        pass
        
    canvas = Image.alpha_composite(canvas, bg)
    
    # 2. Celestial Nebula Glow inside
    nebula = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    neb_draw = ImageDraw.Draw(nebula)
    # Cyan-violet glow in upper left and lower center
    neb_draw.ellipse([center - size*0.35, center - size*0.35, center + size*0.1, center + size*0.1], fill=(56, 189, 248, 60))
    neb_draw.ellipse([center - size*0.1, center - size*0.1, center + size*0.35, center + size*0.35], fill=(168, 85, 247, 60))
    nebula = nebula.filter(ImageFilter.GaussianBlur(radius=size*0.12))
    
    # Mask nebula to circle/rounded background if applicable
    if style in ("circle", "rounded"):
        mask = Image.new('L', (size, size), 0)
        m_draw = ImageDraw.Draw(mask)
        radius = size * 0.46
        if style == "circle":
            m_draw.ellipse([center - radius, center - radius, center + radius, center + radius], fill=255)
        else:
            m_draw.rounded_rectangle([center - radius, center - radius, center + radius, center + radius], radius=int(size * 0.22), fill=255)
        canvas.paste(nebula, (0, 0), mask=mask)
    else:
        canvas = Image.alpha_composite(canvas, nebula)

    # 3. Luna Crescent Moon
    moon_raw = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    m_draw = ImageDraw.Draw(moon_raw)
    
    m_cx = center - size * 0.05
    m_cy = center
    m_r = size * 0.33
    
    # Outer circle with vibrant cyan to electric violet gradient
    for r in range(int(m_r), 0, -1):
        ratio = r / m_r
        # Glowing gradient from #38BDF8 (sky blue) to #A855F7 (purple) to #E0E7FF (white-silver)
        red = int(140 + (240 - 140) * ratio)
        green = int(210 + (245 - 210) * ratio)
        blue = int(255)
        m_draw.ellipse([m_cx - r, m_cy - r, m_cx + r, m_cy + r], fill=(red, green, blue, 255))
        
    # Subtract inner circle to form crescent
    sub_raw = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sub_raw)
    s_cx = m_cx + size * 0.15
    s_cy = m_cy - size * 0.02
    s_r = m_r * 0.86
    s_draw.ellipse([s_cx - s_r, s_cy - s_r, s_cx + s_r, s_cy + s_r], fill=(0, 0, 0, 255))
    
    r_ch, g_ch, b_ch, a_ch = moon_raw.split()
    sub_a = sub_raw.split()[3]
    moon_mask = ImageChops.subtract(a_ch, sub_a)
    
    moon_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    moon_layer.paste(moon_raw, (0, 0), mask=moon_mask)
    
    # 4. Music Note (embraced inside the crescent moon)
    note_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    n_draw = ImageDraw.Draw(note_layer)
    
    # Note head (slanted ellipse)
    nh_x = center + size * 0.06
    nh_y = center + size * 0.15
    nh_rx = size * 0.105
    nh_ry = size * 0.078
    
    # Rotate note head slightly
    nh_canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    nh_draw = ImageDraw.Draw(nh_canvas)
    nh_draw.ellipse([nh_x - nh_rx, nh_y - nh_ry, nh_x + nh_rx, nh_y + nh_ry], fill=(245, 248, 255, 255))
    
    # Stem
    stem_w = size * 0.038
    stem_x = nh_x + nh_rx * 0.72
    stem_top_y = center - size * 0.22
    nh_draw.rounded_rectangle([stem_x - stem_w, stem_top_y, stem_x, nh_y], radius=int(stem_w/2), fill=(245, 248, 255, 255))
    
    # Beam / Flag curve flowing gracefully
    flag_w = int(stem_w * 1.1)
    # Elegant arc
    nh_draw.arc([stem_x - stem_w, stem_top_y, stem_x + size * 0.22, stem_top_y + size * 0.28], 
                start=260, end=40, fill=(245, 248, 255, 255), width=flag_w)
    
    note_layer = Image.alpha_composite(note_layer, nh_canvas)
    
    # Combine Moon + Note
    symbol_layer = Image.alpha_composite(moon_layer, note_layer)
    
    # 5. Dual Glow Layers
    glow_cyan = symbol_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.025))
    glow_purple = symbol_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.065))
    
    # Tint glow
    g_p_r, g_p_g, g_p_b, g_p_a = glow_purple.split()
    tint_p = Image.new('RGBA', (size, size), (168, 85, 247, 180))
    tinted_purple = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    tinted_purple.paste(tint_p, (0, 0), mask=g_p_a)
    
    # Composite all layers
    canvas = Image.alpha_composite(canvas, tinted_purple)
    canvas = Image.alpha_composite(canvas, glow_cyan)
    canvas = Image.alpha_composite(canvas, symbol_layer)
    
    return canvas

def create_feature_graphic(width=1024, height=500):
    img = Image.new('RGBA', (width, height), (10, 14, 26, 255))
    draw = ImageDraw.Draw(img)
    
    # Subtle space gradient
    for x in range(width):
        ratio = x / width
        r = int(10 + 15 * math.sin(ratio * math.pi))
        g = int(14 + 20 * math.sin(ratio * math.pi))
        b = int(26 + 45 * math.sin(ratio * math.pi))
        draw.line([(x, 0), (x, height)], fill=(r, g, b, 255))
        
    # Ambient glows
    ambient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    amb_draw = ImageDraw.Draw(ambient)
    amb_draw.ellipse([width * 0.1, height * 0.1, width * 0.5, height * 0.9], fill=(56, 189, 248, 80))
    amb_draw.ellipse([width * 0.55, height * 0.15, width * 0.95, height * 0.95], fill=(168, 85, 247, 80))
    ambient = ambient.filter(ImageFilter.GaussianBlur(radius=80))
    img = Image.alpha_composite(img, ambient)
    
    # Place Luna Icon on left
    icon = create_luna_art(340, style="circle")
    img.alpha_composite(icon, (80, (height - 340) // 2))
    
    # Render stylized Text "Luna Music"
    # Draw simple clean text lines if font is default
    t_draw = ImageDraw.Draw(img)
    # Title
    t_draw.text((470, 180), "Luna Music", fill=(255, 255, 255, 255))
    t_draw.text((470, 230), "Experience music reimagined. Ad-free, open source.", fill=(186, 230, 253, 220))
    t_draw.text((470, 270), "Background Playback • Synced Lyrics • Hi-Res Audio", fill=(192, 132, 252, 220))
    
    return img

def main():
    print("Generating Luna Music branding assets...")
    os.makedirs("composeApp/src/commonMain/composeResources/drawable", exist_ok=True)
    os.makedirs("composeApp/icon", exist_ok=True)
    os.makedirs("androidApp/src/main/res/drawable", exist_ok=True)
    os.makedirs("androidApp/src/main/res/drawable-v24", exist_ok=True)
    
    # 1. High-res base icons
    circle_512 = create_luna_art(512, style="circle")
    rounded_512 = create_luna_art(512, style="rounded")
    transparent_512 = create_luna_art(512, style="transparent")
    
    circle_512.save("composeApp/src/commonMain/composeResources/drawable/app_icon.png")
    circle_512.save("composeApp/src/commonMain/composeResources/drawable/circle_app_icon.png")
    circle_512.save("androidApp/src/main/res/drawable/app_icon.png")
    circle_512.save("composeApp/icon/circle_app_icon.png")
    rounded_512.save("composeApp/icon/rounded_app_icon.png")
    
    # 2. Windows ICO
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    circle_512.save("composeApp/icon/circle_app_icon.ico", format="ICO", sizes=ico_sizes)
    
    # 3. macOS ICNS
    try:
        circle_512.save("composeApp/icon/circle_app_icon.icns", format="ICNS")
        rounded_512.save("composeApp/icon/rounded_app_icon.icns", format="ICNS")
    except Exception as e:
        print("Note on ICNS:", e)
        
    # 4. Android Mipmaps
    mipmap_configs = {
        "mipmap-mdpi": (48, 108),
        "mipmap-hdpi": (72, 162),
        "mipmap-xhdpi": (96, 216),
        "mipmap-xxhdpi": (144, 324),
        "mipmap-xxxhdpi": (192, 432),
    }
    
    for folder, (ic_size, fg_size) in mipmap_configs.items():
        dir_path = os.path.join("androidApp/src/main/res", folder)
        os.makedirs(dir_path, exist_ok=True)
        
        ic = circle_512.resize((ic_size, ic_size), Image.Resampling.LANCZOS)
        ic.save(os.path.join(dir_path, "ic_launcher.webp"), format="WEBP")
        ic.save(os.path.join(dir_path, "ic_launcher_round.webp"), format="WEBP")
        
        fg = transparent_512.resize((fg_size, fg_size), Image.Resampling.LANCZOS)
        fg.save(os.path.join(dir_path, "ic_launcher_foreground.webp"), format="WEBP")
        fg.save(os.path.join(dir_path, "ic_launcher_round_foreground.webp"), format="WEBP")
        
    # 5. Fastlane metadata images
    os.makedirs("fastlane/metadata/android/en-US/images", exist_ok=True)
    os.makedirs("fastlane/metadata/android/vi-VN/images", exist_ok=True)
    circle_512.save("fastlane/metadata/android/en-US/images/icon.png")
    circle_512.save("fastlane/metadata/android/vi-VN/images/icon.png")
    
    feature_graphic = create_feature_graphic()
    feature_graphic.save("fastlane/metadata/android/en-US/images/featureGraphic.png")
    feature_graphic.save("fastlane/metadata/android/vi-VN/images/featureGraphic.png")
    
    # 6. Vector Drawables (monochrome.xml, ic_launcher_foreground.xml, ic_launcher_background.xml)
    # A sleek crescent moon and musical note in Vector format:
    monochrome_xml = """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <!-- Luna Crescent Moon -->
    <path
        android:fillColor="#000000"
        android:fillType="evenOdd"
        android:pathData="M 50,22 C 32.33,22 18,36.33 18,54 C 18,71.67 32.33,86 50,86 C 58.2,86 65.7,82.9 71.4,77.8 C 55,76 42,62 42,45 C 42,34.2 47.7,24.8 56.2,22.6 C 54.2,22.2 52.1,22 50,22 Z" />
    <!-- Luna Music Note -->
    <path
        android:fillColor="#000000"
        android:pathData="M 64,36 L 64,65 C 62.2,63.8 59.7,63 57,63 C 51.5,63 47,66.6 47,71 C 47,75.4 51.5,79 57,79 C 62.5,79 67,75.4 67,71 L 67,46 L 82,42 L 82,32 Z" />
</vector>
"""
    with open("composeApp/src/commonMain/composeResources/drawable/monochrome.xml", "w", encoding="utf-8") as f:
        f.write(monochrome_xml)
    with open("androidApp/src/main/res/drawable/monochrome.xml", "w", encoding="utf-8") as f:
        f.write(monochrome_xml)

    foreground_xml = """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <!-- Luna Crescent Moon -->
    <path
        android:fillColor="#8BE9FD"
        android:fillType="evenOdd"
        android:pathData="M 50,22 C 32.33,22 18,36.33 18,54 C 18,71.67 32.33,86 50,86 C 58.2,86 65.7,82.9 71.4,77.8 C 55,76 42,62 42,45 C 42,34.2 47.7,24.8 56.2,22.6 C 54.2,22.2 52.1,22 50,22 Z" />
    <!-- Luna Music Note -->
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M 64,36 L 64,65 C 62.2,63.8 59.7,63 57,63 C 51.5,63 47,66.6 47,71 C 47,75.4 51.5,79 57,79 C 62.5,79 67,75.4 67,71 L 67,46 L 82,42 L 82,32 Z" />
</vector>
"""
    with open("androidApp/src/main/res/drawable-v24/ic_launcher_foreground.xml", "w", encoding="utf-8") as f:
        f.write(foreground_xml)

    background_xml = """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0E1220"
        android:pathData="M 0,0 L 108,0 L 108,108 L 0,108 Z" />
    <path
        android:fillColor="#1A233A"
        android:pathData="M 0,0 L 108,0 L 108,54 L 0,54 Z" />
</vector>
"""
    with open("composeApp/src/commonMain/composeResources/drawable/ic_launcher_background.xml", "w", encoding="utf-8") as f:
        f.write(background_xml)

    print("All Luna branding assets successfully generated!")

if __name__ == "__main__":
    main()
