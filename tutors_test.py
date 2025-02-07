import sys # Importing the sys module to access system arguments
from selenium_functions import * # Moved all selenium functions to external file
import time  # Importing the time module for sleep functions
from assembly import assemble  # Importing the assemble_clips function from assembly.py
from audio import export_gtts, sleep_based_on_vo  # Importing the export_gtts and sleep_based_on_vo functions from audio.py
from video import start_ffmpeg_recording, stop_ffmpeg_recording  # Importing the start_ffmpeg_recording and stop_ffmpeg_recording functions from video.py

# Setting the environment based on the system argument (default arg must be 1 hence > 1)
if len(sys.argv) > 1:
    env = sys.argv[1]  # Getting the environment argument

    # Setting the input format and display based on the environment argument
    if env == "macos": # My local environment
        input_format = 'avfoundation'
        input_display = '1'
        driver_location = '/opt/homebrew/bin/chromedriver'
    elif env == "github": # GitHub Actions environment
        input_format = 'x11grab'
        input_display = ':99.0'
        driver_location = '/usr/bin/chromedriver'
    else:
        print("Invalid environment specified. Use 'macos' or 'github'.")
        sys.exit(1)
else:
    print("No environment argument provided. Use 'macos' or 'github'.")
    sys.exit(1)

'''
As of GUIDEFRAME-15, selenium functions have moved to external script. This is to facilitate greater
legibility of main file for ease of use. The intention is to approach the selenium material like an SDK-lite
where documentation will outline the selenium functions and their args without the need to worry about try-catch,
selenium syntax etc. This is simply the first step in that process.
'''

# Function to run the main walkthrough section
def guideframe_script():
    # Main walkthrough logic here divided into steps etc (will hopefully be more legible after future refactors)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    try:
        '''
        Setup - Setup driver and Open Tutors.dev and set window size etc
        '''
        driver = driver_setup(driver_location) # Initializing driver as the return value from the setup function in selenium script
        set_window_size(driver)
        open_url(driver, "https://tutors.dev")
        time.sleep(2)  # Give the page time to load

        '''
        Step 1 - Open Tutors
        '''
        recording1 = start_ffmpeg_recording("step1.mp4", input_format, input_display)
        export_gtts("First, let's open tutors.dev. On this page we see the web toolkit, in addition to any courses we may recently have accessed.", "step1.mp3")
        # sleep_based_on_vo("step1.mp3") # removed to test pacing
        stop_ffmpeg_recording(recording1)

        '''
        Step 2 - setting dark mode
        '''
        recording2 = start_ffmpeg_recording("step2.mp4", input_format, input_display)
        export_gtts("Before we go any further, let's change to dark mode using the layout button in the top right of the screen", "step2.mp3")
        # sleep_based_on_vo("step2.mp3") # removed to test pacing
        # clicking layout button
        click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block")
        time.sleep(2)  # Wait for the navigation to complete
        # clicking the dark mode button
        click_element(driver, "label[data-testid='segment-item']")
        time.sleep(2)  # Wait for the navigation to complete
        # clicking layout button again to close
        click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block")
        stop_ffmpeg_recording(recording2)

        '''
        Step 3 - navigating to the docs page
        '''
        recording3 = start_ffmpeg_recording("step3.mp4", input_format, input_display)
        export_gtts("Now that we're in dark mode, let's navigate to the docs page by clicking the docs button under the web toolkit", "step3.mp3")
        # sleep_based_on_vo("step3.mp3") # removed to test pacing
        # hovering over and clicking the docs link
        hover_and_click(driver, "/course/tutors-reference-manual")
        # time.sleep(2)
        stop_ffmpeg_recording(recording3)

        '''
        Step 4 - Docs page intro
        '''
        recording4 = start_ffmpeg_recording("step4.mp4", input_format, input_display)
        export_gtts("On the docs page, we can see a number of cards. Each of these cards leads to a specific portion of the getting started guide.", "step4.mp3")
        # sleep_based_on_vo("step4.mp3") # removed to test pacing
        stop_ffmpeg_recording(recording4)

        '''
        Step 5 - Hovering over the first card
        '''
        recording5 = start_ffmpeg_recording("step5.mp4", input_format, input_display)
        hover_over_element(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started")
        export_gtts("The getting started card introduces the basic design model of tutors.", "step5.mp3")
        sleep_based_on_vo("step5.mp3")
        stop_ffmpeg_recording(recording5)

        '''
        Step 6 - Hovering over the second card
        '''
        recording6 = start_ffmpeg_recording("step6.mp4", input_format, input_display)
        hover_over_element(driver, "/course/tutors-starter-course")
        export_gtts("The simple starter card provides a helpful template course.", "step6.mp3")
        sleep_based_on_vo("step6.mp3")
        stop_ffmpeg_recording(recording6)

        '''
        Step 7 - Hovering over the third card
        '''
        recording7 = start_ffmpeg_recording("step7.mp4", input_format, input_display)
        hover_over_element(driver, "/course/layout-reference-course")
        export_gtts("The alternative starter card provides an example course to demonstrate layouts and nesting.", "step7.mp3")
        sleep_based_on_vo("step7.mp3")
        stop_ffmpeg_recording(recording7)

        '''
        Step 8 - Hovering over the fourth card
        '''
        recording8 = start_ffmpeg_recording("step8.mp4", input_format, input_display)
        scroll_to_element(driver, "/course/reference-course")
        hover_over_element(driver, "/course/reference-course")
        export_gtts("The reference course contains another example course. This one contains all Tutors learning objects for demonstration.", "step8.mp3")
        sleep_based_on_vo("step8.mp3")
        stop_ffmpeg_recording(recording8)

        '''
        Step 9 - Retuning to the original card
        '''
        recording9 = start_ffmpeg_recording("step9.mp4", input_format, input_display)
        scroll_to_element(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started")
        hover_and_click(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started")
        export_gtts("Finally, let's return to the getting started card and click it to demonstrate the getting started page.", "step9.mp3")
        sleep_based_on_vo("step9.mp3")
        print("End of test")
        stop_ffmpeg_recording(recording9)

    finally:
        print("Test complete -> moving to assembly")
        driver.quit()

# End of walkthrough section
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Main function to run the test and assemble the clips (now passing the number of steps to the assembly function)
if __name__ == "__main__":
    guideframe_script()
    assemble(9)
