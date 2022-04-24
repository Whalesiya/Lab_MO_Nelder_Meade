import random
from typing import Optional


class Vector:
    x: float = 0
    y: float = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({round(self.x, 4)}, {round(self.y, 4)})'

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        return Vector(x, y)

    def __rmul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x, y)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x, y)


def area(point1: Vector,
         point2: Vector,
         point3: Vector) -> float:

    if point1 == point2 or point2 == point3 or point1 == point3:
        return 0.0

    vector1 = point2 - point3
    vector2 = point3 - point1

    return abs(0.5 * (vector1.x * vector2.y - vector1.y * vector2.x))


def func_r(v: Vector) -> float:
    # Rosenbrock_function
    return (1 - v.x) ** 2 + 100 * (v.y - v.x ** 2) ** 2


def nelder_meade(func,
                 point1: Vector,
                 point2: Vector,
                 point3: Vector,
                 alpha: float = 1.0,
                 beta: float = 2.0,
                 gamma: float = - 0.5,
                 delta: float = 0.5,
                 iters: int = 10000,
                 min_area: float = 1e-10,
                 precision: float = 1e-10,
                 ) -> (Optional[Vector], Optional[int]):

    global i

    if area(point1, point2, point3) < min_area:
        print('\n\tВы ввели три точки на одной прямой!')
        return None, None

    best_point, good_point, worst_point = point1, point2, point3

    points = [[p, func(p)] for p in [best_point, good_point, worst_point]]
    points.sort(key=lambda x: x[1])
    best_point, good_point, worst_point = (_[0] for _ in points)

    cur_worst_f = func(worst_point)

    for i in range(iters):

        prev_worst_f = cur_worst_f

        mid_point = (best_point + good_point) / 2
        point_reflection = mid_point + alpha * (mid_point - worst_point)
        if func(point_reflection) < func(good_point):
            worst_point = point_reflection
            point_expansion = mid_point + beta * (mid_point - worst_point)
            if func(point_expansion) < func(best_point):
                good_point = point_expansion
        else:
            if func(point_reflection) < func(worst_point):
                worst_point = point_reflection
            point_contraction = mid_point + gamma * (mid_point - worst_point)
            if func(point_contraction) < func(worst_point):
                worst_point = point_contraction
            else:
                good_point = best_point + delta * (good_point - best_point)
                worst_point = best_point + delta * (worst_point - best_point)

        points = [[p, func(p)] for p in [best_point, good_point, worst_point]]
        points.sort(key=lambda x: x[1])
        best_point, good_point, worst_point = (_[0] for _ in points)

        cur_worst_f = func(worst_point)

        area_break = area(best_point, good_point, worst_point)
        precision_break = abs(cur_worst_f - prev_worst_f)
        if area_break < min_area or precision_break < precision:
            break

    return best_point, i


print('\n\t\t ~ Реализация метода Нелдера-Мида ~ ')
print('_'*60)

yn = int(input('\nЗадать три начальные точки самостоятельно? да-1 нет-0\t->\t'))

if yn == 1:

    print('\n\tВведите координаты трёх начальных точек через пробел: \n')

    a, b = map(int, input('\tКоординаты первой точки: ').split())
    point_1 = Vector(a, b)

    a, b = map(int, input('\tКоординаты второй точки: ').split())
    point_2 = Vector(a, b)

    a, b = map(int, input('\tКоординаты третьей точки: ').split())
    point_3 = Vector(a, b)
else:
    point_1 = Vector(random.randint(-10, 10), random.randint(-10, 10))
    point_2 = Vector(random.randint(-10, 10), random.randint(-10, 10))
    point_3 = Vector(random.randint(-10, 10), random.randint(-10, 10))

min_point, iteration = nelder_meade(func=func_r,
                                    point1=point_1,
                                    point2=point_2,
                                    point3=point_3)
if iteration is not None:
    print('\n\tАлгоритм выполняется ...\n')
    print('_'*60)
    print('Алгоритм выполнился', iteration, 'раз')
    print('Минимум функции в точке (x, y) = ', min_point)
    print('Значение функции F(x, y) = ', round(func_r(min_point), 6))
    print('_'*60)
