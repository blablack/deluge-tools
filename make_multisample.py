import glob
import os
import re
import wave

from lxml import etree
from tqdm import tqdm


def check_for_one_regex(wav_files: list[str], regex_pattern: str) -> bool:
    if not wav_files:
        return False

    for one_full_path_file in wav_files:
        one_file = os.path.basename(one_full_path_file)
        if not re.match(regex_pattern, one_file):
            return False

    return True


def check_if_folder_is_synth(wav_files: list[str]) -> bool:
    if not wav_files:
        return False

    regex_pattern = r".*[A-G]#?-?[0-9]\.wav"

    if check_for_one_regex(wav_files, regex_pattern):
        return (True, 1)

    regex_pattern = r".*[A-G]#?-?[0-9]?-[A-Z0-9]{4}\.wav"

    if check_for_one_regex(wav_files, regex_pattern):
        return (True, 2)

    regex_pattern = r".*[A-G]#?-?[0-9]_0001\.wav"
    if check_for_one_regex(wav_files, regex_pattern):
        return (True, 3)

    regex_pattern = r".*[A-G]#?-?[0-9]_0002\.wav"
    if check_for_one_regex(wav_files, regex_pattern):
        return (True, 3)

    regex_pattern = r".*[A-G]#?-?[0-9]_0003\.wav"
    if check_for_one_regex(wav_files, regex_pattern):
        return (True, 3)

    regex_pattern = r".*[a-g]#?[0-9]\.wav"
    if check_for_one_regex(wav_files, regex_pattern):
        return (True, 4)

    return (False, None)


def clean_and_format_string(input_string: str) -> str:
    parts = input_string.split("_")
    formatted_string = " ".join(word.capitalize() for word in parts)

    return formatted_string


def list_paths(root_dir: str) -> list[str]:
    print(f"Find all synths...")
    folders_with_wav_files = []
    ignored_folders = []

    all_paths = [dirpath for dirpath, dirs, _ in os.walk(root_dir) if not dirs]

    all_paths.sort()

    with tqdm(total=len(all_paths)) as pbar:
        for dirpath in all_paths:
            wav_files = glob.glob(os.path.join(dirpath, "*.wav"))
            (is_it_synth_folder, regex_type) = check_if_folder_is_synth(wav_files)
            if is_it_synth_folder:
                folders_with_wav_files.append(SampleFolder(dirpath, regex_type))
            else:
                ignored_folders.append(dirpath)
            pbar.update(1)

    print(f"Number of synths found: {len(folders_with_wav_files)}")

    if ignored_folders:
        print(f"Ignored paths:")
        for one_folder in ignored_folders:
            print(f"\t{one_folder}")

    return folders_with_wav_files


class SampleFolder:
    def __init__(self, path, regex_type):
        self.path = path

        self.regex_type = regex_type


class SampleFile:
    def __init__(self, path, filename, regex_type):
        self.path = path

        self.filename = filename

        self.regex_type = regex_type

        # 1 r".*[A-G]#?-?[0-9]\.wav"
        # 2 r".*[A-G]#?-?[0-9]?-[A-Z0-9]{4}\.wav"
        # 3 r".*[A-G]#?-?[0-9]_0001\.wav"

        match self.regex_type:
            case 1:
                result_string = filename[:-4]
            case 2:
                result_string = filename[:-9]
            case 3:
                result_string = filename[:-9]
            case 4:
                result_string = filename[:-4]

        try:
            self.octave = int(result_string[-2:])
        except:
            try:
                self.octave = int(result_string[-1:])
            except:
                print(path)
                print(filename)
                raise

        if self.octave < 0:
            result_string = result_string[:-2]
        else:
            result_string = result_string[:-1]

        if result_string[-1:] == "#":
            self.note = result_string[-2:].upper()
        else:
            self.note = result_string[-1:].upper()

        match self.note:
            case "C":
                self.note_digit = 1
            case "C#":
                self.note_digit = 2
            case "D":
                self.note_digit = 3
            case "D#":
                self.note_digit = 4
            case "E":
                self.note_digit = 5
            case "F":
                self.note_digit = 6
            case "F#":
                self.note_digit = 7
            case "G":
                self.note_digit = 8
            case "G#":
                self.note_digit = 9
            case "A":
                self.note_digit = 10
            case "A#":
                self.note_digit = 11
            case "B":
                self.note_digit = 12
            case _:
                print(path)
                print(filename)
                raise Exception(f"Sorry, {self.note} not a note")

    def __repr__(self) -> str:
        return f"({self.filename} - {self.note} {self.octave})"

    def get_fullpath(self) -> str:
        path_string = os.path.join(self.path, self.filename)
        start_index = path_string.find("SAMPLES")
        return path_string[start_index:]

    def get_nframes(self) -> int:
        try:
            with wave.open(os.path.join(self.path, self.filename), "rb") as wav_file:
                num_frames = wav_file.getnframes()
            return num_frames
        except:
            print(f"File {self.filename} is corrupted")
            raise

    def get_deluge_rangeTopNote(self) -> int:
        rangeTopNote = self.note_digit + self.octave * 12 - 1 + 12 + 12
        return (rangeTopNote, 60 - rangeTopNote)


