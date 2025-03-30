from dataclasses import dataclass


@dataclass
class MoistureDto:
    plant: str
    moisture: float


@dataclass
class Moisture:
    plant: str
    moisture: float
    date: str
