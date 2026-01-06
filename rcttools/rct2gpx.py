import logging
import os.path
from datetime import datetime, timezone
from typing import Dict, List, Tuple

import ffmpeg  # type: ignore[import-untyped]
import numpy as np
import pandas as pd
from gpxpy.gpx import GPX, GPXTrack, GPXTrackPoint, GPXTrackSegment
from PIL import Image

from .alphabet import NUMBERS, NUMBERS_SHAPE
from .common import CHAR_WIDTHS, FLOAT_FRAME_TYPE, FLOAT_VIDEO_TYPE, VIDEO_TYPE
from .text_format import EmbeddedData, StateMachine


def transcode(mp4_path: str) -> VIDEO_TYPE:
    """
    Transcode an MP4 video file to extract the region with data.

    Currently assumes 1080p video.
    """
    height = 40
    width = 1450
    mp4 = ffmpeg.input(mp4_path)
    trimmed = mp4.filter("crop", w=width, h=height, x=0, y=1035)
    white = ffmpeg.input(f"color=white:s={width}x{height}", f="lavfi")
    black = ffmpeg.input(f"color=black:s={width}x{height}", f="lavfi")
    out, _ = (
        ffmpeg.filter([trimmed, white, white, black], "threshold")
        .output("pipe:", format="rawvideo", pix_fmt="rgb24")
        .run(capture_stdout=True, quiet=True)
    )
    return np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])


def fast_parse(
    mp4_path: str, write_stacked_frames: bool = False, output_directory: str = ""
) -> Tuple[dict[int, EmbeddedData], pd.Series[float]]:
    alphabet = NUMBERS

    video = transcode(mp4_path)

    start_time = datetime.now(timezone.utc)

    y_offsets = {0: StateMachine(), -1: StateMachine(True)}
    seconds_digit_video: Dict[int, FLOAT_VIDEO_TYPE] = {
        y_offset: 1
        - (
            video[:, (5 + y_offset) : (35 + y_offset), 561 : 561 + NUMBERS_SHAPE[1]]
            / 255.0
        )
        for y_offset in y_offsets
    }

    change_scores: Dict[
        int, Dict[str, np.ndarray[Tuple[int], np.dtype[np.float32]]]
    ] = {}
    best_average = 0.0
    change_df = pd.DataFrame()
    selected_y = 0
    for y in y_offsets:
        change_scores[y] = {}
        for letter in alphabet:
            change_scores[y][letter] = alphabet[letter].score_video(
                seconds_digit_video[y]
            )

        current_df = pd.DataFrame(change_scores[y])
        current_average = current_df.max(axis=1).mean()
        if current_average > best_average:
            change_df = current_df
            best_average = current_average
            selected_y = y

    best_fit = change_df.idxmax(axis=1)

    changes = best_fit[best_fit != best_fit.shift(1)].index
    change_max = change_df.max(axis=1)

    ranges: List[Tuple[int, int]] = []
    for i in range(len(changes) - 1):
        if change_max[i] > 0.8:
            ranges.append((changes[i], changes[i + 1]))
    ranges.append((changes[-1], len(video)))

    stacked_frames: Dict[int, FLOAT_FRAME_TYPE] = {}
    for r in ranges:
        stacked_frames[r[0]] = video[r[0] : r[1]].mean(axis=0)
        if write_stacked_frames:
            path = os.path.join(output_directory, f"data_{r[0]}.png")
            Image.fromarray(stacked_frames[r[0]].astype(np.uint8)).save(path)

    result: Dict[int, EmbeddedData] = {}
    summary_stats: Dict[int, float] = {}
    state_machine = y_offsets[selected_y]
    for frame_index, stacked_frame in stacked_frames.items():
        chars: List[str] = []
        best_scores: List[float] = []

        while not state_machine.is_complete():
            alphabet = state_machine.get_alphabet()
            if alphabet == {}:
                continue
            offset = state_machine.get_next_offset()
            offset_frame = {
                width: (
                    1
                    - (
                        stacked_frame[
                            (5 + selected_y) : (35 + selected_y),
                            offset : offset + width,
                        ]
                        / 255.0
                    )
                )
                for width in set(CHAR_WIDTHS[x] for x in alphabet.keys())
            }
            scores = {
                letter: alphabet[letter].score_frame(offset_frame[CHAR_WIDTHS[letter]])
                for letter in alphabet
            }
            max_score = 0.0
            max_letter = ""
            for letter, score in scores.items():
                if score > max_score:
                    max_score = score
                    max_letter = letter

            state_machine.append(max_letter)
            chars.append(max_letter)
            best_scores.append(max_score)

        result[int(frame_index)] = state_machine.result()
        summary_stats[int(frame_index)] = pd.Series(best_scores).mean()
        state_machine.reset()

    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()
    logging.info(f"Parsed {len(video)} frames in {duration:.2f} seconds")

    return result, pd.Series(summary_stats)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract GPX data embedded in MP4 video files from Garmin Varia RCT715 devices",
    )
    parser.add_argument("mp4_path", type=str)
    parser.add_argument("--csv", action="store_true", help="Output results to CSV file")
    parser.add_argument(
        "--write-stacked-frames",
        action="store_true",
        help="Write stacked frames to PNG files",
    )
    parser.add_argument("--no-gpx", action="store_true", help="Do not output GPX file")
    parser.add_argument(
        "--output-directory",
        type=str,
        default="",
        help="Directory to save output files",
    )
    parser.add_argument(
        "--show-stats", action="store_true", help="Show summary statistics"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    mp4_path = args.mp4_path
    prefix = os.path.dirname(mp4_path)
    if args.output_directory:
        prefix = args.output_directory
    basename = os.path.basename(mp4_path).rsplit(".", 1)[0]
    csv = args.csv
    gpx = not args.no_gpx
    show_stats = args.show_stats
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    result, summary_stats = fast_parse(
        mp4_path,
        write_stacked_frames=args.write_stacked_frames,
        output_directory=prefix,
    )

    if show_stats or args.verbose:
        output_func = print if not args.verbose else logging.info
        output_func(f"Summary statistics for {mp4_path}:")
        stats = summary_stats.to_frame(name="goodness_of_fit")
        stats.index.name = "frame_index"
        output_func(stats)

    if csv:
        df = pd.DataFrame.from_dict(result, orient="index")
        df.index.name = "frame_index"
        csv_path = os.path.join(prefix, f"{basename}.csv")
        df.to_csv(csv_path)

    if gpx:
        gpx_obj = GPX()
        track = GPXTrack()
        gpx_obj.tracks.append(track)
        segment = GPXTrackSegment()
        track.segments.append(segment)

        for frame_index in sorted(result.keys()):
            data = result[frame_index]
            if data["latitude"] is not None and data["longitude"] is not None:
                segment.points.append(
                    GPXTrackPoint(
                        latitude=float(data["latitude"]),
                        longitude=float(data["longitude"]),
                        time=data["datetime"],
                    )
                )
        gpx_path = os.path.join(prefix, f"{basename}.gpx")
        with open(gpx_path, "w") as f:
            f.write(gpx_obj.to_xml(version="1.1"))


if __name__ == "__main__":
    main()
