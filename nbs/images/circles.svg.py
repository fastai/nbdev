"""---
---"""

# Original copyright 2022 Gram, MIT license; https://github.com/orsinium-labs/generative-art; Changes copyright Jeremy Howard

import math,svg
from random import randint,random,seed
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
    def distance_to(self, p):
        dx = abs(self.x - p.x)
        dy = abs(self.y - p.y)
        return math.sqrt(dx ** 2 + dy ** 2)


class Circle(NamedTuple):
    c: Point
    r: float
    def contains(self, point): return self.c.distance_to(point) <= self.r
    def min_distance(self, other): return abs(self.r - self.c.distance_to(other))
    def render(self, stroke= "none", fill= "none"):
        return svg.Circle( cx=self.c.x, cy=self.c.y, r=self.r, stroke=stroke, stroke_width=1, fill=fill,)


class Generator:
    size=800; min_shift=20; max_shift=60; min_width=20; min_circles=200; max_circles=300; min_radius=4
    def generate(self): return svg.SVG( width=self.size, height=self.size, xmlns='http://www.w3.org/2000/svg', elements=list(self.iter_elements()),)
    def color(self): return f'hsl({randint(0, 360)}, {randint(75, 100)}%, 50%)'

    def __init__(self):
        outer_r = self.size//2
        outer_center = Point(outer_r, outer_r)
        self.outer = Circle(c=outer_center, r=outer_r)

    def inner(self):
        inner_x = self.outer.r + randint(self.min_shift, self.max_shift)
        inner_y = self.outer.r + randint(self.min_shift, self.max_shift)
        inner_center = Point(inner_x, inner_y)
        r = self.outer.min_distance(inner_center) - self.min_width
        return Circle(c=inner_center, r=r)

    def iter_elements(self):
        assert self.inner().r < self.outer.r
        yield self.outer.render(fill="white")
        circles_count = randint(self.min_circles, self.max_circles)
        min_distance = math.ceil(self.inner().min_distance(Point(self.outer.r, self.outer.r)))
        circles = [self.inner()]
        for _ in range(circles_count):
            for _ in range(40):
                circle = self.get_random_circle(min_distance, circles)
                if circle is not None:
                    circles.append(circle)
                    yield circle.render(stroke=self.color())
                    break

    def get_random_circle( self, min_distance: int, circles: list[Circle],):
        distance = randint(min_distance, math.floor(self.outer.r))
        angle = random() * math.pi * 2
        cx = self.outer.r + math.cos(angle) * distance
        cy = self.outer.r + math.sin(angle) * distance
        center = Point(cx, cy)
        for other in circles:
            if other.contains(center): return None
        r = self.outer.min_distance(center)
        for other in circles: r = min(r, other.min_distance(center))
        if r < self.min_radius: return None
        return Circle(c=center, r=r)

seed(42)
print(Generator().generate())

