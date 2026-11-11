import os
from render_cinematic_scenes import ken_burns_video

scenes_dir = "episodes/ep01_dunkirk_1940/assets/scenes"
clips_dir = "episodes/ep01_dunkirk_1940/assets/clips"

print("Rendering Scene 01 (Beach Ken Burns)...")
ken_burns_video(
    os.path.join(scenes_dir, "scene_01_beach.jpg"),
    os.path.join(clips_dir, "cine_01_beach.mp4"),
    duration_sec=6.0,
    zoom_factor=1.15,
    pan_direction="zoom_in"
)

print("Rendering Scene 02 (Panzers Ken Burns)...")
ken_burns_video(
    os.path.join(scenes_dir, "scene_02_panzers.jpg"),
    os.path.join(clips_dir, "cine_02_panzers.mp4"),
    duration_sec=7.0,
    zoom_factor=1.12,
    pan_direction="zoom_in"
)

print("Rendering Scene 03 (London Cabinet Ken Burns)...")
ken_burns_video(
    os.path.join(scenes_dir, "scene_03_london.jpg"),
    os.path.join(clips_dir, "cine_03_london.mp4"),
    duration_sec=8.0,
    zoom_factor=1.14,
    pan_direction="pan_down"
)

print("Rendering Scene 04 (Eastern Front Ken Burns)...")
ken_burns_video(
    os.path.join(scenes_dir, "scene_04_east.jpg"),
    os.path.join(clips_dir, "cine_04_east.mp4"),
    duration_sec=8.0,
    zoom_factor=1.15,
    pan_direction="zoom_in"
)

print("All cinematic clips rendered successfully!")
