import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def create_brand_new_luna_art(size=1024, style="circle"):
    """
    Brand New Modern Icon Design for Luna Music:
    "The Neon Pulsar Luna — Celestial Sound Resonance"
    Features:
      - Deep obsidian cosmic background with luminous starlight resonance rings
      - Fluid modern harmonic crescent ribbon sculpted with Sunset Coral -> Electric Magenta -> Neon Cyan gradient
      - Glowing acoustic core / sound pearl with iridescent starlight reflection
      - Sleek stylized music note integrated with harmonic soundwave resonance rings
      - Brilliant 4-point celestial pulsar stars
      - Guaranteed safe-zone margins (all elements within radius <= 0.255 * size)
    """
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    center = size / 2.0
    
    # 1. Background
    bg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    radius = size * 0.46
    
    if style in ("circle", "rounded", "full_bg"):
        max_r = int(radius if style != "full_bg" else size * 0.72)
        # Deep royal cosmic gradient
        for r in range(max_r, 0, -2):
            ratio = r / max_r
            # Center: deep rich royal indigo (38, 16, 74) -> Edge: velvet obsidian (10, 4, 22)
            red = int(38 + (10 - 38) * (ratio ** 1.1))
            green = int(16 + (4 - 16) * (ratio ** 1.1))
            blue = int(74 + (22 - 74) * (ratio ** 1.1))
            bg_draw.ellipse([center - r, center - r, center + r, center + r], fill=(red, green, blue, 255))
            
        # Concentric sound resonance rings in the cosmos
        for r_ring in [size * 0.38, size * 0.32, size * 0.26]:
            bg_draw.ellipse([center - r_ring, center - r_ring, center + r_ring, center + r_ring], 
                            outline=(168, 85, 247, 30), width=int(size * 0.005))
            
        # Subtle nebula glow clouds
        nebula = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        neb_draw = ImageDraw.Draw(nebula)
        neb_draw.ellipse([center - size*0.05, center - size*0.35, center + size*0.40, center + size*0.10], fill=(236, 72, 153, 90))
        neb_draw.ellipse([center - size*0.40, center - size*0.10, center + size*0.10, center + size*0.40], fill=(6, 182, 212, 90))
        nebula = nebula.filter(ImageFilter.GaussianBlur(radius=size * 0.12))
        bg = Image.alpha_composite(bg, nebula)
            
        if style == "circle":
            mask = Image.new('L', (size, size), 0)
            ImageDraw.Draw(mask).ellipse([center - radius, center - radius, center + radius, center + radius], fill=255)
            bg.putalpha(mask)
        elif style == "rounded":
            mask = Image.new('L', (size, size), 0)
            ImageDraw.Draw(mask).rounded_rectangle([center - radius, center - radius, center + radius, center + radius], radius=int(size*0.22), fill=255)
            bg.putalpha(mask)
            
    canvas = Image.alpha_composite(canvas, bg)

    # 2. Modern Harmonic Crescent Ribbon
    # Outer radius = size * 0.225, inner cutout radius = size * 0.180
    m_cx = center - size * 0.02
    m_cy = center
    m_r = size * 0.225

    # Multi-stop sunset-coral -> fuchsia -> electric violet -> cyan gradient
    gradient_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient_img)
    y_min = int(m_cy - m_r)
    y_max = int(m_cy + m_r)
    height_span = max(1, y_max - y_min)
    
    for y in range(y_min, y_max + 1):
        t = (y - y_min) / height_span
        if t < 0.28:
            # Radiant Sunset Flame Coral (#FF5E3A -> #FF007F)
            st = t / 0.28
            r = 255
            g = int(94 * (1 - st) + 0 * st)
            b = int(58 * (1 - st) + 127 * st)
        elif t < 0.62:
            # Electric Orchid / Magenta (#FF007F -> #8B5CF6)
            st = (t - 0.28) / 0.34
            r = int(255 * (1 - st) + 139 * st)
            g = int(0 * (1 - st) + 92 * st)
            b = int(127 * (1 - st) + 246 * st)
        else:
            # Electric Violet to Neon Cyan & Turquoise (#8B5CF6 -> #00F2FE)
            st = (t - 0.62) / 0.38
            r = int(139 * (1 - st) + 0 * st)
            g = int(92 * (1 - st) + 242 * st)
            b = int(246 * (1 - st) + 254 * st)
        g_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Mask for the crescent ribbon
    moon_mask = Image.new('L', (size, size), 0)
    mm_draw = ImageDraw.Draw(moon_mask)
    mm_draw.ellipse([m_cx - m_r, m_cy - m_r, m_cx + m_r, m_cy + m_r], fill=255)
    
    cutout_cx = m_cx + size * 0.082
    cutout_cy = m_cy - size * 0.005
    cutout_r = size * 0.182
    mm_draw.ellipse([cutout_cx - cutout_r, cutout_cy - cutout_r, cutout_cx + cutout_r, cutout_cy + cutout_r], fill=0)
    
    moon_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    moon_layer.paste(gradient_img, (0, 0), mask=moon_mask)

    # 3. Luminous Musical Note & Sound Resonance
    note_mask = Image.new('L', (size, size), 0)
    nm_draw = ImageDraw.Draw(note_mask)
    
    # Acoustic pearl note head
    nh_x = center + size * 0.035
    nh_y = center + size * 0.075
    nh_rx = size * 0.078
    nh_ry = size * 0.055
    
    nh_temp = Image.new('L', (size, size), 0)
    t_draw = ImageDraw.Draw(nh_temp)
    t_draw.ellipse([nh_x - nh_rx, nh_y - nh_ry, nh_x + nh_rx, nh_y + nh_ry], fill=255)
    nh_rot = nh_temp.rotate(-24, resample=Image.Resampling.BICUBIC, center=(int(nh_x), int(nh_y)))
    note_mask = ImageChops.lighter(note_mask, nh_rot)
    
    # Sleek Note Stem
    stem_w = int(size * 0.022)
    stem_x = int(nh_x + nh_rx * 0.65)
    stem_top_y = int(center - size * 0.155)
    stem_bot_y = int(nh_y)
    nm_draw.rectangle([stem_x - stem_w//2, stem_top_y, stem_x + stem_w//2, stem_bot_y], fill=255)
    
    # Dynamic flag curve
    flag_w = int(stem_w * 1.05)
    nm_draw.arc([stem_x - stem_w, stem_top_y, stem_x + int(size * 0.125), stem_top_y + int(size * 0.17)], 
                start=260, end=40, fill=255, width=flag_w)
    
    # Note Gradient: glowing starlight gold (#FFFBEB) down to vivid azure (#38BDF8)
    note_grad = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ng_draw = ImageDraw.Draw(note_grad)
    for y in range(int(stem_top_y), int(nh_y + nh_ry) + 1):
        t = (y - stem_top_y) / max(1, (nh_y + nh_ry - stem_top_y))
        r = int(255 * (1 - t) + 45 * t)
        g = int(250 * (1 - t) + 195 * t)
        b = int(230 * (1 - t) + 250 * t)
        ng_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
        
    note_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    note_layer.paste(note_grad, (0, 0), mask=note_mask)

    # 4. Soundwave Equalizer Arcs (Symbolizing active music streaming)
    waves_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    w_draw = ImageDraw.Draw(waves_layer)
    wave_center_x = stem_x + int(size * 0.04)
    wave_center_y = int(center - size * 0.03)
    
    # 3 radiant soundwave pulses
    for idx, (rw, alpha, color) in enumerate([
        (int(size * 0.045), 230, (0, 242, 254)),
        (int(size * 0.075), 180, (217, 70, 239)),
        (int(size * 0.105), 130, (254, 240, 138)),
    ]):
        bbox = [wave_center_x - rw, wave_center_y - rw, wave_center_x + rw, wave_center_y + rw]
        w_draw.arc(bbox, start=-35, end=35, fill=(color[0], color[1], color[2], alpha), width=int(size * 0.012))

    # 5. Brilliant 4-Point Celestial Pulsar Stars
    def draw_pulsar_star(draw_obj, cx, cy, arm_len, width, color):
        pts_h = [(cx - arm_len, cy), (cx + arm_len, cy)]
        pts_v = [(cx, cy - arm_len), (cx, cy + arm_len)]
        draw_obj.line(pts_h, fill=color, width=width)
        draw_obj.line(pts_v, fill=color, width=width)
        r_d = arm_len * 0.32
        draw_obj.polygon([(cx, cy - r_d), (cx + r_d, cy), (cx, cy + r_d), (cx - r_d, cy)], fill=color)

    stars_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stars_layer)
    
    # Golden Pulsar Star at upper right
    draw_pulsar_star(s_draw, center + size * 0.155, center - size * 0.165, size * 0.038, int(size * 0.009), (254, 240, 138, 255))
    # Cyan Pulsar Star near top crescent tip
    draw_pulsar_star(s_draw, center + size * 0.012, center - size * 0.205, size * 0.026, int(size * 0.007), (103, 232, 249, 255))
    # Magenta Accent Star near bottom crescent
    draw_pulsar_star(s_draw, center - size * 0.16, center + size * 0.175, size * 0.028, int(size * 0.007), (244, 114, 182, 255))

    # Combine all elements
    symbol_layer = Image.alpha_composite(moon_layer, note_layer)
    symbol_layer = Image.alpha_composite(symbol_layer, waves_layer)
    symbol_layer = Image.alpha_composite(symbol_layer, stars_layer)

    # 6. Radiant Neon Bloom (Dual-pass glow: Magenta + Cyan)
    glow_p = symbol_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.035))
    _, _, _, a_p = glow_p.split()
    tint_p = Image.new('RGBA', (size, size), (236, 72, 153, 190))
    glow_p_tinted = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_p_tinted.paste(tint_p, (0, 0), mask=a_p)

    glow_c = symbol_layer.filter(ImageFilter.GaussianBlur(radius=size * 0.016))
    _, _, _, a_c = glow_c.split()
    tint_c = Image.new('RGBA', (size, size), (0, 242, 254, 190))
    glow_c_tinted = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_c_tinted.paste(tint_c, (0, 0), mask=a_c)

    # Final composite
    canvas = Image.alpha_composite(canvas, glow_p_tinted)
    canvas = Image.alpha_composite(canvas, glow_c_tinted)
    canvas = Image.alpha_composite(canvas, symbol_layer)

    return canvas

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("Generating brand-new modern Luna Music icons (safe-zone optimized)...")

    # 1. Master icons (512x512)
    circle_icon = create_brand_new_luna_art(size=512, style="circle")
    rounded_icon = create_brand_new_luna_art(size=512, style="rounded")
    transparent_icon = create_brand_new_luna_art(size=512, style="transparent")

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

        # Legacy launcher icon (rounded)
        img_std = rounded_icon.resize((icon_sz, icon_sz), Image.Resampling.LANCZOS)
        img_std.save(os.path.join(folder, "ic_launcher.webp"), "WEBP", quality=95)

        # Legacy round launcher icon (circle)
        img_rnd = circle_icon.resize((icon_sz, icon_sz), Image.Resampling.LANCZOS)
        img_rnd.save(os.path.join(folder, "ic_launcher_round.webp"), "WEBP", quality=95)

        # Adaptive icon foreground layer (with safe-zone padding)
        fg_art = create_brand_new_luna_art(size=fg_sz, style="transparent")
        fg_art.save(os.path.join(folder, "ic_launcher_foreground.webp"), "WEBP", quality=95)
        fg_art.save(os.path.join(folder, "ic_launcher_round_foreground.webp"), "WEBP", quality=95)

    print("✓ Saved all brand-new Android mipmap webp icons")

    # 3. Fastlane Store Assets
    store_dir = os.path.join(root, "fastlane", "metadata", "android", "en-US", "images")
    os.makedirs(store_dir, exist_ok=True)
    circle_icon.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(store_dir, "icon.png"), "PNG")

    # Feature Graphic (1024x500)
    fg_w, fg_h = 1024, 500
    feat_img = Image.new('RGBA', (fg_w, fg_h), (12, 6, 26, 255))
    f_draw = ImageDraw.Draw(feat_img)
    for x in range(fg_w):
        t = x / fg_w
        r = int(18 + (46 - 18) * math.sin(t * math.pi))
        g = int(8 + (22 - 8) * math.sin(t * math.pi))
        b = int(36 + (88 - 36) * math.sin(t * math.pi))
        f_draw.line([(x, 0), (x, fg_h)], fill=(r, g, b, 255))

    logo_art = create_brand_new_luna_art(size=360, style="circle")
    feat_img.paste(logo_art, (70, 70), mask=logo_art)
    feat_img.save(os.path.join(store_dir, "featureGraphic.png"), "PNG")
    print("✓ Saved Fastlane store graphics")

    # 4. Website Assets
    public_assets = os.path.join(root, "public", "assets")
    if os.path.exists(public_assets):
        circle_icon.save(os.path.join(public_assets, "logo.png"), "PNG")
        feat_img.save(os.path.join(public_assets, "banner.png"), "PNG")
        print("✓ Updated public website assets")

    print("\n🎉 Brand-new Luna Music icons successfully created!")

if __name__ == "__main__":
    main()
