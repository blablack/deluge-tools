import glob
import os
import wave

from lxml import etree


class KitInstrument:
    def __init__(self, path: str):
        self.instrument_name = os.path.basename(path)
        self.samples = glob.glob(os.path.join(path, "*.wav"))

    def get_sample_path(self, index: int) -> str:
        path_string = self.samples[index]
        start_index = path_string.find("SAMPLES")
        return path_string[start_index:]

    def get_nframes(self, index: int) -> int:
        try:
            with wave.open(self.samples[index], "rb") as wav_file:
                num_frames = wav_file.getnframes()
            return num_frames
        except:
            print(f"File {self.samples[index]} is corrupted")
            raise

    def __repr__(self) -> str:
        return f"{self.instrument_name} - {len(self.samples)} instruments"


def process_folder(path: str) -> None:
    name = os.path.basename(path)

    print(f"Processing: {name}")

    all_paths = [dirpath for dirpath, dirs, _ in os.walk(path) if not dirs]

    all_instruments = []

    for dirpath in all_paths:
        kit_instrument = KitInstrument(dirpath)
        print(kit_instrument)
        all_instruments.append(kit_instrument)

    xml_string = generate_xml(all_instruments)

    write_xml(name, xml_string)


def write_xml(instrument_name: str, xml_string: str) -> None:
    output_folder = "output"

    os.makedirs(output_folder, exist_ok=True)

    with open(f"{os.path.join(output_folder, instrument_name)}.xml", "wb") as f:
        f.write(xml_string)


def generate_xml(all_instruments: [KitInstrument]) -> str:
    kit = etree.Element(
        "kit",
        firmwareVersion="4.1.3",
        earliestCompatibleFirmware="4.1.0-alpha",
        lpfMode="24dB",
        modFXType="flanger",
        modFXCurrentParam="feedback",
        currentFilterType="lpf",
    )

    delay = etree.SubElement(kit, "delay", pingPong="1", analog="0", syncLevel="7")

    compressor = etree.SubElement(
        kit,
        "compressor",
        syncLevel="6",
        attack="327244",
        release="936",
    )

    defaultParams = etree.SubElement(
        kit,
        "defaultParams",
        reverbAmount="0x80000000",
        volume="0x3504F334",
        pan="0x00000000",
        sidechainCompressorShape="0xDC28F5B2",
        modFXDepth="0x00000000",
        modFXRate="0xE0000000",
        stutterRate="0x00000000",
        sampleRateReduction="0x80000000",
        bitCrush="0x80000000",
        modFXOffset="0x00000000",
        modFXFeedback="0x80000000",
    )

    delay = etree.SubElement(
        defaultParams, "delay", rate="0x00000000", feedback="0x80000000"
    )

    lpf = etree.SubElement(
        defaultParams, "lpf", frequency="0x7FFFFFFF", resonance="0x80000000"
    )

    hpf = etree.SubElement(
        defaultParams, "hpf", frequency="0x80000000", resonance="0x80000000"
    )

    equalizer = etree.SubElement(
        defaultParams,
        "equalizer",
        bass="0x00000000",
        treble="0x00000000",
        bassFrequency="0x00000000",
        trebleFrequency="0x00000000",
    )
    soundSources = etree.SubElement(kit, "soundSources")

    for one_instrument in all_instruments:
        sound = etree.SubElement(
            soundSources,
            "sound",
            name=one_instrument.instrument_name,
            polyphonic="auto",
            voicePriority="1",
            sideChainSend="2147483647",
            mode="subtractive",
            lpfMode="24dB",
            modFXType="none",
        )

        for i in [0, 1]:
            osc = etree.SubElement(
                sound,
                f"osc{i+1}",
                type="sample",
                loopMode="1",
                reversed="0",
                timeStretchEnable="0",
                timeStretchAmount="0",
                fileName=one_instrument.get_sample_path(i),
            )

            etree.SubElement(
                osc,
                "zone",
                startSamplePos="0",
                endSamplePos=f"{one_instrument.get_nframes(i)}",
            )

        etree.SubElement(sound, "lfo1", type="triangle", syncLevel="0")
        etree.SubElement(sound, "lfo2", type="triangle")
        etree.SubElement(sound, "unison", num="1", detune="8")
        etree.SubElement(
            sound,
            "delay",
            pingPong="1",
            analog="0",
            syncLevel="7",
        )
        etree.SubElement(
            sound, "compressor", syncLevel="6", attack="327244", release="936"
        )
        defaultParams = etree.SubElement(
            sound,
            "defaultParams",
            arpeggiatorGate="0x00000000",
            portamento="0x80000000",
            compressorShape="0xDC28F5B2",
            oscAVolume="0x00000000",
            oscAPulseWidth="0x00000000",
            oscAWavetablePosition="0x00000000",
            oscBVolume="0x00000000",
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
            sound,
            "envelope1",
            attack="0x80000000",
            decay="0xE6666654",
            sustain="0x7FFFFFD2",
            release="0x80000000",
        )

        etree.SubElement(
            sound,
            "envelope2",
            attack="0xE6666654",
            decay="0xE6666654",
            sustain="0xFFFFFFE9",
            release="0xE6666654",
        )

        patchCables = etree.SubElement(sound, "patchCables")
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
            patchCables,
            "patchCable",
            source="velocity",
            destination="oscAVolume",
            amount="0x3FFFFFE8",
        )
        etree.SubElement(
            patchCables,
            "patchCable",
            source="velocity",
            destination="oscBVolume",
            amount="0xC0000018",
        )

        etree.SubElement(
            defaultParams,
            "equalizer",
            bass="0x00000000",
            treble="0x00000000",
            bassFrequency="0x00000000",
            trebleFrequency="0x00000000",
        )

        etree.SubElement(
            sound, "arpeggiator", mode="off", numOctaves="2", syncLevel="7"
        )

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
        etree.SubElement(modKnobs, "modKnob", controlsParam="pitch")
        etree.SubElement(modKnobs, "modKnob", controlsParam="stutterRate")
        etree.SubElement(modKnobs, "modKnob", controlsParam="bitcrushAmount")
        etree.SubElement(modKnobs, "modKnob", controlsParam="sampleRateReduction")

    selectedDrumIndex = etree.SubElement(kit, "selectedDrumIndex")
    selectedDrumIndex.text = "1"

    return etree.tostring(
        kit, xml_declaration=True, encoding="UTF-8", pretty_print=True
    )


if __name__ == "__main__":
    path = [
        "/home/blablack/ZGarbage/SAMPLES/MyStuff/Krautrock",
        "/home/blablack/ZGarbage/SAMPLES/MyStuff/Mapex",
    ]

    for one_path in path:
        process_folder(one_path)
