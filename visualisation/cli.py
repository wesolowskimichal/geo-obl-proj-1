from core.cli import CLI
from core.utils import segment_intersection

import matplotlib.pyplot as plt

from core.models import Point


class VisualisationCLI(CLI):
    def present(self, points):
        p1, q1, p2, q2 = points
        result = segment_intersection(p1, q1, p2, q2)

        _, ax = plt.subplots()
        # Rysowanie obu odcinków: pierwszy na niebiesko, drugi na zielono
        self._draw_segment(ax, p1, q1, style="b-")
        self._draw_segment(ax, p2, q2, style="g-")

        if result is None:
            # Brak przecięcia – tylko odcinki i komunikat
            title = "Odcinki się nie przecinają"
        elif isinstance(result, Point):
            # Przecięcie w jednym punkcie – zaznaczenie go i opis
            ax.scatter(result.x, result.y, marker="o", s=100, zorder=5)
            title = f"Punkt przecięcia: ({result.x:.4g}, {result.y:.4g})"
        else:
            # Przecięcie jako wspólny fragment – rysowanie go na czerwono
            a, b = result
            self._draw_segment(ax, a, b, style="r-")
            title = (
                "Odcinki nakładają się\n"
                f"Początek: ({a.x:.4g}, {a.y:.4g}), "
                f"koniec: ({b.x:.4g}, {b.y:.4g})"
            )

        # Konfiguracja osi i wyświetlenie wykresu
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)
        ax.axis("equal")
        ax.grid(True)
        plt.show()

    def _draw_segment(self, ax, a: Point, b: Point, *, style: str = "-") -> None:
        # Pomocnicza funkcja do rysowania pojedynczego odcinka na wykresie
        ax.plot([a.x, b.x], [a.y, b.y], style, linewidth=2)
