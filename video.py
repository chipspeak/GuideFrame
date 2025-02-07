import subprocess

'''
Starts recording the screen with FFmpeg using ffmpeg-python wrapper
We still need the process object in order to pass 'q' in order to end the recording
The wrapper doesn't have a stop() command or an equivalent hence this combo of both versions
'''

def start_ffmpeg_recording(output_file, input_format, input_display):
    print("Beginning recording of clip")
    command = [
        'ffmpeg',
        '-f', input_format,              # Input format for macOS
        '-video_size', '1920x1080',   # Resolution
        '-framerate', '24',           # Frame rate
        '-i', input_display,                # Input display (1 or :99.0 for GitHub actions)
        '-vcodec', 'libxvid',         # Video codec
        '-preset', 'fast',            # Preset for encoding speed
        '-b:v', '3000k',              # Bitrate
        '-pix_fmt', 'yuv420p',        # Pixel format
        output_file                   # Output file path
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    return process

def stop_ffmpeg_recording(process):
    process.stdin.write(b"q\n")  # Send 'q' to gracefully stop the recording
    process.communicate()         # Wait for the process to finish
    print("Ending recording of clip")