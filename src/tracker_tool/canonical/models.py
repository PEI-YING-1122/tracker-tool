from dataclasses import dataclass


@dataclass
class Observation:
    production_frame: int
    x_pixel: float
    y_pixel: float


@dataclass
class Track:
    track_id: str
    track_name: str
    observations: list[Observation]