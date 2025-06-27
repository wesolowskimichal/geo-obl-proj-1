from .models import Point
from .constants import EPS
from typing import Optional, Tuple, Union
import math


def orientation(a: Point, b: Point, c: Point) -> int:
    # Oblicza orientację trójki punktów (a, b, c)
    # Zwraca:
    #   0 – punkty współliniowe
    #   1 – skręt w prawo
    #  -1 – skręt w lewo
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if abs(val) <= EPS:
        return 0
    return 1 if val > 0 else -1


def on_segment(a: Point, b: Point, c: Point) -> bool:
    # Sprawdza, czy punkt `b` leży na odcinku `ac`, z uwzględnieniem błędu EPS
    return (
        min(a.x, c.x) - EPS <= b.x <= max(a.x, c.x) + EPS
        and min(a.y, c.y) - EPS <= b.y <= max(a.y, c.y) + EPS
    )


def line_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Point:
    # Oblicza punkt przecięcia dwóch prostych przechodzących przez (p1, p2) i (p3, p4)
    # Jeśli proste są równoległe (wyznacznik bliski zeru), rzuca wyjątek
    a1 = p2.y - p1.y
    b1 = p1.x - p2.x
    c1 = a1 * p1.x + b1 * p1.y

    a2 = p4.y - p3.y
    b2 = p3.x - p4.x
    c2 = a2 * p3.x + b2 * p3.y

    det = a1 * b2 - a2 * b1
    if abs(det) <= EPS:
        raise ValueError("Lines are parallel – no unique intersection.")

    x = (b2 * c1 - b1 * c2) / det
    y = (a1 * c2 - a2 * c1) / det
    return Point(x, y)


def segment_intersection(
    p1: Point, q1: Point, p2: Point, q2: Point
) -> Optional[Union[Point, Tuple[Point, Point]]]:
    # Sprawdza przecięcie dwóch odcinków: (p1–q1) i (p2–q2)
    # Zwraca:
    #   - Point, jeśli jest dokładnie jeden punkt przecięcia
    #   - (Point, Point), jeśli odcinki nachodzą się (część wspólna)
    #   - None, jeśli brak przecięcia

    o1, o2 = orientation(p1, q1, p2), orientation(p1, q1, q2)
    o3, o4 = orientation(p2, q2, p1), orientation(p2, q2, q1)

    # Przypadek przecięcia „ogólnego” – skrzyżowanie się odcinków
    if o1 != o2 and o3 != o4:
        return line_intersection(p1, q1, p2, q2)

    def _collect() -> list[Point]:
        # Zbiera punkty wspólne leżące na obu odcinkach
        pts: list[Point] = []
        for P in (p1, q1, p2, q2):
            if on_segment(p1, P, q1) and on_segment(p2, P, q2):
                pts.append(P)

        # Usunięcie punktów powtarzających się (z dokładnością do EPS)
        uniq: list[Point] = []
        for pt in pts:
            if not any(math.hypot(pt.x - u.x, pt.y - u.y) <= EPS for u in uniq):
                uniq.append(pt)
        return uniq

    # Przypadek współliniowy – sprawdzanie nałożonych fragmentów
    if o1 == o2 == o3 == o4 == 0:
        common = sorted(_collect(), key=lambda pt: (pt.x, pt.y))
        if not common:
            return None
        if len(common) == 1:
            return common[0]
        return common[0], common[-1]

    # Sprawdzenie przypadków krawędziowych – jednoznacznie wspólne końce
    for a, b, c in ((p1, p2, q2), (p1, q1, p2), (p2, p1, q1), (p2, q2, p1)):
        if orientation(a, b, c) == 0 and on_segment(a, b, c):
            return b

    return None
