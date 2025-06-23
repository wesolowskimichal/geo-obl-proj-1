import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


HERE = Path(__file__).resolve().parent
REQ_FILE = HERE / "visualisation" / "requirements.txt"


def _run_console(argv: Optional[List[str]]) -> None:
    from console.main import main as console_main

    console_main(argv)


def _install_visualisation_deps() -> None:
    print("\n⏳  Instaluję zależności wizualizacji… (to potrwa chwilę)\n")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)]
        )
    except subprocess.CalledProcessError as exc:
        print(
            "\n❌  Instalacja zakończyła się niepowodzeniem.\n"
            "Możesz spróbować ręcznie:\n"
            f'    python -m pip install -r "{REQ_FILE}"\n'
        )
        raise SystemExit(1) from exc


def _run_visual(argv: Optional[List[str]]) -> None:
    try:
        from visualisation.main import main as visual_main
    except ImportError:
        print("⚠️  Biblioteka Matplotlib (lub inne zależności) nie jest zainstalowana.")
        choice = input(
            f"Czy chcesz zainstalować pakiety z {REQ_FILE.relative_to(HERE)}? [y/N] "
        ).strip()
        if choice.lower() != "y":
            print("Anulowano uruchamianie wizualizacji.")
            sys.exit(1)

        _install_visualisation_deps()

        try:
            from importlib import reload

            import visualisation.main

            visual_main = reload(visualisation.main).main
        except ImportError as err:
            print("\n❌  Coś wciąż nie działa – przerywam.")
            raise SystemExit(1) from err

    visual_main(argv)


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=Path(sys.argv[0]).name,
        description="Segment-intersection project – choose CLI or visual mode.",
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    for name, help_txt in (
        ("cli", "Run console (text) version"),
        ("viz", "Run visual (matplotlib) version"),
    ):
        p = sub.add_parser(name, help=help_txt)
        p.add_argument("coords", nargs="*", help="x1 y1 x2 y2 x3 y3 x4 y4")

    return parser


def main() -> None:
    parser = build_argparser()
    ns = parser.parse_args()
    argv = ns.coords or None

    if ns.mode == "cli":
        _run_console(argv)
    elif ns.mode == "viz":
        _run_visual(argv)
    else:
        parser.error(f"Unknown mode {ns.mode!r}")


if __name__ == "__main__":
    main()
