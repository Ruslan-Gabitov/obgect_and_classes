class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


class Lecturer(Mentor):
    _lecturers = []
    _overall_assessment = 0
    _number_of_ratings = 0

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.courses_attached = []
        Lecturer._lecturers.append(self)

    def get_average_score(self):
        for _assessment in self.grades.values():
            self._overall_assessment += sum(_assessment)
            self._number_of_ratings += len(_assessment)
        return f'Средний бал {round(self._overall_assessment / self._number_of_ratings, 1)}'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредний балл за лекции: {self.get_average_score()}'

    def __lt__(self, other):
        if isinstance(other, Student):
            if self.get_average_score() > other.get_average_score():
                return 'Нет, у лектора балл выше чем у студента!'
            else:
                return 'У студента балл выше чем у лектора!'
        else:
            return 'Ошибка, но лектор всеровно круче!'


class Student(Lecturer):
    _students = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student._students.append(self)

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредний балл за домашние задания: {self.get_average_score()}\nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}\nЗавершенные курсы: {", ".join(self.finished_courses)}'


class Reviewer(Mentor):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def average_students_score(course, students):
    total_balls = 0
    students_on_course = 0
    for student in students:
        if course in student.courses_in_progress:
            total_balls += sum(student.grades[course])
            students_on_course += 1
    return f'Курс: {course}\nКоличесво студентов на крусе: {students_on_course}\nСреднее количесвто баллов всех студентов по курсу: {round(total_balls / students_on_course, 1)}'


def average_lecturers_score(course, lecturers):
    total_balls = 0
    lecturers_on_course = 0
    for lecturer in lecturers:
        if course in lecturer.courses_attached:
            total_balls += sum(lecturer.grades[course])
            lecturers_on_course += 1
    return f'Курс: {course}\nКоличесво лектров на крусе: {lecturers_on_course}\nСреднее количесвто баллов всех лекторов по курсу: {round(total_balls / lecturers_on_course, 1)}'


mentor = Mentor('kay', 'lop')

lector_1 = Lecturer('Bob', 'Gef')
lector_1.courses_attached = ['Python', 'Get']

lector_2 = Lecturer('Don', 'Gon')
lector_2.courses_attached = ['Java', 'Ruby', 'Python']

reviewer_1 = Reviewer('Jack', 'Pol')
reviewer_1.courses_attached = ['Python', 'Get']

reviewer_2 = Reviewer('Jack', 'Pol')
reviewer_2.courses_attached = ['Java', 'Ruby']

best_student_1 = Student('Jon', 'lit', 'gender')
best_student_1.courses_in_progress += ['Get', 'Python', 'Java']
best_student_1.finished_courses += ['Java', 'Повар-крндитер']
best_student_1.rate_hw(lector_1, 'Python', 8)
best_student_1.rate_hw(lector_2, 'Java', 6)

best_student_2 = Student('Tony', 'Stark', 'gender')
best_student_2.courses_in_progress += ['Python', 'Get', 'Ruby']
best_student_2.finished_courses += ['Java', 'Повар-крндитер']
best_student_2.rate_hw(lector_2, 'Python', 7)
best_student_2.rate_hw(lector_2, 'Ruby', 7)

reviewer_1.rate_hw(best_student_1, 'Python', 10)
reviewer_1.rate_hw(best_student_1, 'Get', 4)

reviewer_1.rate_hw(best_student_2, 'Python', 10)
reviewer_1.rate_hw(best_student_2, 'Get', 4)

reviewer_2.rate_hw(best_student_1, 'Java', 8)
reviewer_2.rate_hw(best_student_2, 'Ruby', 7)

print(lector_1 < best_student_1)

print(lector_1.get_average_score())
print(best_student_1.get_average_score())

print(average_students_score('Python', Student._students))
print(average_students_score('Java', Student._students))
print(average_students_score('Ruby', Student._students))
print(average_students_score('Get', Student._students))

print(average_lecturers_score('Python', Lecturer._lecturers))
print(average_lecturers_score('Java', Lecturer._lecturers))
print(average_lecturers_score('Ruby', Lecturer._lecturers))