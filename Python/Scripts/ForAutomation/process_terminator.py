import psutil
import os
from time import sleep

# Terminate notepad as a test.
find_me = "notepad.exe"
reassure = f"Watching for {find_me} in processes.."
print(reassure)

while True:
    processes = os.popen('wmic process get description, processid').read()

    for line in processes.splitlines():
        if find_me in line:
            try:
                # Remove the process name and the blank spaces so we can grab the PPID as an integer.
                ppid = int(line.strip(find_me).strip())
                # Instantiating the "Process" class as "p".
                p = psutil.Process(ppid)
                p.kill()
                print(f"Found {find_me} active as process {ppid} and terminated it.")
                print(reassure)

            except ValueError:
                # Debugging:
                print(f"'{find_me}' produced a value error in:\n{line}\n")
                continue

    sleep(1)