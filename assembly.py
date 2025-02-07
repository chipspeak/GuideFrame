import ffmpeg
import os

'''
This script contains the logic used to assemble the audio and video per-step before a final assembly of all clips
before a cleanup occurs to remove the various created files. This will likely change as we move towards attempting 
containerisation/headless. In any case, this is the logic as of sprint 1 ending.
'''
# Combinging audio and video via wrapper (wrapper aids legibility and removes need for subprocess)
def assemble_audio_video(video_file, audio_file, output_file):
    # Check that both files exist
    if os.path.exists(video_file) and os.path.exists(audio_file):
        # The wrapper doesn't allow multiple .input tags like the '-i' in cli. This solution is from stack overflow
        video_in = ffmpeg.input(video_file)
        audio_in = ffmpeg.input(audio_file)
        combined_output = ffmpeg.output(video_in, audio_in, output_file, vcodec='copy', acodec='copy')
        try:
            (
                combined_output.run()
            )
            print(f"Successfully created: {output_file}")
        # Attempting to extract an error via the wrapper if one occurs
        except ffmpeg.Error as e:
            # Outputting the error
            error_output = e.stderr.decode('utf-8') if e.stderr else "No error details available."
            print(f"Error combining {video_file} and {audio_file}: {error_output}")
    else:
        print(f"Missing video or audio file: {video_file}, {audio_file}")


# Combining all of the audio + video combinations (result of the above)
def combine_all_videos(output_files, final_output):
    # Temp text file to iterate through
    file_list = "file_list.txt"

    # Write the list of video files to the same file
    with open(file_list, "w") as f:
        for video in output_files:
            if os.path.exists(video):
                f.write(f"file '{video}'\n")
            else:
                print(f"Error: {video} not found")

    try:
        # Run FFmpeg using the concat method and check for errors etc
        ffmpeg.input(file_list, format="concat", safe=0).output(final_output, vcodec='libxvid', acodec='aac').run()
        print(f"Successfully combined all videos into {final_output}")
    except ffmpeg.Error as e:
        error_output = e.stderr.decode('utf-8') if e.stderr else "No error details available."
        print(f"Error combining videos: {error_output}")
    finally:
        # Removing the txt file
        os.remove(file_list)


# Combine individual video and audio for each step (obviously needs error handling etc but will do for now) (now taking in a number of clips rather than hardcoding in aid of tutors test)
def assemble(number_of_steps):
    # Combine individual video and audio for each step by iterating through files and passing to above functions
    clip_number = number_of_steps + 1
    for i in range(1, clip_number):
        video_file = f"step{i}.mp4"
        audio_file = f"step{i}.mp3"
        output_file = f"output_step{i}.mp4"
        # Call the function to combine video and audio
        assemble_audio_video(video_file, audio_file, output_file)

    # Now that all video/audio combinations are complete, combine the output videos into the final one
    output_files = [f"output_step{i}.mp4" for i in range(1, clip_number)]
    combine_all_videos(output_files, "final_output.mp4")

    # Check if final_output exists and if so, clean up temporary files (the various mp3 and mp4 files we created)
    if os.path.exists("final_output.mp4"):
        print("Final output created. Cleaning up temporary files...")
        # Cleanup loop
        for i in range(1, clip_number):
            step_video = f"step{i}.mp4"
            step_audio = f"step{i}.mp3"
            output_step = f"output_step{i}.mp4"
            if os.path.exists(step_video):
                os.remove(step_video)
                print(f"Removed {step_video}")
            if os.path.exists(step_audio):
                os.remove(step_audio)
            if os.path.exists(output_step):
                os.remove(output_step)
                print(f"Removed {output_step}")
        print("Cleanup complete.")
    else:
        print("Final output not found. No cleanup performed.")
