"""
Zeitlinie X - Cinematic Image-to-Video Engine (Ken Burns + Camera Movement)
Transforms photorealistic still images into dynamic 9:16 movie shots.
"""

import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageEnhance

W, H = 720, 1280
FPS = 24

def ken_burns_video(image_path, output_path, duration_sec=5.0, zoom_factor=1.12, pan_direction="zoom_in"):
    """
    Renders a photorealistic still image with a cinematic slow zoom/pan (Ken Burns effect).
    """
    if not os.path.exists(image_path):
        print(f"Error: {image_path} does not exist!")
        return

    img = Image.open(image_path).convert("RGB")
    orig_w, orig_h = img.size

    # Fit image to 9:16 canvas by cropping or scaling
    scale = max(W / orig_w, H / orig_h)
    base_w = int(orig_w * scale)
    base_h = int(orig_h * scale)
    img_scaled = img.resize((base_w, base_h), Image.Resampling.LANCZOS)

    # Crop to center
    left = (base_w - W) // 2
    top = (base_h - H) // 2
    base_frame = img_scaled.crop((left, top, left + W, top + H))

    total_frames = int(duration_sec * FPS)
    frames = []

    for f in range(total_frames):
        t = f / float(total_frames)

        # Smooth easing (ease-in-out)
        ease = 0.5 - 0.5 * math.cos(t * math.pi)

        if pan_direction == "zoom_in":
            current_zoom = 1.0 + (zoom_factor - 1.0) * ease
            zw = int(W * current_zoom)
            zh = int(H * current_zoom)
            z_img = base_frame.resize((zw, zh), Image.Resampling.BILINEAR)
            cx = (zw - W) // 2
            cy = (zh - H) // 2
            frame = z_img.crop((cx, cy, cx + W, cy + H))
        elif pan_direction == "pan_down":
            current_zoom = 1.08
            zw = int(W * current_zoom)
            zh = int(H * current_zoom)
            z_img = base_frame.resize((zw, zh), Image.Resampling.BILINEAR)
            cx = (zw - W) // 2
            max_y = zh - H
            cy = int(max_y * ease)
            frame = z_img.crop((cx, cy, cx + W, cy + H))
        else:
            frame = base_frame

        # Subtle film grain / contrast adjustment
        enhancer = ImageEnhance.Contrast(frame)
        frame_contrasted = enhancer.enhance(1.05)

        frames.append(np.array(frame_contrasted))

    # Pipe to ffmpeg
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "18",
        output_path
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for f in frames:
        proc.stdin.write(f.tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"Cinematic clip rendered: {output_path}")

if __name__ == "__main__":
    pass
