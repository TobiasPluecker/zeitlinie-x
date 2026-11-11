"""
Zeitlinie X - Complete Procedural Video Generation Engine
Renders high-quality 9:16 vertical animation clips for TikTok / Shorts.
"""

import os
import math
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def save_frames_to_mp4(output_path, frames, fps=24):
    h, w, c = frames[0].shape
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{w}x{h}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "18",
        output_path
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for frame in frames:
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()

OUTPUT_DIR = "episodes/ep01_dunkirk_1940/assets/clips"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colors
BG_COLOR = "#0B1120"
LAND_COLOR = "#1E293B"
WATER_COLOR = "#0F172A"
AXIS_RED = "#EF4444"
ALLIED_BLUE = "#38BDF8"
ACCENT_GOLD = "#F59E0B"
TEXT_WHITE = "#F8FAFC"
MUTED_GRAY = "#64748B"

W, H = 720, 1280  # 9:16 vertical resolution (fast & sharp)
FPS = 24

def render_hook_clip(output_path, duration_sec=6.0):
    """Clip 1: High-impact Hook Title Scene"""
    print(f"Rendering Hook Clip ({duration_sec}s)...")
    total_frames = int(duration_sec * FPS)
    frames = []

    for f in range(total_frames):
        t = f / float(total_frames)
        img = Image.new("RGB", (W, H), color=(11, 17, 32))
        draw = ImageDraw.Draw(img)

        # Subtle dark vignette / grid lines
        for y in range(0, H, 80):
            draw.line([(0, y), (W, y)], fill=(18, 28, 48), width=1)
        for x in range(0, W, 80):
            draw.line([(x, 0), (x, H)], fill=(18, 28, 48), width=1)

        # Pulse circle
        pulse = (math.sin(t * math.pi * 4) + 1) * 0.5
        r = 180 + int(pulse * 30)
        draw.ellipse([(W//2 - r, H//2 - 120 - r), (W//2 + r, H//2 - 120 + r)], outline=(239, 68, 68, 80), width=3)

        # Header Badge
        draw.rectangle([(W//2 - 140, 280), (W//2 + 140, 325)], fill=(245, 158, 11), outline=(255, 255, 255))
        draw.text((W//2, 302), "ZEITLINIE X", fill=(11, 17, 32), anchor="mm")

        # Big Hook Text
        scale_zoom = 1.0 + t * 0.08
        draw.text((W//2, 450), "MAI 1940", fill=(148, 163, 184), anchor="mm")
        draw.text((W//2, 530), "DER TAG, AN DEM", fill=(248, 250, 252), anchor="mm")
        draw.text((W//2, 600), "HITLER FAST GEWANN", fill=(239, 68, 68), anchor="mm")

        # Subtitle teaser
        draw.text((W//2, 730), "Über 300.000 Soldaten in der Falle.", fill=(203, 213, 225), anchor="mm")
        draw.text((W//2, 770), "Mit dem Rücken zum Meer.", fill=(245, 158, 11), anchor="mm")

        frames.append(np.array(img))

    save_frames_to_mp4(output_path, frames, fps=FPS)
    print(f"Hook Clip saved to {output_path}")

def render_map_dunkirk_pocket(output_path, duration_sec=19.5):
    """Clip 2: Tactical Pocket Map (Panzers Advance & Halt)"""
    print(f"Rendering Dunkirk Pocket Map ({duration_sec}s)...")
    total_frames = int(duration_sec * FPS)
    frames = []

    dpi = 100
    fig_w, fig_h = W / dpi, H / dpi

    for f in range(total_frames):
        t = f / float(total_frames)

        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi, facecolor=BG_COLOR)
        ax.set_facecolor(WATER_COLOR)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 17.77)
        ax.axis('off')

        # French Coast
        land_poly = patches.Polygon(xy=[(0, 0), (10, 0), (10, 11), (4.5, 12.5), (3.2, 11.8), (0, 8)],
                                    facecolor=LAND_COLOR, edgecolor="#334155", linewidth=2)
        ax.add_patch(land_poly)

        # English Coast
        england_poly = patches.Polygon(xy=[(0, 17.77), (5, 17.77), (2.5, 14.5), (0, 13.5)],
                                       facecolor=LAND_COLOR, edgecolor="#334155", linewidth=2)
        ax.add_patch(england_poly)

        # Geography labels
        ax.text(1.8, 15.8, "GROSSBRITANNIEN", color="#64748B", fontsize=11, fontweight='bold', alpha=0.8)
        ax.text(1.2, 13.2, "Ärmelkanal", color="#475569", fontsize=10, style='italic')
        ax.text(6.8, 4.5, "FRANKREICH", color="#475569", fontsize=13, fontweight='bold', alpha=0.4)

        # Dunkirk marker
        dx, dy = 4.2, 12.2
        ax.plot(dx, dy, marker='o', markersize=9, color=ACCENT_GOLD)
        ax.text(dx + 0.3, dy + 0.35, "DÜNKIRCHEN", color=ACCENT_GOLD, fontsize=12, fontweight='bold')

        # Allied Pocket (330.000 men)
        pocket = patches.Circle((4.2, 11.5), radius=1.1, facecolor=ALLIED_BLUE, alpha=0.25,
                                edgecolor=ALLIED_BLUE, linewidth=2, linestyle='--')
        ax.add_patch(pocket)
        ax.text(4.2, 11.5, "ALLIIERTER KESSEL\n330.000 SOLDATEN", color=TEXT_WHITE, fontsize=9, fontweight='bold', ha='center', va='center')

        # German advance (moves until t=0.5, then HALTS)
        adv = min(t * 2.0, 1.0)
        # Southwest Panzers (Guderian)
        s1x, s1y = 1.0, 7.0
        t1x, t1y = s1x + (3.2 - s1x) * adv, s1y + (10.8 - s1y) * adv
        ax.annotate('', xy=(t1x, t1y), xytext=(s1x, s1y),
                    arrowprops=dict(facecolor=AXIS_RED, edgecolor=AXIS_RED, width=5, headwidth=14, shrink=0.05))

        # Southeast Panzers
        s2x, s2y = 8.0, 8.5
        t2x, t2y = s2x + (5.1 - s2x) * adv, s2y + (11.4 - s2y) * adv
        ax.annotate('', xy=(t2x, t2y), xytext=(s2x, s2y),
                    arrowprops=dict(facecolor=AXIS_RED, edgecolor=AXIS_RED, width=5, headwidth=14, shrink=0.05))

        # If t > 0.5: Show the famous HALT ORDER banner
        if t >= 0.5:
            blink = int((t * 10) % 2 == 0)
            status_box_col = "#DC2626" if blink else "#991B1B"
            ax.text(5.0, 8.2, "HITLERS HALTEBEFEHL:\nPANZER STOPPEN FÜR 48 STUNDEN!", color="#FFFFFF",
                    fontsize=11, fontweight='black', ha='center', va='center',
                    bbox=dict(facecolor=status_box_col, edgecolor="#FFFFFF", boxstyle='round,pad=0.6', linewidth=2))

        # Top banner
        ax.text(5.0, 16.8, "MAI 1940: DER KESSEL VON DÜNKIRCHEN", color=TEXT_WHITE,
                fontsize=11, fontweight='black', ha='center',
                bbox=dict(facecolor=BG_COLOR, edgecolor=ACCENT_GOLD, boxstyle='round,pad=0.4'))

        # Watermark
        ax.text(5.0, 0.8, "ZEITLINIE X | @zeitlinie_x", color="#475569", fontsize=9, ha='center', fontweight='bold')

        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        frames.append(rgba[:, :, :3])
        plt.close(fig)

    save_frames_to_mp4(output_path, frames, fps=FPS)
    print(f"Pocket Map saved to {output_path}")

def render_timeline_split_clip(output_path, duration_sec=8.0):
    """Clip 3: The Divergence / Timeline X Split"""
    print(f"Rendering Timeline Split Clip ({duration_sec}s)...")
    total_frames = int(duration_sec * FPS)
    frames = []

    for f in range(total_frames):
        t = f / float(total_frames)
        img = Image.new("RGB", (W, H), color=(11, 17, 32))
        draw = ImageDraw.Draw(img)

        # Baseline horizontal / vertical timeline
        cy = H // 2
        draw.line([(80, cy), (W//2, cy)], fill=(56, 189, 248), width=6)  # Blue history line
        draw.text((120, cy - 35), "UNSERE ZEITLINIE", fill=(56, 189, 248))
        draw.text((120, cy + 20), "330.000 gerettet", fill=(148, 163, 184))

        # Branching line: Timeline X diverges downwards in fiery red/gold
        prog = min(t * 1.5, 1.0)
        end_x = W//2 + int(prog * (W//2 - 100))
        end_y = cy + int(prog * 250)

        draw.line([(W//2, cy), (end_x, end_y)], fill=(239, 68, 68), width=8)
        draw.ellipse([(W//2 - 10, cy - 10), (W//2 + 10, cy + 10)], fill=(245, 158, 11))

        # Divergence Box
        draw.rectangle([(W//2 - 200, 260), (W//2 + 200, 360)], fill=(15, 23, 42), outline=(245, 158, 11), width=2)
        draw.text((W//2, 290), "DER WENDEPUNKT", fill=(245, 158, 11), anchor="mm")
        draw.text((W//2, 330), "KEIN HALTEBEFEHL", fill=(255, 255, 255), anchor="mm")

        if prog > 0.6:
            draw.text((end_x, end_y + 40), "ZEITLINIE X", fill=(239, 68, 68), anchor="mm")
            draw.text((end_x, end_y + 75), "Totale Vernichtung", fill=(248, 250, 252), anchor="mm")

        frames.append(np.array(img))

    save_frames_to_mp4(output_path, frames, fps=FPS)
    print(f"Timeline Split Clip saved to {output_path}")

def render_crushed_pocket(output_path, duration_sec=21.0):
    """Clip 4: Panzers Breach Perimeter & Destroy Pocket"""
    print(f"Rendering Crushed Pocket Clip ({duration_sec}s)...")
    total_frames = int(duration_sec * FPS)
    frames = []

    dpi = 100
    fig_w, fig_h = W / dpi, H / dpi

    for f in range(total_frames):
        t = f / float(total_frames)

        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi, facecolor=BG_COLOR)
        ax.set_facecolor(WATER_COLOR)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 17.77)
        ax.axis('off')

        # Coast
        land_poly = patches.Polygon(xy=[(0, 0), (10, 0), (10, 11), (4.5, 12.5), (3.2, 11.8), (0, 8)],
                                    facecolor=LAND_COLOR, edgecolor="#334155", linewidth=2)
        ax.add_patch(land_poly)

        # Pocket shrinking and turning red
        radius = max(1.1 - t * 0.9, 0.2)
        col = ALLIED_BLUE if t < 0.3 else AXIS_RED
        pocket = patches.Circle((4.2, 11.5), radius=radius, facecolor=col, alpha=0.35,
                                edgecolor=col, linewidth=3)
        ax.add_patch(pocket)

        # Massive Red Panzers Crushing Inside
        adv = min(t * 1.4, 1.0)
        ax.annotate('', xy=(4.0, 11.8), xytext=(2.0, 9.5),
                    arrowprops=dict(facecolor=AXIS_RED, edgecolor="#FFFFFF", width=6, headwidth=16))
        ax.annotate('', xy=(4.4, 11.8), xytext=(6.5, 10.0),
                    arrowprops=dict(facecolor=AXIS_RED, edgecolor="#FFFFFF", width=6, headwidth=16))

        if t > 0.4:
            ax.text(5.0, 8.5, "KESSEL ÜBERRANNT:\nBEF VERNICHTET & GEFANGEN", color="#FFFFFF",
                    fontsize=12, fontweight='black', ha='center', va='center',
                    bbox=dict(facecolor="#991B1B", edgecolor="#EF4444", boxstyle='round,pad=0.6', linewidth=2))

        ax.text(5.0, 16.8, "ZEITLINIE X: DER STURM AUF DÜNKIRCHEN", color=TEXT_WHITE,
                fontsize=11, fontweight='black', ha='center',
                bbox=dict(facecolor=BG_COLOR, edgecolor=AXIS_RED, boxstyle='round,pad=0.4'))

        ax.text(5.0, 0.8, "ZEITLINIE X | @zeitlinie_x", color="#475569", fontsize=9, ha='center', fontweight='bold')

        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        frames.append(rgba[:, :, :3])
        plt.close(fig)

    save_frames_to_mp4(output_path, frames, fps=FPS)
    print(f"Crushed Pocket Clip saved to {output_path}")

def render_all():
    render_hook_clip(os.path.join(OUTPUT_DIR, "clip_01_hook.mp4"), duration_sec=6.0)
    render_map_dunkirk_pocket(os.path.join(OUTPUT_DIR, "clip_02_pocket.mp4"), duration_sec=19.5)
    render_timeline_split_clip(os.path.join(OUTPUT_DIR, "clip_03_split.mp4"), duration_sec=8.0)
    render_crushed_pocket(os.path.join(OUTPUT_DIR, "clip_04_crushed.mp4"), duration_sec=21.0)
    print("All core animation clips rendered!")

if __name__ == "__main__":
    render_all()
