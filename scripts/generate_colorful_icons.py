import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def create_vibrant_luna_art(size=1024, style="circle"):
    """
    Creates an ultra-vibrant, colorful, modern artwork for Luna Music with safe-zone padding.
    Features:
      - Rich cosmic nebula background (deep royal purple, indigo, radiant magenta & cyan aurora)
      - Highly colorful, luminous crescent moon with sunset-coral, electric magenta, violet, and tropical cyan gradient
      - Glowing music note with golden starlight
      - Celestial sparkle stars
      - Guaranteed safe-zone dimensions for Android adaptive icon masks (squircle/circle) and Android 12+ splash screen.
    """
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    center = size / 2.0
    
    # 1. Background
    bg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    radius = size * 0.46
    
    if style == "circle":
        # Multi-stop radial cosmic background
        for r in range(int(radius), 0, -1):
            ratio = r / radius  # 1.0 at edge, 0.0 at center
            red = int(58 + (22 - 58) * (ratio ** 1.2))
            green = int(22 + (12 - 22) * (ratio ** 1.2))
            blue = int(110 + (42 - 110) * (ratio ** 1.2))
            bg_draw.ellipse([center - r, center - r, center + r, center + r], fill=(red, green, blue, 255))
    elif style == "rounded":
        corner = int(size * 0.22)
        bbox = [center - radius, center - radius, center + radius, center + radius]
        bg_draw.rounded_rectangle(bbox, radius=corner, fill=(26, 12, 52, 255))
        for r in range(int(radius), 0, -2):
            ratio = r / radius
            red = int(58 + (22 - 58) * (ratio ** 1.2))
            green = int(22 + (12 - 22) * (ratio ** 1.2))
            blue = int(110 + (42 - 110) * (ratio ** 1.2))
            bg_draw.ellipse([center - r, center - r, center + r, center + r], fill=(red, green, blue, 255))
    elif style == "full_bg":
        # Full rectangular 108dp background for adaptive icon layer
        for r in range(int(size * 0.72), 0, -2):
            ratio = r / (size * 0.72)
            red = int(58 + (22 - 58) * (ratio ** 1.2))
            green = int(22 + (12 - 22) * (ratio ** 1.2))
            blue = int(110 + (42 - 110) * (ratio ** 1.2))
            bg_draw.ellipse([center - r, center - r, center + r, center + r], fill=(red, green, blue, 255))
    else:
        # transparent foreground for adaptive icon
        pass

    canvas = Image.alpha_composite(canvas, bg)

    # 2. Rich Colorful Nebula Clouds (if background enabled)
    if style in ("circle", "rounded", "full_bg"):
        nebula = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        neb_draw = ImageDraw.Draw(nebula)
        # Vibrant magenta glow in upper right
        neb_draw.ellipse([center - size*0.1, center - size*0.38, center + size*0.42, center + size*0.12], fill=(236, 72, 153, 110))
        # Vibrant cyan / turquoise glow in lower left
        neb_draw.ellipse([center - size*0.42, center - size*0.12, center + size*0.12, center + size*0.42], fill=(6, 182, 212, 110))
        # Electric violet glow in upper left
        neb_draw.ellipse([center - size*0.38, center - size*0.4, center + size*0.08, center + size*0.08], fill=(168, 85, 247, 90))
        # Warm golden glow near center
        neb_draw.ellipse([center - size*0.05, center - size*0.05, center + size*0.25, center + size*0.25], fill=(245, 158, 11, 75))
        
        nebula = nebula.filter(ImageFilter.GaussianBlur(radius=size * 0.12))
        
        # Mask nebula if circular/rounded
        if style in ("circle", "rounded"):
            mask = Image.new('L', (size, size), 0)
            m_draw = ImageDraw.Draw(mask)
            if style == "circle":
                m_draw.ellipse([center - radius, center - radius, center + radius, center + radius], fill=255)
            else:
                m_draw.rounded_rectangle([center - radius, center - radius, center + radius, center + radius], radius=int(size * 0.22), fill=255)
            canvas.paste(nebula, (0, 0), mask=mask)
        else:
            canvas = Image.alpha_composite(canvas, nebula)

    # 3. Vibrant Multicolor Luna Crescent Moon (Safe-zone scaled)
    # The scale ensures max radius <= 0.27 * size (well inside 0.305 safe limit)
    moon_raw = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    m_cx = center - size * 0.035
    m_cy = center
    m_r = size * 0.225

    # Multi-color gradient for moon
    gradient_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient_img)
    
    y_min = int(m_cy - m_r)
    y_max = int(m_cy + m_r)
    height_span = max(1, y_max - y_min)
    
    for y in range(y_min, y_max + 1):
        t = (y - y_min) / height_span
        if t < 0.33:
            # Sunset Coral (#ff5900) to Fuchsia (#ff007f)
            st = t / 0.33
            r = 255
            g = int(89 * (1 - st) + 0 * st)
            b = int(0 * (1 - st) + 127 * st)
        elif t < 0.66:
            # Fuchsia (#ff007f) to Electric Violet (#8b5cf6)
            st = (t - 0.33) / 0.33
            r = int(255 * (1 - st) + 139 * st)
            g = int(0 * (1 - st) + 92 * st)
            b = int(127 * (1 - st) + 246 * st)
        else:
            # Electric Violet (#8b5cf6) to Tropical Cyan (#00f0ff)
            st = (t - 0.66) / 0.34
            r = int(139 * (1 - st) + 0 * st)
            g = int(92 * (1 - st) + 240 * st)
            b = int(246 * (1 - st) + 255 * st)
        g_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Outer moon mask
    moon_mask = Image.new('L', (size, size), 0)
    mm_draw = ImageDraw.Draw(moon_mask)
    mm_draw.ellipse([m_cx - m_r, m_cy - m_r, m_cx + m_r, m_cy + m_r], fill=255)
    
    # Cutout circle for crescent shape
    cutout_cx = m_cx + size * 0.08
    cutout_cy = m_cy - size * 0.01
    cutout_r = size * 0.19
    mm_draw.ellipse([cutout_cx - cutout_r, cutout_cy - cutout_r, cutout_cx + cutout_r, cutout_cy + cutout_r], fill=0)
    
    moon_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    moon_layer.paste(gradient_img, (0, 0), mask=moon_mask)

    # 4. Stylized Luminous Music Note (Safe-zone scaled)
    nh_canvas = Image.new('L', (size, size), 0)
    nh_draw = ImageDraw.Draw(nh_canvas)
    
    nh_x = center + size * 0.035
    nh_y = center + size * 0.08
    nh_rx = size * 0.085
    nh_ry = size * 0.06
    
    # Draw rotated elliptical note head
    nh_temp = Image.new('L', (size, size), 0)
    t_draw = ImageDraw.Draw(nh_temp)
    t_draw.ellipse([nh_x - nh_rx, nh_y - nh_ry, nh_x + nh_rx, nh_y + nh_ry], fill=255)
    nh_rot = nh_temp.rotate(-22, resample=Image.Resampling.BICUBIC, center=(int(nh_x), int(nh_y)))
    nh_canvas = ImageChops.lighter(nh_canvas, nh_rot)
    
    # Stem
    stem_w = int(size * 0.022)
    stem_x = int(nh_x + nh_rx * 0.68)
    stem_top_y = int(center - size * 0.17)
    stem_bot_y = int(nh_y)
    nh_draw.rectangle([stem_x - stem_w//2, stem_top_y, stem_x + stem_w//2, stem_bot_y], fill=255)
    
    # Flag curve
    flag_w = int(stem_w * 1.05)
    nh_draw.arc([stem_x - stem_w, stem_top_y, stem_x + int(size * 0.14), stem_top_y + int(size * 0.19)], 
                start=260, end=40, fill=255, width=flag_w)
    
    # Note gradient: luminous starlight gold (#fff7ed) down to sparkling azure (#38bdf8)
    note_grad = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ng_draw = ImageDraw.Draw(note_grad)
    for y in range(int(stem_top_y), int(nh_y + nh_ry) + 1):
        t = (y - stem_top_y) / max(1, (nh_y + nh_ry - stem_top_y))
        r = int(255 * (1 - t) + 56 * t)
        g = int(250 * (1 - t) + 189 * t)
        b = int(230 * (1 - t) + 248 * t)
        ng_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
        
    note_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    note_layer.paste(note_grad, (0, 0), mask=nh_canvas)

    # 5. Celestial Sparkle Stars (Safe-zone bounded)
    def draw_star(draw_obj, cx, cy, arm_len, width, color):
        pts_h = [(cx - arm_len, cy), (cx + arm_len, cy)]
        pts_v = [(cx, cy - arm_len), (cx, cy + arm_len)]
        draw_obj.line(pts_h, fill=color, width=width)
        draw_obj.line(pts_v, fill=color, width=width)
        r_d = arm_len * 0.35
        draw_obj.polygon([(cx, cy - r_d), (cx + r_d, cy), (cx, cy + r_d), (cx - r_d, cy)], fill=color)

    stars_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stars_layer)
    
    # Bright golden sparkle at top right
    draw_star(s_draw, center + size * 0.165, center - size * 0.18, size * 0.040, int(size * 0.010), (254, 240, 138, 255))
    # Electric cyan sparkle near upper curve
    draw_star(s_draw, center + size * 0.015, center - size * 0.22, size * 0.028, int(size * 0.008), (103, 232, 249, 255))
    # Magenta sparkle at bottom left
    draw_star(s_draw, center - size * 0.17, center + size * 0.20, size * 0.030, int(size * 0.008), (244, 114, 182, 255))
    # Small starlight dot
    s_draw.ellipse([center + size*0.22 - size*0.008, center + size*0.06 - size*0.008,
                    center + size*0.22 + size*0.008, center + size*0.06 + size*0.008], fill=(255, 255, 255, 220))

    # Combine symbols
    symbol_layer = Image.alpha_composite(moon_layer, note_layer)
    symbol_layer = Image.alpha_composite(symbol_layer, stars_layer)

    # 6. Radiant Neon Glows
    glow_p = symbol_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.035))
    _, _, _, a_p = glow_p.split()
    tint_p = Image.new('RGBA', (size, size), (236, 72, 153, 200))
    glow_p_tinted = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_p_tinted.paste(tint_p, (0, 0), mask=a_p)

    glow_c = symbol_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.018))
    _, _, _, a_c = glow_c.split()
    tint_c = Image.new('RGBA', (size, size), (6, 182, 212, 190))
    glow_c_tinted = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_c_tinted.paste(tint_c, (0, 0), mask=a_c)

    # Composite all layers
    canvas = Image.alpha_composite(canvas, glow_p_tinted)
    canvas = Image.alpha_composite(canvas, glow_c_tinted)
    canvas = Image.alpha_composite(canvas, symbol_layer)

    return canvas

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Generating ultra-vibrant colorful Luna Music icons with safe-zone padding...")

    # 1. Master icons (512x512)
    circle_icon = create_vibrant_luna_art(size=512, style="circle")
    rounded_icon = create_vibrant_luna_art(size=512, style="rounded")
    transparent_icon = create_vibrant_luna_art(size=512, style="transparent")

    # Save to composeApp icon folder
    icon_dir = os.path.join(root, "composeApp", "icon")
    os.makedirs(icon_dir, exist_ok=True)
    circle_icon.save(os.path.join(icon_dir, "circle_app_icon.png"), "PNG")
    rounded_icon.save(os.path.join(icon_dir, "rounded_app_icon.png"), "PNG")
    transparent_icon.save(os.path.join(icon_dir, "app_icon.png"), "PNG")
    print("✓ Saved master PNGs to composeApp/icon")

    # 2. Android Mipmap densities
    # (icon_sz is legacy launcher size 48..192; fg_sz is adaptive icon canvas 108..432)
    densities = {
        "mdpi": (48, 108),
        "hdpi": (72, 162),
        "xhdpi": (96, 216),
        "xxhdpi": (144, 324),
        "xxxhdpi": (192, 432),
    }

    res_base = os.path.join(root, "androidApp", "src", "main", "res")
    for name, (icon_sz, fg_sz) in densities.items():
        folder = os.path.join(res_base, f"mipmap-{name}")
        os.makedirs(folder, exist_ok=True)

        # Legacy launcher icon (rounded squircle)
        img_std = rounded_icon.resize((icon_sz, icon_sz), Image.Resampling.LANCZOS)
        img_std.save(os.path.join(folder, "ic_launcher.webp"), "WEBP", quality=95)

        # Legacy round launcher icon (circle)
        img_rnd = circle_icon.resize((icon_sz, icon_sz), Image.Resampling.LANCZOS)
        img_rnd.save(os.path.join(folder, "ic_launcher_round.webp"), "WEBP", quality=95)

        # Adaptive icon foreground layer (with safe-zone padding so OEM masks never crop it!)
        fg_art = create_vibrant_luna_art(size=fg_sz, style="transparent")
        fg_art.save(os.path.join(folder, "ic_launcher_foreground.webp"), "WEBP", quality=95)
        fg_art.save(os.path.join(folder, "ic_launcher_round_foreground.webp"), "WEBP", quality=95)

    print("✓ Saved all vibrant Android mipmap webp icons (safe-zone optimized)")

    # 3. Fastlane Store Assets
    store_dir = os.path.join(root, "fastlane", "metadata", "android", "en-US", "images")
    os.makedirs(store_dir, exist_ok=True)
    circle_icon.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(store_dir, "icon.png"), "PNG")

    # Feature Graphic (1024x500)
    fg_w, fg_h = 1024, 500
    feat_img = Image.new('RGBA', (fg_w, fg_h), (18, 8, 38, 255))
    f_draw = ImageDraw.Draw(feat_img)
    for x in range(fg_w):
        t = x / fg_w
        r = int(24 + (52 - 24) * math.sin(t * math.pi))
        g = int(10 + (28 - 10) * math.sin(t * math.pi))
        b = int(48 + (96 - 48) * math.sin(t * math.pi))
        f_draw.line([(x, 0), (x, fg_h)], fill=(r, g, b, 255))

    logo_art = create_vibrant_luna_art(size=360, style="circle")
    feat_img.paste(logo_art, (70, 70), mask=logo_art)
    feat_img.save(os.path.join(store_dir, "featureGraphic.png"), "PNG")
    print("✓ Saved Fastlane store graphics")

    # 4. Website Assets
    public_assets = os.path.join(root, "public", "assets")
    if os.path.exists(public_assets):
        circle_icon.save(os.path.join(public_assets, "logo.png"), "PNG")
        feat_img.save(os.path.join(public_assets, "banner.png"), "PNG")
        print("✓ Updated public website assets")

    print("\n🎉 All colorful Luna Music icons created successfully with guaranteed safe-zone margins!")

if __name__ == "__main__":
    main()
