from dataclasses import dataclass


@dataclass
class ShotConfig:
    image_width: int
    image_height: int
    production_start_frame: int
    production_end_frame: int | None
    source_software: str
    target_software: str