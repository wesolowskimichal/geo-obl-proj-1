from .cli import ConsoleCLI


def main(argv: list[str] | None = None) -> None:
    parser = ConsoleCLI(
        description="Check intersection of two planar segments.",
        epilog="© 2025 Geometry Calculus Project",
    )

    points = parser.prompt_coords(argv)
    parser.present(points)


if __name__ == "__main__":
    main()
