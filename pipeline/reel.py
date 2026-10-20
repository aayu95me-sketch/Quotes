"""Build a static-image Reel (1080x1920 mp4) from one image and an optional audio file.

Usage: python pipeline/reel.py slide.png out.mp4 [--audio track.mp3] [--seconds 9]

The image is placed on a 1080x1920 canvas (blurred fill) so no motion is needed.
Audio must be commercially cleared or original. Trending audio is normally
attached at upload time through the Instagram app/API, not baked into the file.
"""
import argparse
import subprocess


def build(image, out, audio=None, seconds=9):
    vf = (
        "split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=30:5[bg];[b]scale=1080:-2[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p"
    )
    cmd = ["ffmpeg", "-y", "-loop", "1", "-t", str(seconds), "-i", image]
    if audio:
        cmd += ["-i", audio, "-shortest", "-c:a", "aac"]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-c:a", "aac", "-t", str(seconds)]
    cmd += ["-vf", vf, "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True, capture_output=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("out")
    ap.add_argument("--audio")
    ap.add_argument("--seconds", type=int, default=9)
    a = ap.parse_args()
    build(a.image, a.out, a.audio, a.seconds)
    print(a.out)
