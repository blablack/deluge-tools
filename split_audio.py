import subprocess
import shutil
import os

# aubioonset -i audio.wav > onset.txt

i = 1

with open("onset.txt", "r") as onset_file:
    head = [next(onset_file) for _ in range(2)]
    start = float(head[0].strip())
    end = float(head[1].strip())
    duration = round(end-start)-0.5
    print(duration)

os.makedirs("output", exist_ok=True)

with open("onset.txt", "r") as onset_file:
    for onset in onset_file:
        start_time = onset.strip()
        formatted_i = f"{i:02}"

        print(f"Splitting at {start_time}")

        subprocess.run(["sox", "audio.wav", os.path.join("output", "tmp1.wav"), "trim", start_time, str(duration)])
        subprocess.run(
            [
                "sox",
                os.path.join("output", "tmp1.wav"),
                os.path.join("output", "tmp2.wav"),
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
        subprocess.run(["rm", "-rf", os.path.join("output", "tmp1.wav")])
        subprocess.run(
            ["sox", os.path.join("output", "tmp2.wav"), "-b", "16", "-r", "48000", "-c", "2", os.path.join("output", "tmp3.wav")]
        )
        subprocess.run(["rm", "-rf", os.path.join("output", "tmp2.wav")])
        subprocess.run(["mv", os.path.join("output", "tmp3.wav"), os.path.join("output", f"output_{formatted_i}.wav")])
        subprocess.run(["rm", "-rf", os.path.join("output", "tmp3.wav")])

        i += 1

all_instr = [
    "Kick",
    "Snare",
    "Hat edge closed",
    "Hat edge open",
    "Hat top closed",
    "Hat top open",
    "Crash",
    "Floor tom",
    "Rack tom",
    "Ride edge",
    "Ride",
    "Ride bell",
]

i = 0

for t in all_instr:
    print(t)

    i += 1
    formatted_i = f"{i:02}"
    shutil.move(os.path.join("output", f"output_{formatted_i}.wav"), os.path.join("output", f"{t} 4.wav"))

    i += 1
    formatted_i = f"{i:02}"
    shutil.move(os.path.join("output", f"output_{formatted_i}.wav"), os.path.join("output", f"{t} 3.wav"))

    i += 1
    formatted_i = f"{i:02}"
    shutil.move(os.path.join("output", f"output_{formatted_i}.wav"), os.path.join("output", f"{t} 2.wav"))

    i += 1
    formatted_i = f"{i:02}"
    shutil.move(os.path.join("output", f"output_{formatted_i}.wav"), os.path.join("output", f"{t} 1.wav"))
