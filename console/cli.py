from core.cli import CLI
from core.models import Point
from core.utils import segment_intersection


class ConsoleCLI(CLI):
    def present(slef, points):
        p1, q1, p2, q2 = points
        result = segment_intersection(p1, q1, p2, q2)

        if result is None:
            # Brak przecięcia odcinków
            print("NIE")
        elif isinstance(result, Point):
            # Przecięcie w pojedynczym punkcie
            print("TAK")
            print(f"Punkt przecięcia: ({result.x:.10g}, {result.y:.10g})")
        else:
            # Przecięcie jako wspólny fragment (odcinek)
            a, b = result
            print("TAK")
            print(
                "Odcinek przecięcia: ("
                f"({a.x:.10g}, {a.y:.10g}) – "
                f"({b.x:.10g}, {b.y:.10g}))"
            )
