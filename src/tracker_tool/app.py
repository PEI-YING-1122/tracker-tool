"""File-level conversion shared by the CLI and the GUI.

Reads native text, runs the Core conversion, and writes the target text
only after the conversion has succeeded. The behaviour is the released
v1.0.1 CLI file handling (docs/INTERCHANGE_MASTER.md, "CLI Contract"):

- an output path that resolves to an input path is rejected before any
  file is read or written
- input is read as UTF-8 text
- output is written as UTF-8 text in text mode (platform newlines)
- on failure no output is created and an existing output is untouched
"""

from pathlib import Path

from tracker_tool.config import ShotConfig
from tracker_tool.conversion import (
    convert_pftrack_source_set,
    convert_tracks,
)


def convert_file(
    input_path,
    output_path,
    shot_config: ShotConfig,
    *,
    pftrack_source_role: str | None = None,
) -> None:
    input_path = Path(input_path)
    output_path = Path(output_path)

    if input_path.resolve() == output_path.resolve():
        raise ValueError(
            "Input and output paths must be different"
        )

    native_text = input_path.read_text(
        encoding="utf-8",
    )

    output_text = convert_tracks(
        native_text,
        shot_config,
        pftrack_source_role=pftrack_source_role,
    )

    output_path.write_text(
        output_text,
        encoding="utf-8",
    )


def convert_pftrack_source_set_files(
    autotrack_path,
    usertrack_path,
    output_path,
    shot_config: ShotConfig,
) -> None:
    autotrack_path = Path(autotrack_path)
    usertrack_path = Path(usertrack_path)
    output_path = Path(output_path)

    if (
        output_path.resolve()
        == autotrack_path.resolve()
        or output_path.resolve()
        == usertrack_path.resolve()
    ):
        raise ValueError(
            "Input and output paths must be different"
        )

    autotrack_text = autotrack_path.read_text(
        encoding="utf-8",
    )
    usertrack_text = usertrack_path.read_text(
        encoding="utf-8",
    )

    output_text = convert_pftrack_source_set(
        autotrack_text,
        usertrack_text,
        shot_config,
    )

    output_path.write_text(
        output_text,
        encoding="utf-8",
    )
