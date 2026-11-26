import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def create_vibrant_luna_art(size=1024, style="circle"):
    """
    Creates an ultra-vibrant, colorful, modern artwork for Luna Music.
    Features:
      - Rich cosmic nebula background (deep royal purple, indigo, radiant magenta & cyan aurora)
      - Highly colorful, luminous crescent moon with sunset-coral, electric magenta, violet, and tropical cyan gradient
      - Glowing music note with golden starlight
      - Celestial sparkle stars
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
            # Gradient: edge deep royal midnight (24, 10, 48) -> center electric indigo/purple (55, 20, 105)
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
    else:  # transparent foreground for adaptive icon
        pass

    canvas = Image.alpha_composite(canvas, bg)

    # 2. Rich Colorful Nebula Clouds (if background enabled)
    if style in ("circle", "rounded"):
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
        
        # Mask nebula to circle/rounded boundary
        mask = Image.new('L', (size, size), 0)
        m_draw = ImageDraw.Draw(mask)
        if style == "circle":
            m_draw.ellipse([center - radius, center - radius, center + radius, center + radius], fill=255)
        else:
            m_draw.rounded_rectangle([center - radius, center - radius, center + radius, center + radius], radius=int(size * 0.22), fill=255)
        canvas.paste(nebula, (0, 0), mask=mask)

    # 3. Vibrant Multicolor Luna Crescent Moon
    # We render the moon disk with a sweeping multi-color gradient from angle / height
    moon_raw = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    m_cx = center - size * 0.05
    m_cy = center
    m_r = size * 0.33

    # Generate a gorgeous multi-color gradient bitmap for the moon
    gradient_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient_img)
    
    # Gradient stops along vertical axis with angle tilt:
    # Top: Vibrant Sunset Amber/Coral (#ff4500 -> #ff007a)
    # Middle: Electric Magenta / Orchid (#d946ef -> #8b5cf6)
    # Bottom: Radiant Sky Cyan & Turquoise (#00f0ff -> #06b6d4)
    y_min = int(m_cy - m_r)
    y_max = int(m_cy + m_r)
    height_span = max(1, y_max - y_min)
    
    for y in range(y_min, y_max + 1):
        t = (y - y_min) / height_span  # 0 at top, 1 at bottom
        if t < 0.33:
            # Coral (#ff5900) to Fuchsia (#ff007f)
            st = t / 0.33
            r = int(255)
            g = int(89 * (1 - st) + 0 * st)
            b = int(0 * (1 - st) + 127 * st)
        elif t < 0.66:
            # Fuchsia (#ff007f) to Electric Violet (#8b5cf6)
            st = (t - 0.33) / 0.33
            r = int(255 * (1 - st) + 139 * st)
            g = int(0 * (1 - st) + 92 * st)
            b = int(127 * (1 - st) + 246 * st)
        else:
            # Electric Violet (#8b5cf6) to Tropical Cyan (#00f5d4)
            st = (t - 0.66) / 0.34
            r = int(139 * (1 - st) + 0 * st)
            g = int(92 * (1 - st) + 245 * st)
            b = int(246 * (1 - st) + 212 * st)
        g_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Mask gradient to outer moon circle
    circle_mask = Image.new('L', (size, size), 0)
    c_draw = ImageDraw.Draw(circle_mask)
    c_draw.ellipse([m_cx - m_r, m_cy - m_r, m_cx + m_r, m_cy + m_r], fill=255)

    # Cut out inner circle to form crescent
    sub_raw = Image.new('L', (size, size), 0)
    s_draw = ImageDraw.Draw(sub_raw)
    s_cx = m_cx + size * 0.15
    s_cy = m_cy - size * 0.02
    s_r = m_r * 0.86
    s_draw.ellipse([s_cx - s_r, s_cy - s_r, s_cx + s_r, s_cy + s_r], fill=255)

    crescent_mask = ImageChops.subtract(circle_mask, sub_raw)
    
    moon_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    moon_layer.paste(gradient_img, (0, 0), mask=crescent_mask)

    # 4. Glowing Music Note with golden-to-cyan gradient
    note_mask = Image.new('L', (size, size), 0)
    n_draw = ImageDraw.Draw(note_mask)
    
    # Note head (slanted ellipse)
    nh_x = center + size * 0.06
    nh_y = center + size * 0.15
    nh_rx = size * 0.105
    nh_ry = size * 0.078
    
    nh_canvas = Image.new('L', (size, size), 0)
    nh_draw = ImageDraw.Draw(nh_canvas)
    nh_draw.ellipse([nh_x - nh_rx, nh_y - nh_ry, nh_x + nh_rx, nh_y + nh_ry], fill=255)
    
    # Stem
    stem_w = size * 0.038
    stem_x = nh_x + nh_rx * 0.72
    stem_top_y = center - size * 0.22
    nh_draw.rounded_rectangle([stem_x - stem_w, stem_top_y, stem_x, nh_y], radius=int(stem_w/2), fill=255)
    
    # Beam / Flag curve flowing gracefully
    flag_w = int(stem_w * 1.1)
    nh_draw.arc([stem_x - stem_w, stem_top_y, stem_x + size * 0.22, stem_top_y + size * 0.28], 
                start=260, end=40, fill=255, width=flag_w)
    
    # Note gradient: luminous starlight gold (#fff7ed -> #fef08a) down to sparkling azure (#38bdf8)
    note_grad = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ng_draw = ImageDraw.Draw(note_grad)
    for y in range(int(stem_top_y), int(nh_y + nh_ry) + 1):
        t = (y - stem_top_y) / max(1, (nh_y + nh_ry - stem_top_y))
        # Top pure warm gold/white (255, 250, 230) -> Bottom vivid electric cyan (56, 189, 248)
        r = int(255 * (1 - t) + 56 * t)
        g = int(250 * (1 - t) + 189 * t)
        b = int(230 * (1 - t) + 248 * t)
        ng_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
        
    note_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    note_layer.paste(note_grad, (0, 0), mask=nh_canvas)

    # 5. Celestial Sparkle Stars
    def draw_star(draw_obj, cx, cy, arm_len, width, color):
        pts_h = [(cx - arm_len, cy), (cx + arm_len, cy)]
        pts_v = [(cx, cy - arm_len), (cx, cy + arm_len)]
        draw_obj.line(pts_h, fill=color, width=width)
        draw_obj.line(pts_v, fill=color, width=width)
        # Small diamond in center
        r_d = arm_len * 0.35
        draw_obj.polygon([(cx, cy - r_d), (cx + r_d, cy), (cx, cy + r_d), (cx - r_d, cy)], fill=color)

    stars_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stars_layer)
    # Bright golden sparkle at top right
    draw_star(s_draw, center + size * 0.24, center - size * 0.26, size * 0.055, int(size * 0.012), (254, 240, 138, 255))
    # Electric cyan sparkle near upper curve
    draw_star(s_draw, center + size * 0.02, center - size * 0.32, size * 0.038, int(size * 0.009), (103, 232, 249, 255))
    # Magenta sparkle at bottom left
    draw_star(s_draw, center - size * 0.25, center + size * 0.28, size * 0.042, int(size * 0.01), (244, 114, 182, 255))
    # Small starlight dot
    s_draw.ellipse([center + size*0.32 - size*0.01, center + size*0.08 - size*0.01,
                    center + size*0.32 + size*0.01, center + size*0.08 + size*0.01], fill=(255, 255, 255, 220))

    # Combine symbols
    symbol_layer = Image.alpha_composite(moon_layer, note_layer)
    symbol_layer = Image.alpha_composite(symbol_layer, stars_layer)

    # 6. Radiant Neon Glows (Dual halo: vibrant magenta-pink + bright cyan)
    # Magenta glow
    glow_p = symbol_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.055))
    r_ch, g_ch, b_ch, a_ch = glow_p.split()
    tint_p = Image.new('RGBA', (size, size), (236, 72, 153, 210))
    glow_p_tinted = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_p_tinted.paste(tint_p, (0, 0), mask=a_ch)

    # Cyan glow
    glow_c = symbol_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.025))
    r_ch, g_ch, b_ch, a_ch = glow_c.split()
    tint_c = Image.new('RGBA', (size, size), (6, 182, 212, 200))
    glow_c_tinted = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_c_tinted.paste(tint_c, (0, 0), mask=a_ch)

    # Composite all layers
    canvas = Image.alpha_composite(canvas, glow_p_tinted)
    canvas = Image.alpha_composite(canvas, glow_c_tinted)
    canvas = Image.alpha_composite(canvas, symbol_layer)

    return canvas

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Generating ultra-vibrant colorful Luna Music icons...")

    # 1. Circle & Rounded master icons (512x512)
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

        # Standard launcher icon (rounded)
        img_std = rounded_icon.resize((icon_sz, icon_sz), Image.Resampling.LANCZOS)
        img_std.save(os.path.join(folder, "ic_launcher.webp"), "WEBP", quality=95)

        # Round launcher icon (circle)
        img_rnd = circle_icon.resize((icon_sz, icon_sz), Image.Resampling.LANCZOS)
        img_rnd.save(os.path.join(folder, "ic_launcher_round.webp"), "WEBP", quality=95)

        # Foreground for adaptive icon (scaled to fit nicely in 108dp keyline)
        fg_art = create_vibrant_luna_art(size=fg_sz, style="transparent")
        fg_art.save(os.path.join(folder, "ic_launcher_foreground.webp"), "WEBP", quality=95)
        fg_art.save(os.path.join(folder, "ic_launcher_round_foreground.webp"), "WEBP", quality=95)

    print("✓ Saved all vibrant Android mipmap webp icons")

    # 3. Fastlane Store Assets
    store_dir = os.path.join(root, "fastlane", "metadata", "android", "en-US", "images")
    os.makedirs(store_dir, exist_ok=True)
    circle_icon.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(store_dir, "icon.png"), "PNG")

    # Feature Graphic (1024x500)
    fg_w, fg_h = 1024, 500
    feat_img = Image.new('RGBA', (fg_w, fg_h), (18, 8, 38, 255))
    f_draw = ImageDraw.Draw(feat_img)
    # Sweeping rich cosmic nebula background
    for x in range(fg_w):
        t = x / fg_w
        r = int(24 + (52 - 24) * math.sin(t * math.pi))
        g = int(10 + (28 - 10) * math.sin(t * math.pi))
        b = int(48 + (96 - 48) * math.sin(t * math.pi))
        f_draw.line([(x, 0), (x, fg_h)], fill=(r, g, b, 255))

    # Big vibrant logo on left
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

    print("\n🎉 All colorful Luna Music icons created successfully!")

if __name__ == "__main__":
    main()
