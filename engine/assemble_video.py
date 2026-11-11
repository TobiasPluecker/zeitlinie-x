import subprocess
import os

clips = [
    "clip_01_hook.mp4",
    "clip_02_pocket.mp4",
    "clip_03_split.mp4",
    "clip_04_crushed.mp4",
    "clip_05_london.mp4",
    "clip_06_europe_east.mp4",
    "clip_07_cta.mp4"
]

clips_dir = os.path.abspath("episodes/ep01_dunkirk_1940/assets/clips")
concat_txt = os.path.join(clips_dir, "video_concat.txt")

with open(concat_txt, "w", encoding="utf-8") as f:
    for c in clips:
        f.write(f"file '{c}'\n")

audio_file = os.path.abspath("episodes/ep01_dunkirk_1940/assets/rough_voiceover.wav")
output_video = os.path.abspath("episodes/ep01_dunkirk_1940/ep01_preview_video.mp4")

# Concat video and merge audio
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_txt,
    "-i", audio_file,
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    output_video
]

print("Stitching preview video...")
subprocess.run(cmd, cwd=clips_dir)
print("Preview video created at:", output_video)