def generate_xml(sample_list: list[SampleFile]) -> str:
    sound = etree.Element(
        "sound",
        firmwareVersion="4.1.3",
        earliestCompatibleFirmware="4.1.0-alpha",
        polyphonic="poly",
        voicePriority="1",
        mode="subtractive",
        lpfMode="24dB",
        modFXType="none",
    )

    osc1 = etree.SubElement(
        sound,
        "osc1",
        type="sample",
        loopMode="0",
        reversed="0",
        timeStretchEnable="0",
        timeStretchAmount="0",
    )

    sampleRanges = etree.SubElement(osc1, "sampleRanges")

    deluge_notes_already_done = []

    for one_sample in sample_list:
        deluge_note = one_sample.get_deluge_rangeTopNote()

        if deluge_note not in deluge_notes_already_done:
            deluge_notes_already_done.append(deluge_note)
            try:
                nframes = one_sample.get_nframes()

                sampleRange = etree.SubElement(
                    sampleRanges,
                    "sampleRange",
                    rangeTopNote=str(deluge_note[0]),
                    fileName=one_sample.get_fullpath(),
                    transpose=str(deluge_note[1]),
                )
                etree.SubElement(
                    sampleRange,
                    "zone",
                    startSamplePos="0",
                    endSamplePos=str(nframes),
                )
            except Exception:
                pass

    etree.SubElement(
        sound,
        "osc2",
        type="square",
        transpose="0",
        cents="0",
        retrigPhase="-1",
    )

    etree.SubElement(sound, "lfo1", type="triangle", syncLevel="0")

    etree.SubElement(sound, "lfo2", type="triangle")
    etree.SubElement(sound, "unison", num="1", detune="8")

    etree.SubElement(sound, "delay", pingPong="1", analog="0", syncLevel="7")

    etree.SubElement(sound, "compressor", syncLevel="6", attack="327244", release="936")

    defaultParams = etree.SubElement(
        sound,
        "defaultParams",
        arpeggiatorGate="0x00000000",
        portamento="0x80000000",
        compressorShape="0xDC28F5B2",
        oscAVolume="0x7FFFFFFF",
        oscAPulseWidth="0x00000000",
        oscAWavetablePosition="0x00000000",
        oscBVolume="0x80000000",
        oscBPulseWidth="0x00000000",
        oscBWavetablePosition="0x00000000",
        noiseVolume="0x80000000",
        volume="0x4CCCCCA8",
        pan="0x00000000",
        lpfFrequency="0x7FFFFFFF",
        lpfResonance="0x80000000",
        hpfFrequency="0x80000000",
        hpfResonance="0x80000000",
        lfo1Rate="0x1999997E",
        lfo2Rate="0x00000000",
        modulator1Amount="0x80000000",
        modulator1Feedback="0x80000000",
        modulator2Amount="0x80000000",
        modulator2Feedback="0x80000000",
        carrier1Feedback="0x80000000",
        carrier2Feedback="0x80000000",
        modFXRate="0x00000000",
        modFXDepth="0x00000000",
        delayRate="0x00000000",
        delayFeedback="0x80000000",
        reverbAmount="0x80000000",
        arpeggiatorRate="0x00000000",
        stutterRate="0x00000000",
        sampleRateReduction="0x80000000",
        bitCrush="0x80000000",
        modFXOffset="0x00000000",
        modFXFeedback="0x00000000",
    )

    etree.SubElement(
        defaultParams,
        "envelope1",
        attack="0x80000000",
        decay="0xE6666654",
        sustain="0x7FFFFFFF",
        release="0x02000000",
    )

    etree.SubElement(
        defaultParams,
        "envelope2",
        attack="0xE6666654",
        decay="0xE6666654",
        sustain="0xFFFFFFE9",
        release="0xE6666654",
    )

    patchCables = etree.SubElement(defaultParams, "patchCables")

    etree.SubElement(
        patchCables,
        "patchCable",
        source="velocity",
        destination="volume",
        amount="0x3FFFFFE8",
    )

    etree.SubElement(
        patchCables,
        "patchCable",
        source="aftertouch",
        destination="volume",
        amount="0x2A3D7094",
    )

    etree.SubElement(
        patchCables,
        "patchCable",
        source="y",
        destination="lpfFrequency",
        amount="0x19999990",
    )

    etree.SubElement(
        defaultParams,
        "equalizer",
        bass="0x00000000",
        treble="0x00000000",
        bassFrequency="0x00000000",
        trebleFrequency="0x00000000",
    )

    etree.SubElement(sound, "arpeggiator", mode="off", numOctaves="2", syncLevel="7")

    modKnobs = etree.SubElement(sound, "modKnobs")
    etree.SubElement(modKnobs, "modKnob", controlsParam="pan")
    etree.SubElement(modKnobs, "modKnob", controlsParam="volumePostFX")
    etree.SubElement(modKnobs, "modKnob", controlsParam="lpfResonance")
    etree.SubElement(modKnobs, "modKnob", controlsParam="lpfFrequency")
    etree.SubElement(modKnobs, "modKnob", controlsParam="env1Release")
    etree.SubElement(modKnobs, "modKnob", controlsParam="env1Attack")
    etree.SubElement(modKnobs, "modKnob", controlsParam="delayFeedback")
    etree.SubElement(modKnobs, "modKnob", controlsParam="delayRate")
    etree.SubElement(modKnobs, "modKnob", controlsParam="reverbAmount")
    etree.SubElement(
        modKnobs,
        "modKnob",
        controlsParam="volumePostReverbSend",
        patchAmountFromSource="compressor",
    )
    etree.SubElement(
        modKnobs, "modKnob", controlsParam="pitch", patchAmountFromSource="lfo1"
    )
    etree.SubElement(modKnobs, "modKnob", controlsParam="lfo1Rate")
    etree.SubElement(modKnobs, "modKnob", controlsParam="portamento")
    etree.SubElement(modKnobs, "modKnob", controlsParam="stutterRate")
    etree.SubElement(modKnobs, "modKnob", controlsParam="bitcrushAmount")
    etree.SubElement(modKnobs, "modKnob", controlsParam="sampleRateReduction")

    final_string = etree.tostring(
        sound, xml_declaration=True, encoding="UTF-8", pretty_print=True
    )

    final_string = final_string.replace(b"&amp;", b"&")

    return final_string


