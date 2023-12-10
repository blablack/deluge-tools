#########################################################
##                                                     ##
## Script used to lean Wave Alchemy samples            ##
##                                                     ##
#########################################################

import glob
import os
import wave

from tqdm import tqdm

def check_one_wave_file(filename: str) -> None:
    try:
        with wave.open(filename, "rb") as wave_file:
            frames = wave_file.readframes(-1)
            sample_width = wave_file.getsampwidth()
            num_channels = wave_file.getnchannels()
            frame_rate = wave_file.getframerate()
            comptype = wave_file.getcomptype()
            compname = wave_file.getcompname()
            nframes = wave_file.getnframes()
            if (comptype != "NONE") or (compname != "not compressed") or (nframes <= 0):
                raise Exception()
    except:
        print(f"File {filename} is corrupted")
        raise


def process_path(path: str) -> None:
    all_paths = [dirpath for dirpath, dirs, _ in os.walk(path) if not dirs]

    all_paths.sort()

    with tqdm(total=len(all_paths)) as pbar:
        for dirpath in all_paths:
            wav_files = glob.glob(os.path.join(dirpath, "*.wav"))
            for one_wave_file in wav_files:
                check_one_wave_file(one_wave_file)
            pbar.update(1)


if __name__ == "__main__":
    path = "/home/blablack/ZGarbage/SAMPLES/MyStuff/Samples from Mars"

    process_path(path)
