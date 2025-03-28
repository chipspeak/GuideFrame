---
title: Assembly
layout: default
nav_order: 5
parent: Library
permalink: assembly
---

# Assembly
The assembly file contains the functions which act to combine the various files created during the GuideFrame pipeline. The following section will list each function contained within this file and provide some insight into its use and syntax.


### assemble_audio_video()
```python
def assemble_audio_video(video_file, audio_file, output_file):
    # Check that both files exist
    if os.path.exists(video_file) and os.path.exists(audio_file):
        # Create video and audio in variables for us in combined output
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
```
This function takes a `video_file`, `audio_file` and `output_file` as arguments. It checks for these files before using the `ffmpeg` python package to combine them into a single file, named by the passed argument. This file then contains the combined audio and video for a single `guide_step`.


### combine_all_videos()
```python
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
```
This function takes `output_files` and `final_output` as arguments. It takes the array of passed files and writes them to a newly created text file called `file_list`. The `concat` function from `ffmpeg` is used with the `file_list` passed. This is the `input` portion of the command before the `output` portion uses the `final_output` name for outputted file name. 


### assemble()
```python
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
    # Now using the extract_script_name function from guideframe_utils.py to get the script name
    script_name = extract_script_name()
    # Creating a unique filename for the final output file via uuid and the extracted script name
    output_filename = f"{script_name}_{uuid.uuid4().hex[:6]}.mp4"
    # Combining all the videos into the final output as a single video
    combine_all_videos(output_files, output_filename)

    # Check if final_output exists and if so, clean up temporary files (the various mp3 and mp4 files we created)
    if os.path.exists(output_filename):
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
```
This function uses the two others from this file to perform the overall assembly and cleanup of GuideFrame step files. It takes the `clip_number` argument and uses it to iterate through a loop of all audio and video files in addition to creating the appropriately named `output_file` during the loop. 

*Note: 1 is added to account for steps starting at 1. This means an iteration from 1 -> `clip_number` will have the intended range.* 

Within each loop, these files are passed to the `assemble_audio_video()` function for combination.

An array of the files outputted by this process is then created using another loop and the `clip_number` variable. A `script_name` variable is intialised using `extract_script_name()` from `utils`. An output file is then created using the `script_name` and a randomly generated `uuid`. The array and filename are then passed to `combine_all_videos()` for final assembly.

Once this process is complete, a check that a matching file exists is performed. Provided this is successful, a cleanup loop occurs using the `clip_number` variable again to iterate through all created audio and video files with the exception of the final output.