def generate_synth(root_dir: SampleFolder) -> str:
    files_to_use = 20

    sample_list = [
        SampleFile(root_dir.path, o, root_dir.regex_type)
        for o in os.listdir(root_dir.path)
    ]

    sample_list.sort(key=lambda x: (x.octave, x.note_digit))

    file_count = len(sample_list)
    if file_count > files_to_use:
        modulo_calc = round(file_count / 20)

        new_list = []
        i = 0
        for o in sample_list:
            if i % modulo_calc == 0:
                new_list.append(o)
            i += 1

        sample_list = new_list

    return generate_xml(sample_list)


def write_xml(xml_string: str, synth_path: str, root_path: str) -> None:
    output_folder = "output"

    result_folder = synth_path.replace(root_path, "")

    name = clean_and_format_string(os.path.basename(root_path))

    folders = os.path.normpath(result_folder)
    folders = folders.split(os.sep)
    folders = [
        clean_and_format_string(one_folder)
        for one_folder in folders
        if len(one_folder) > 0
    ]

    final_path = os.path.join(output_folder, name, *folders[:-1])
    os.makedirs(final_path, exist_ok=True)

    with open(f"{os.path.join(output_folder, name, *folders)}.xml", "wb") as f:
        f.write(xml_string)


def generate_all_synths(found_synths_path: list[SampleFolder], path: str) -> None:
    print(f"Write all synths XML...")

    with tqdm(total=len(found_synths_path)) as pbar:
        for one_synth_path in found_synths_path:
            xml_string = generate_synth(one_synth_path)
            write_xml(xml_string, one_synth_path.path, path)
            pbar.update(1)


def process_folder(path: str) -> None:
    name = os.path.basename(path)

    print(f"Processing: {clean_and_format_string(name)}")

    print()

    found_synths_path = list_paths(path)

    print()

    generate_all_synths(found_synths_path, path)


if __name__ == "__main__":
    path = [
        "/media/blablack/15BC-5006/SAMPLES/MyStuff/Samples from Mars/Synths/junos_from_mars",
    ]

    for one_path in path:
        process_folder(one_path)
