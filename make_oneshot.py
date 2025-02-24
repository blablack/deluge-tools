import os
import wave


def get_nframes(one_file: str) -> int:
    try:
        with wave.open(one_file, "rb") as wav_file:
            num_frames = wav_file.getnframes()
        return num_frames
    except:
        print(f"File {one_file} is corrupted")
        raise


def write_one_file(rootpath: str, dirpath: str, one_file: str):
    new_dirpath = dirpath[dirpath.index("SAMPLES") :]
    folder_name = "output/" + dirpath[len(rootpath) :]
    xmlfilename = one_file[: one_file.index(".wav")] + ".XML"

    if not os.path.exists(folder_name):
        # Create the folder if it doesn't exist
        os.makedirs(folder_name)

    with open(folder_name + "/" + xmlfilename, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<sound\n")
        f.write('	firmwareVersion="c1.2.0"\n')
        f.write('	earliestCompatibleFirmware="4.1.0-alpha"\n')
        f.write('	polyphonic="poly"\n')
        f.write('	voicePriority="1"\n')
        f.write('	mode="subtractive"\n')
        f.write('	modFXType="none"\n')
        f.write('	lpfMode="24dB"\n')
        f.write('	hpfMode="HPLadder"\n')
        f.write('	filterRoute="H2L"\n')
        f.write('	maxVoices="8">\n')
        f.write("	<osc1\n")
        f.write('		type="sample"\n')
        f.write('		loopMode="0"\n')
        f.write('		reversed="0"\n')
        f.write('		timeStretchEnable="0"\n')
        f.write('		timeStretchAmount="0"\n')
        f.write(f'		fileName="{new_dirpath}/{one_file}"\n')
        f.write('		transpose="-5">\n')
        f.write("		<zone\n")
        f.write('			startSamplePos="0"\n')
        f.write(
            f'			endSamplePos="{str(get_nframes(os.path.join(dirpath, one_file)))}" />\n'
        )
        f.write("	</osc1>\n")
        f.write("	<osc2\n")
        f.write('		type="square"\n')
        f.write('		transpose="0"\n')
        f.write('		cents="0"\n')
        f.write('		retrigPhase="-1" />\n')
        f.write('	<lfo1 type="triangle" syncLevel="0" syncType="0" />\n')
        f.write('	<lfo2 type="triangle" syncLevel="0" syncType="0" />\n')
        f.write('	<unison num="1" detune="8" spread="0" />\n')
        f.write("	<defaultParams\n")
        f.write('		arpeggiatorGate="0x00000000"\n')
        f.write('		portamento="0x80000000"\n')
        f.write('		compressorShape="0xDC28F5B2"\n')
        f.write('		oscAVolume="0x7FFFFFFF"\n')
        f.write('		oscAPulseWidth="0x00000000"\n')
        f.write('		oscAWavetablePosition="0x00000000"\n')
        f.write('		oscBVolume="0x80000000"\n')
        f.write('		oscBPulseWidth="0x00000000"\n')
        f.write('		oscBWavetablePosition="0x00000000"\n')
        f.write('		noiseVolume="0x80000000"\n')
        f.write('		volume="0x4CCCCCA8"\n')
        f.write('		pan="0x00000000"\n')
        f.write('		lpfFrequency="0x7FFFFFFF"\n')
        f.write('		lpfResonance="0x80000000"\n')
        f.write('		hpfFrequency="0x80000000"\n')
        f.write('		hpfResonance="0x80000000"\n')
        f.write('		lfo1Rate="0x1999997E"\n')
        f.write('		lfo2Rate="0x00000000"\n')
        f.write('		modulator1Amount="0x80000000"\n')
        f.write('		modulator1Feedback="0x80000000"\n')
        f.write('		modulator2Amount="0x80000000"\n')
        f.write('		modulator2Feedback="0x80000000"\n')
        f.write('		carrier1Feedback="0x80000000"\n')
        f.write('		carrier2Feedback="0x80000000"\n')
        f.write('		modFXRate="0x00000000"\n')
        f.write('				modFXDepth="0x00000000"\n')
        f.write('				delayRate="0x00000000"\n')
        f.write('				delayFeedback="0x80000000"\n')
        f.write('				reverbAmount="0x80000000"\n')
        f.write('				arpeggiatorRate="0x00000000"\n')
        f.write('				stutterRate="0x00000000"\n')
        f.write('				sampleRateReduction="0x80000000"\n')
        f.write('				bitCrush="0x80000000"\n')
        f.write('				modFXOffset="0x00000000"\n')
        f.write('				modFXFeedback="0x00000000"\n')
        f.write('				compressorThreshold="0x00000000"\n')
        f.write('				lpfMorph="0x80000000"\n')
        f.write('				hpfMorph="0x80000000"\n')
        f.write('				waveFold="0x80000000"\n')
        f.write('				ratchetProbability="0x80000000"\n')
        f.write('				ratchetAmount="0x80000000"\n')
        f.write('				sequenceLength="0x80000000"\n')
        f.write('				rhythm="0x80000000">\n')
        f.write("				<envelope1\n")
        f.write('					attack="0x80000000"\n')
        f.write('					decay="0xE6666654"\n')
        f.write('					sustain="0x7FFFFFFF"\n')
        f.write('					release="0x02000000" />\n')
        f.write("				<envelope2\n")
        f.write('					attack="0xE6666654"\n')
        f.write('					decay="0xE6666654"\n')
        f.write('					sustain="0xFFFFFFE9"\n')
        f.write('					release="0xE6666654" />\n')
        f.write("				<patchCables>\n")
        f.write("					<patchCable\n")
        f.write('						source="velocity"\n')
        f.write('						destination="volume"\n')
        f.write('						amount="0x3FFFFFE8" />\n')
        f.write("					<patchCable\n")
        f.write('						source="aftertouch"\n')
        f.write('						destination="volume"\n')
        f.write('						amount="0x2A3D7094" />\n')
        f.write("					<patchCable\n")
        f.write('						source="y"\n')
        f.write('						destination="lpfFrequency"\n')
        f.write('						amount="0x19999990" />\n')
        f.write("				</patchCables>\n")
        f.write("				<equalizer\n")
        f.write('					bass="0x00000000"\n')
        f.write('					treble="0x00000000"\n')
        f.write('					bassFrequency="0x00000000"\n')
        f.write('					trebleFrequency="0x00000000" />\n')
        f.write("			</defaultParams>\n")
        f.write("			<arpeggiator\n")
        f.write('				mode="off"\n')
        f.write('				numOctaves="2"\n')
        f.write('				syncLevel="7"\n')
        f.write('				syncType="0"\n')
        f.write('				arpMode="off"\n')
        f.write('				noteMode="up"\n')
        f.write('				octaveMode="up"\n')
        f.write('				mpeVelocity="off" />\n')
        f.write("			<modKnobs>\n")
        f.write('				<modKnob controlsParam="pan" />\n')
        f.write('				<modKnob controlsParam="volumePostFX" />\n')
        f.write('				<modKnob controlsParam="lpfResonance" />\n')
        f.write('				<modKnob controlsParam="lpfFrequency" />\n')
        f.write('				<modKnob controlsParam="env1Release" />\n')
        f.write('				<modKnob controlsParam="env1Attack" />\n')
        f.write('				<modKnob controlsParam="delayFeedback" />\n')
        f.write('				<modKnob controlsParam="delayRate" />\n')
        f.write('				<modKnob controlsParam="reverbAmount" />\n')
        f.write(
            '				<modKnob controlsParam="volumePostReverbSend" patchAmountFromSource="compressor" />\n'
        )
        f.write('				<modKnob controlsParam="pitch" patchAmountFromSource="lfo1" />\n')
        f.write('				<modKnob controlsParam="lfo1Rate" />\n')
        f.write('				<modKnob controlsParam="portamento" />\n')
        f.write('				<modKnob controlsParam="stutterRate" />\n')
        f.write('				<modKnob controlsParam="bitcrushAmount" />\n')
        f.write('				<modKnob controlsParam="sampleRateReduction" />\n')
        f.write("			</modKnobs>\n")
        f.write("			<delay\n")
        f.write('				pingPong="1"\n')
        f.write('				analog="0"\n')
        f.write('				syncLevel="7"\n')
        f.write('				syncType="0" />\n')
        f.write("			<sidechain\n")
        f.write('				attack="327244"\n')
        f.write('				release="936"\n')
        f.write('				syncLevel="6"\n')
        f.write('				syncType="0" />\n')
        f.write("			<audioCompressor\n")
        f.write('				attack="83886080"\n')
        f.write('				release="83886080"\n')
        f.write('				thresh="0"\n')
        f.write('				ratio="1073741824"\n')
        f.write('				compHPF="0"\n')
        f.write('				compBlend="2147483647" />\n')
        f.write("		</sound>\n")


def process_folder(path: str) -> None:
    name = os.path.basename(path)

    print(f"Processing: {name}")

    for dirpath, _, files in os.walk(path):
        print(dirpath)
        for one_file in files:
            if not one_file.endswith("wav"):
                continue
            write_one_file(path, dirpath, one_file)


if __name__ == "__main__":
    path = ["/media/blablack/15BC-5006/SAMPLES/MyStuff/Moog/"]

    for one_path in path:
        process_folder(one_path)
