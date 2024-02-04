import subprocess
import shutil

# aubioonset -i audio.wav > onset.txt

i = 1

with open("onset.txt", "r") as onset_file:
    for onset in onset_file:
        start_time = onset.strip()
        formatted_i = f"{i:02}"

        print(f"Splitting at {start_time}")

        subprocess.run(["sox", "audio.wav", "tmp1.wav", "trim", start_time, "18"])
        subprocess.run(
            [
                "sox",
                "tmp1.wav",
                "tmp2.wav",
                "silence",
                "1",
                "0.0",
                "0.1%",
                "reverse",
                "silence",
                "1",
                "0.0",
                "0.1%",
                "reverse",
                "pad",
                "0",
                "0.5",
            ]
        )
        subprocess.run(["rm", "-rf", "tmp1.wav"])
        subprocess.run(
            ["sox", "tmp2.wav", "-b", "16", "-r", "48000", "-c", "2", "tmp3.wav"]
        )
        subprocess.run(["rm", "-rf", "tmp2.wav"])
        subprocess.run(["mv", "tmp3.wav", f"output_{formatted_i}.wav"])
        subprocess.run(["rm", "-rf", "tmp3.wav"])

        i += 1

all_instr = [
    "Kick",
    "Snare",
    "Hat edge closed",
    "Hat edge open",
    "Hat top closed",
    "Hat top open",
    "High crash",
    "Med crash",
    "Low crash",
    "Floor tom",
    "Lo tom",
    "Hi tom",
    "Ride edge",
    "Ride",
    "Ride bell",
]

i = 0

for t in all_instr:
    print(t)

    i += 1
    formatted_i = f"{i:02}"
    shutil.move(f"output_{formatted_i}.wav", f"{t} loud.wav")

    i += 1
    formatted_i = f"{i:02}"
    shutil.move(f"output_{formatted_i}.wav", f"{t} quiet.wav")
