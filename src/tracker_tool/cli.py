import argparse

from tracker_tool.app import (
    convert_file,
    convert_pftrack_source_set_files,
)
from tracker_tool.config import ShotConfig
from tracker_tool.contract import (
    SOFTWARE_PFTRACK_2017,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracker-tool",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    convert_parser = subparsers.add_parser(
        "convert",
    )

    convert_parser.add_argument(
        "--source",
        required=True,
    )
    convert_parser.add_argument(
        "--target",
        required=True,
    )
    convert_parser.add_argument(
        "--input",
        required=True,
    )
    convert_parser.add_argument(
        "--output",
        required=True,
    )
    convert_parser.add_argument(
        "--width",
        required=True,
        type=int,
    )
    convert_parser.add_argument(
        "--height",
        required=True,
        type=int,
    )
    convert_parser.add_argument(
        "--start-frame",
        required=True,
        type=int,
    )
    convert_parser.add_argument(
        "--end-frame",
        type=int,
        default=None,
    )
    convert_parser.add_argument(
        "--pftrack-source-role",
        default=None,
    )

    source_set_parser = subparsers.add_parser(
        "convert-pftrack-source-set",
    )

    source_set_parser.add_argument(
        "--autotrack-input",
        required=True,
    )
    source_set_parser.add_argument(
        "--usertrack-input",
        required=True,
    )
    source_set_parser.add_argument(
        "--target",
        required=True,
    )
    source_set_parser.add_argument(
        "--output",
        required=True,
    )
    source_set_parser.add_argument(
        "--width",
        required=True,
        type=int,
    )
    source_set_parser.add_argument(
        "--height",
        required=True,
        type=int,
    )
    source_set_parser.add_argument(
        "--start-frame",
        required=True,
        type=int,
    )
    source_set_parser.add_argument(
        "--end-frame",
        type=int,
        default=None,
    )

    return parser



def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "convert":
        shot_config = ShotConfig(
            image_width=args.width,
            image_height=args.height,
            production_start_frame=args.start_frame,
            production_end_frame=args.end_frame,
            source_software=args.source,
            target_software=args.target,
        )

        convert_file(
            args.input,
            args.output,
            shot_config,
            pftrack_source_role=args.pftrack_source_role,
        )

        return 0

    if args.command == "convert-pftrack-source-set":
        shot_config = ShotConfig(
            image_width=args.width,
            image_height=args.height,
            production_start_frame=args.start_frame,
            production_end_frame=args.end_frame,
            source_software=SOFTWARE_PFTRACK_2017,
            target_software=args.target,
        )

        convert_pftrack_source_set_files(
            args.autotrack_input,
            args.usertrack_input,
            args.output,
            shot_config,
        )

        return 0

    raise ValueError(
        f"Unsupported command: {args.command}"
    )
