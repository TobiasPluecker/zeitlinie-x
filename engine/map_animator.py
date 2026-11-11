"""
Zeitlinie X - Dynamic Map Animation Engine
Renders high-contrast, tactical vertical maps (9:16) for TikTok / Reels.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
from PIL import Image

# Design Palette
BG_COLOR = "#0B1120"       # Deep dark slate
LAND_COLOR = "#1E293B"     # Dark landmass
WATER_COLOR = "#0F172A"    # Dark water
AXIS_RED = "#EF4444"       # Wehrmacht offensive arrows
ALLIED_BLUE = "#38BDF8"    # British / French pocket
ACCENT_GOLD = "#F59E0B"    # Timeline X highlights
TEXT_COLOR = "#F8FAFC"     # Clean typography

def generate_dunkirk_pocket_animation(output_path="episodes/ep01_dunkirk_1940/assets/dunkirk_map.gif", fps=15, duration_sec=4):
    """
    Renders an animated vertical tactical map of the Dunkirk encirclement.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    total_frames = fps * duration_sec
    frames = []

    # 9:16 vertical figure size (e.g. 5.4 x 9.6 inches @ 100 dpi = 540x960 px preview)
    fig_w, fig_h = 5.4, 9.6
    dpi = 100

    print(f"Rendering {total_frames} frames for {output_path}...")

    for frame_idx in range(total_frames):
        progress = frame_idx / float(total_frames - 1)  # 0.0 to 1.0

        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi, facecolor=BG_COLOR)
        ax.set_facecolor(WATER_COLOR)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 17.77)  # 9:16 ratio
        ax.axis('off')

        # 1. Simplified Coastal Landmass (Northern France / Flanders)
        # Land polygon
        land_x = [0, 10, 10, 4.5, 3.2, 0]
        land_y = [0, 0, 11, 12.5, 11.8, 8]
        land_poly = patches.Polygon(xy=list(zip(land_x, land_y)), facecolor=LAND_COLOR, edgecolor="#334155", linewidth=2)
        ax.add_patch(land_poly)

        # 2. English Coastline (top left)
        england_x = [0, 5, 2.5, 0]
        england_y = [17.77, 17.77, 14.5, 13.5]
        england_poly = patches.Polygon(xy=list(zip(england_x, england_y)), facecolor=LAND_COLOR, edgecolor="#334155", linewidth=2)
        ax.add_patch(england_poly)

        # Labels for Geography
        ax.text(1.5, 15.5, "ENGLAND", color="#64748B", fontsize=12, fontweight='bold', alpha=0.7)
        ax.text(1.2, 13.0, "Ärmelkanal", color="#475569", fontsize=10, style='italic')
        ax.text(6.5, 5.0, "FRANKREICH", color="#475569", fontsize=13, fontweight='bold', alpha=0.5)

        # Dunkirk Port Marker (approx. x=4.2, y=12.2)
        dunkirk_x, dunkirk_y = 4.2, 12.2
        ax.plot(dunkirk_x, dunkirk_y, marker='o', markersize=8, color=ACCENT_GOLD)
        ax.text(dunkirk_x + 0.3, dunkirk_y + 0.3, "DÜNKIRCHEN", color=ACCENT_GOLD, fontsize=12, fontweight='bold')

        # 3. Allied Pocket (BEF & French Troops)
        # Contracting pocket as German armor advances
        pocket_scale = 1.0 - 0.4 * progress
        pocket_circle = patches.Circle((4.2, 11.5), radius=1.2 * pocket_scale, 
                                       facecolor=ALLIED_BLUE, alpha=0.25, edgecolor=ALLIED_BLUE, linewidth=2, linestyle='--')
        ax.add_patch(pocket_circle)
        ax.text(4.2, 11.4, "BEF KESSEL\n(330.000)", color=TEXT_COLOR, fontsize=9, fontweight='bold', ha='center', va='center')

        # 4. Advancing German Panzers (Red Arrows)
        # Arrow 1: From South-West (Rommel / Guderian)
        adv1 = min(progress * 1.3, 1.0)
        start1_x, start1_y = 1.5, 7.5
        target1_x = start1_x + (3.3 - start1_x) * adv1
        target1_y = start1_y + (11.0 - start1_y) * adv1
        ax.annotate('', xy=(target1_x, target1_y), xytext=(start1_x, start1_y),
                    arrowprops=dict(facecolor=AXIS_RED, edgecolor=AXIS_RED, width=4, headwidth=12, shrink=0.05))

        # Arrow 2: From East/South-East (Heeresgruppe B)
        adv2 = min(progress * 1.2, 1.0)
        start2_x, start2_y = 7.5, 9.0
        target2_x = start2_x + (5.0 - start2_x) * adv2
        target2_y = start2_y + (11.6 - start2_y) * adv2
        ax.annotate('', xy=(target2_x, target2_y), xytext=(start2_x, start2_y),
                    arrowprops=dict(facecolor=AXIS_RED, edgecolor=AXIS_RED, width=4, headwidth=12, shrink=0.05))

        # Title / Status Overlay at Top
        ax.text(5.0, 17.0, "MAI 1940: DER KESSEL SCHLIESST SICH", color=TEXT_COLOR, 
                fontsize=11, fontweight='black', ha='center', bbox=dict(facecolor=BG_COLOR, edgecolor=ACCENT_GOLD, boxstyle='round,pad=0.4'))

        # Watermark
        ax.text(5.0, 0.8, "ZEITLINIE X | @zeitlinie_x", color="#475569", fontsize=9, ha='center', fontweight='bold')

        # Convert plot to image
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        # Convert RGBA to RGB
        rgb = rgba[:, :, :3]
        frames.append(rgb)
        plt.close(fig)

    imageio.mimsave(output_path, frames, fps=fps)
    print(f"Successfully generated map animation: {output_path}")

if __name__ == "__main__":
    generate_dunkirk_pocket_animation()
