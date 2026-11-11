import json
import subprocess
import os

def create_rough_audio():
    # Slices from take2_raw.wav based on Whisper timings
    # We will pick the best portions and stitch them with small crossfades
    segments = [
        # (start, end, label)
        (0.8, 6.8, "hook"),             # "Es gab einen einzigen Tag..."
        (14.0, 33.5, "dunkirk_pocket"),  # "Dünkirchen, Mai 1940..."
        (34.0, 42.0, "timeline_x"),     # "Doch was passiert in Zeitlinie X..."
        (49.0, 69.5, "bef_crushed"),     # "Innerhalb von 72 Stunden..."
        (70.0, 78.5, "london_crisis"),   # "In London bricht die Regierung zusammen..."
        (84.0, 88.0, "capitulation"),    # "Kapitulation oder demütigender Frieden..."
        (88.0, 95.0, "west_exit"),       # "Großbritannien scheidet 1940 aus dem Krieg aus..."
        (99.0, 104.0, "east_invasion"),  # "Und als 1941 der Angriff auf die Sowjetunion beginnt..."
        (108.0, 118.5, "axis_power"),    # "Die gesamte industrielle und militärische Macht..."
        (128.0, 134.5, "cta"),           # "Hätte England trotzdem weitergekämpft?..."
    ]

    in_wav = "episodes/ep01_dunkirk_1940/assets/take2_raw.wav"
    out_dir = "episodes/ep01_dunkirk_1940/assets/slices"
    os.makedirs(out_dir, exist_ok=True)

    concat_list_path = os.path.join(out_dir, "concat.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for idx, (start, end, label) in enumerate(segments):
            dur = end - start
            filename = f"part_{idx:02d}_{label}.wav"
            part_path = os.path.join(out_dir, filename)
            cmd = [
                "ffmpeg", "-y", "-ss", str(start), "-t", str(dur),
                "-i", in_wav, "-c", "copy", part_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            f.write(f"file '{filename}'\n")

    # Concat using absolute paths
    concat_list_path = os.path.abspath(concat_list_path)
    rough_audio = os.path.abspath("episodes/ep01_dunkirk_1940/assets/rough_voiceover.wav")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_path, "-c", "copy", rough_audio
    ])

    print("Rough voiceover assembled at:", rough_audio)

if __name__ == "__main__":
    create_rough_audio()
