import time
import subprocess

def run_script():
    script_path = "/weixw_repo/oam_branch/tr069Clone/tr_checkcommit.py"
    script_args = ["master","WNTD4"]  # Replace with your desired arguments
    subprocess.call(["python", script_path] + script_args)
    time.sleep(10)
    script_args = ["master","5GGW3-OMNI-1"]  # Replace with your desired arguments
    subprocess.call(["python", script_path] + script_args)

while True:
    # Get the current time
    current_time = time.strftime("%H:%M:%S", time.localtime())

    # Check if the current time is 00:00:00
    if current_time == "00:00:00":
        # Run your script
        run_script()

        # Wait for 24 hours before checking again
        time.sleep(23 * 60 * 60)
    else:
        # Wait for 1 second before checking the time again
        time.sleep(1)

