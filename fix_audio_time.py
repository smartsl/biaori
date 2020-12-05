import os
import sys
import itertools
import json
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def split_on_silence_ex(
    audio_segment,
    min_silence_len=1000,
    silence_thresh=-16,
    keep_silence=100,
    seek_step=1,
):
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    if isinstance(keep_silence, bool):
        keep_silence = len(audio_segment) if keep_silence else 0

    output_ranges = [
        [start - keep_silence, end + keep_silence]
        for (start, end) in detect_nonsilent(
            audio_segment, min_silence_len, silence_thresh, seek_step
        )
    ]

    for range_i, range_ii in pairwise(output_ranges):
        last_end = range_i[1]
        next_start = range_ii[0]
        if next_start < last_end:
            range_i[1] = (last_end + next_start) // 2
            range_ii[0] = range_i[1]

    return [
        [max(start, 0), min(end, len(audio_segment))] for start, end in output_ranges
    ]


def get_chunks(sound, silence_thresh, min_nonsilence):
    chunks = split_on_silence_ex(
        sound, min_silence_len=50, silence_thresh=silence_thresh, keep_silence=0
    )
    chunks_ok = []
    chunks_short = []
    for chunk in chunks:
        if chunk[1] - chunk[0] >= min_nonsilence:
            chunks_ok.append(chunk)
        else:
            chunks_short.append(chunk)
            chunks_short[-1].append(chunk[1] - chunk[0])
    return chunks_ok, chunks_short


def get_pepm_chunks(
    mp3_path, debug=False, silence_thresh=-200, min_nonsilence=0, search=0
):
    if not os.path.isfile(mp3_path):
        return []

    chunks_path = mp3_path + ".txt"
    if not debug:
        if os.path.isfile(chunks_path):
            with open(chunks_path, "r") as f:
                chunks = json.load(f)
            return None, chunks

    sound = AudioSegment.from_mp3(mp3_path)
    sound_rms = mp3_path + ".rms.log"
    sound_dBFS = mp3_path + ".dBFS.log"
    if debug and not (os.path.isfile(sound_rms) and os.path.isfile(sound_dBFS)):
        with open(sound_rms, "w", encoding="utf-8") as f1:
            with open(sound_dBFS, "w", encoding="utf-8") as f2:
                f1.write("len(sound): %s\n" % len(sound))
                f2.write("len(sound): %s\n" % len(sound))

                # "graph" the volume in 0.001 second increments
                for x in range(0, int(len(sound))):
                    f1.write("%s\t%s\n" % (x, sound[x : x + 1].rms))
                    f2.write("%s\t%s\n" % (x, sound[x : x + 1].dBFS))

    sname, _sext = os.path.splitext(mp3_path)
    sname += ".ogg"
    if not os.path.isfile(sname):
        sound.export(sname, format="ogg", bitrate="48k")

    if search:
        best = silence_thresh
        err = sys.maxsize
        for tmp in range(silence_thresh - 10, silence_thresh + 10):
            chunks_ok, chunks_short = get_chunks(sound, tmp, min_nonsilence)
            if abs(len(chunks_ok) - search) < err:
                best = tmp
                err = abs(len(chunks_ok) - search)
        print(best, len(chunks_ok))
        return [sound, []]
    else:
        chunks_ok, chunks_short = get_chunks(sound, silence_thresh, min_nonsilence)

    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks_ok, f, ensure_ascii=False, separators=(",", ":"))
    if chunks_short:
        with open(chunks_path + ".txt", "w", encoding="utf-8") as f:
            json.dump(
                chunks_short, f, ensure_ascii=False, separators=(",", ":"), indent=4
            )

    return sound, chunks_ok


if __name__ == "__main__":
    book = str(1 + 1)
    unit = str(7 + 1)
    lesson = str(31 + 1)
    pepm_dir = (
        r"assets\book" + book + r"\book" + book + r"-unit" + unit + r"\lesson" + lesson
    )
    sound, chunks = get_pepm_chunks(
        os.path.join(pepm_dir, "lesson_words.pepm"),
        debug=False,
        silence_thresh=-66,
        min_nonsilence=500,
    )
    print(chunks)
    print("number of chunks", len(chunks))
