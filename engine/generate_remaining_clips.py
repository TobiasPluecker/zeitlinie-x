"""
Zeitlinie X - Generate Remaining Video Clips (Clips 05 - 08)
"""

import os
import math
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw

OUTPUT_DIR = "episodes/ep01_dunkirk_1940/assets/clips"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BG_COLOR = "#0B1120"
LAND_COLOR = "#1E293B"
WATER_COLOR = "#0F172A"
AXIS_RED = "#EF4444"
ALLIED_BLUE = "#38BDF8"
ACCENT_GOLD = "#F59E0B"
TEXT_WHITE = "#F8FAFC"

W, H = 720, 1280
FPS = 24

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

def render_london_crisis(output_path, duration_sec=12.0):
    """Clip 5: London Crisis / Government Collapse"""
    print(f"Rendering London Crisis ({duration_sec}s)...")
    total_frames = int(duration_sec * FPS)
    frames = []

    for f in range(total_frames):
        t = f / float(total_frames)
        img = Image.new("RGB", (W, H), color=(15, 23, 42))
        draw = ImageDraw.Draw(img)

        # Tactical Grid
        for y in range(0, H, 100):
            draw.line([(0, y), (W, y)], fill=(25, 35, 58), width=1)
        for x in range(0, W, 100):
            draw.line([(x, 0), (x, H)], fill=(25, 35, 58), width=1)

        # Breaking Dossier Box
        draw.rectangle([(60, 240), (W - 60, H - 280)], fill=(11, 17, 32), outline=(239, 68, 68), width=3)
        draw.rectangle([(60, 240), (W - 60, 310)], fill=(239, 68, 68))
        draw.text((W//2, 275), "KABINETTSKRISE IN LONDON", fill=(255, 255, 255), anchor="mm")

        # Content
        draw.text((W//2, 400), "MAI / JUNI 1940", fill=(148, 163, 184), anchor="mm")
        draw.text((W//2, 480), "CHURCHILL VERLIERT DEN RÜCKHALT", fill=(248, 250, 252), anchor="mm")
        draw.text((W//2, 540), "Die gesamte Berufsarmee verloren.", fill=(203, 213, 225), anchor="mm")

        # Choice Box: Surrender vs Peace
        draw.rectangle([(100, 640), (W - 100, 720)], fill=(30, 41, 59), outline=(245, 158, 11), width=2)
        draw.text((W//2, 680), "OPTION: WAFFENSTILLSTAND MIT BERLIN", fill=(245, 158, 11), anchor="mm")

        draw.rectangle([(100, 750), (W - 100, 830)], fill=(30, 41, 59), outline=(100, 116, 139), width=1)
        draw.text((W//2, 790), "ENGLAND SCHEIDET AUS DEM KRIEG AUS", fill=(203, 213, 225), anchor="mm")

        frames.append(np.array(img))

    save_frames_to_mp4(output_path, frames, fps=FPS)
    print(f"London Crisis saved to {output_path}")

def render_europe_east(output_path, duration_sec=12.0):
    """Clip 6: Map of Europe - Axis eye on the East"""
    print(f"Rendering Europe East Strategic Map ({duration_sec}s)...")
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

        # Western Europe (Pacified in red tint)
        west_poly = patches.Polygon(xy=[(1, 4), (5, 4), (5, 13), (1, 13)],
                                    facecolor="#7F1D1D", edgecolor="#EF4444", linewidth=2, alpha=0.5)
        ax.add_patch(west_poly)
        ax.text(3.0, 8.5, "WESTEUROPA\nBEFRIEDET\n(1940)", color="#FCA5A5", fontsize=11, fontweight='bold', ha='center')

        # Massive Arrows Heading East towards USSR
        adv = min(t * 1.5, 1.0)
        start_x, start_y = 5.0, 9.0
        target_x = start_x + (4.0 * adv)
        ax.annotate('', xy=(target_x, start_y), xytext=(start_x, start_y),
                    arrowprops=dict(facecolor=AXIS_RED, edgecolor="#FFFFFF", width=8, headwidth=20))

        ax.text(8.5, 11.0, "SOWJETUNION", color="#94A3B8", fontsize=13, fontweight='bold', ha='center')
        ax.plot(8.5, 9.0, marker='*', markersize=14, color=ACCENT_GOLD)
        ax.text(8.5, 8.2, "MOSKAU", color=ACCENT_GOLD, fontsize=12, fontweight='bold', ha='center')

        # Status text
        ax.text(5.0, 16.5, "KEINE ZWEITE FRONT IM WESTEN", color=TEXT_WHITE,
                fontsize=12, fontweight='black', ha='center',
                bbox=dict(facecolor=BG_COLOR, edgecolor=ACCENT_GOLD, boxstyle='round,pad=0.5'))

        ax.text(5.0, 14.5, "Volle Wehrmachtskonzentration auf den Osten", color="#F8FAFC", fontsize=10, ha='center')
        ax.text(5.0, 0.8, "ZEITLINIE X | @zeitlinie_x", color="#475569", fontsize=9, ha='center', fontweight='bold')

        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        frames.append(rgba[:, :, :3])
        plt.close(fig)

    save_frames_to_mp4(output_path, frames, fps=FPS)
    print(f"Europe East Map saved to {output_path}")

def render_cta_clip(output_path, duration_sec=8.0):
    """Clip 8: Call to Action & Zeitlinie X Outro"""
    print(f"Rendering Outro / CTA Clip ({duration_sec}s)...")
    total_frames = int(duration_sec * FPS)
    frames = []

    for f in range(total_frames):
        t = f / float(total_frames)
        img = Image.new("RGB", (W, H), color=(11, 17, 32))
        draw = ImageDraw.Draw(img)

        # Pulsing circle logo
        pulse = (math.sin(t * math.pi * 4) + 1) * 0.5
        r = 140 + int(pulse * 20)
        draw.ellipse([(W//2 - r, 450 - r), (W//2 + r, 450 + r)], outline=(245, 158, 11), width=4)
        draw.text((W//2, 450), "X", fill=(245, 158, 11), anchor="mm")

        draw.text((W//2, 630), "ZEITLINIE X", fill=(248, 250, 252), anchor="mm")
        draw.text((W//2, 675), "Geschichte neu gedacht.", fill=(148, 163, 184), anchor="mm")

        # Question sticker for comment engagement
        draw.rectangle([(80, 780), (W - 80, 940)], fill=(30, 41, 59), outline=(56, 189, 248), width=3)
        draw.text((W//2, 825), "HÄTTE ENGLAND TROTZDEM", fill=(255, 255, 255), anchor="mm")
        draw.text((W//2, 865), "WEITERGEKÄMPFT?", fill=(56, 189, 248), anchor="mm")
        draw.text((W//2, 905), "💬 Schreib deine Theorie in die Kommentare", fill=(203, 213, 225), anchor="mm")

        # Follow button reminder
        draw.rectangle([(W//2 - 160, 1020), (W//2 + 160, 1080)], fill=(239, 68, 68))
        draw.text((W//2, 1050), "+ FOLGEN FÜR TEIL 2", fill=(255, 255, 255), anchor="mm")

        frames.append(np.array(img))

    save_frames_to_mp4(output_path, frames, fps=FPS)
    print(f"CTA Clip saved to {output_path}")

def render_remaining():
    render_london_crisis(os.path.join(OUTPUT_DIR, "clip_05_london.mp4"), duration_sec=12.0)
    render_europe_east(os.path.join(OUTPUT_DIR, "clip_06_europe_east.mp4"), duration_sec=12.0)
    render_cta_clip(os.path.join(OUTPUT_DIR, "clip_07_cta.mp4"), duration_sec=8.0)
    print("All remaining clips successfully generated!")

if __name__ == "__main__":
    render_remaining()
