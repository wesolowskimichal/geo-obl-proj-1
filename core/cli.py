from abc import ABC, abstractmethod
import argparse
from typing import Sequence

from .models import Point


class CLI(ABC):
    parser: argparse.ArgumentParser

    def __init__(
        self,
        description: str,
        epilog: str = "",
    ):
        self.parser = argparse.ArgumentParser(description=description, epilog=epilog)
        self.parser.add_argument(
            "coords",
            metavar="N",
            nargs="*",
            help="x1 y1 x2 y2 x3 y3 x4 y4 – coordinates of the two segments",
        )

    def parse_args(self, argv: list[str] | None = None):
        return self.parser.parse_args(argv)

    def parse_coords(self, coords: Sequence[str]) -> list[Point]:
        try:
            nums = list(map(float, coords))
        except ValueError as exc:
            raise SystemExit(f"All coordinates must be numeric – {exc}") from exc
        if len(nums) != 8:
            raise SystemExit("Exactly 8 numeric coordinates are required.")
        return [Point(nums[i], nums[i + 1]) for i in range(0, 8, 2)]

    def prompt_coords(self, argv: list[str] | None = None) -> list[Point]:
        args = self.parse_args(argv)

        if args.coords:
            return self.parse_coords(args.coords)

        prompt = (
            "Enter coordinates for the segments (x y) in order: "
            "P1, Q1, P2, Q2, separated by spaces → "
        )
        try:
            nums = list(map(float, input(prompt).strip().split()))
        except ValueError:
            raise SystemExit("All coordinates must be numeric.")
        return self.parse_coords(list(map(str, nums)))

    @abstractmethod
    def present(slef, points: list[Point]) -> None:
        """Method to present the parsed coordinates or results."""
        ...
