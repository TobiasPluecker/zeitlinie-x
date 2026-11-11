import subprocess
import os

clips = [
    "cine_01_beach.mp4",        # Photorealistic beach shot (6s)
    "clip_02_pocket.mp4",       # Tactical Dunkirk pocket map
    "cine_02_panzers.mp4",      # Photorealistic tanks idling in mud (7s)
    "clip_03_split.mp4",        # Timeline X divergence effect
    "clip_04_crushed.mp4",      # Panzers assault and crush the pocket
    "cine_03_london.mp4",       # Photorealistic Churchill / Cabinet room (8s)
    "clip_05_london.mp4",       # Tactical London dossier
    "clip_06_europe_east.mp4",  # Strategic map of Europe (March East)
    "cine_04_east.mp4",         # Photorealistic snowstorm armored assault (8s)
    "clip_07_cta.mp4"           # Outro & Call to Action
]

clips_dir = os.path.abspath("episodes/ep01_dunkirk_1940/assets/clips")
concat_txt = os.path.join(clips_dir, "cine_concat.txt")

with open(concat_txt, "w", encoding="utf-8") as f:
    for c in clips:
        f.write(f"file '{c}'\n")

audio_file = os.path.abspath("episodes/ep01_dunkirk_1940/assets/rough_voiceover.wav")
output_video = os.path.abspath("episodes/ep01_dunkirk_1940/ep01_cinematic_movie_cut.mp4")

cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_txt,
    "-i", audio_file,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    output_video
]

print("Stitching cinematic movie cut...")
subprocess.run(cmd, cwd=clips_dir)
print("Cinematic video ready at:", output_video)
