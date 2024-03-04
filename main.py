class Student:
    def __init__(self, name: str, marks: list[int]):
        self._name = name
        self._marks = marks

    def get_marks(self) -> list[int]:
        return self._marks

    def add_mark(self, mark: int):
        self._marks.append(mark)

    def avg_mark(self):
        return sum(self._marks) / len(self._marks)

    def __str__(self):
        return f'{self._name}'

    def __gt__(self, other):
        return self.avg_mark() > other.avg_mark()

    def __lt__(self, other):
        return self.avg_mark() < other.avg_mark()


class Group:
    def __init__(self, students: list[Student] | None = None):
        if students is None:
            self._students = []
        else:
            self._students = students

    def __iter__(self):
        return iter(self._students)

    def __len__(self):
        return len(self._students)

    def __contains__(self, student: str):
        return student in map(lambda x: str(x), self._students)

    def avg_mark(self):
        marks = []
        for student in self._students:
            marks += student.get_marks()
        return sum(marks) / len(marks)


s1 = Student('John', [5, 5, 5, 5])
s2 = Student('Michael', [3, 4, 5])
s3 = Student('Joe', [4, 3, 4])
s4 = Student('Jason', [2, 3, 2, 4])
s5 = Student('Patrik', [3, 4, 2])
s6 = Student('Viktor', [4, 5, 4])
g = Group([s1, s2, s3])
print(g.avg_mark())
sorted_g = sorted(g, lambda x: x.avgm_marks())
# class Dollar:
#     def __init__(self, dollars: int, cents: int):
#         self._dollars = dollars
#         self._cents = cents
#
#     def __str__(self):
#         str_cents = str(self._cents) \
#             if self._cents >= 10 else (
#                 "0" + str(self._cents))
#         return f'{self._dollars}.{str_cents}'
#
#     def __add__(self, another_dollar):
#         if isinstance(another_dollar, Dollar):
#             dollars = self._dollars + another_dollar._dollars
#             cents = self._cents + another_dollar._cents
#             return Dollar(dollars, cents)
#         elif isinstance(another_dollar, int):
#             dollars = self._dollars + another_dollar
#             return Dollar(dollars, self._cents)
#         else:
#             return super().__add__(another_dollar)
#
#     def __radd__(self, another_dollar):
#         return self.__add__(another_dollar)
#
#     def __sub__(self, another_dollar: "Dollar"):
#         dollars = self._dollars - another_dollar._dollars
#         cents = self._cents - another_dollar._cents
#         return Dollar(dollars, cents)
#
#
# d = Dollar(100, 32)
# d2 = Dollar(1, 23)
# d3 = Dollar(100, 4)
# lst = [d, d2, d3]
# print(sum(lst))
