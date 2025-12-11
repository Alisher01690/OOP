# models.py

class Subject:
    """Класс для представления учебного предмета."""
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon

    def __repr__(self):
        return f"<Subject: {self.name}>"

    def to_dict(self):
        return {'name': self.name, 'icon': self.icon}

    @staticmethod
    def from_dict(data, all_subjects):
        return next((s for s in all_subjects if s.name == data['name']), None)


class Grade:
    """Класс для представления оценки."""
    def __init__(self, value, subject: Subject):
        if not isinstance(subject, Subject):
            raise TypeError("Предмет должен быть объектом класса Subject")
        self.value = value
        self.subject = subject

    def __repr__(self):
        return f"<Grade: {self.value} for {self.subject.name}>"

    def to_dict(self):
        return {'value': self.value, 'subject': self.subject.name}

    @staticmethod
    def from_dict(data, all_subjects):
        subject_name = data['subject']
        subject = next((s for s in all_subjects if s.name == subject_name), None)
        if subject:
            return Grade(data['value'], subject)
        return None


class Student:
    """Класс для представления ученика."""
    _id_counter = 0

    def __init__(self, name):
        # Генерация уникального ID для каждого ученика
        Student._id_counter += 1
        self.id = Student._id_counter
        self.name = name
        self.grades = []

    def add_grade(self, grade: Grade):
        """Добавляет оценку ученику."""
        if not isinstance(grade, Grade):
            raise TypeError("Оценка должна быть объектом класса Grade")
        self.grades.append(grade)

    def get_average_grade(self):
        """Рассчитывает средний балл ученика."""
        if not self.grades:
            return 0.0
        return sum(g.value for g in self.grades) / len(self.grades)

    def __repr__(self):
        return f"<Student ID {self.id}: {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'grades': [g.to_dict() for g in self.grades]
        }

    @staticmethod
    def from_dict(data, all_subjects):
        student = Student(data['name'])
        student.id = data['id']
        # Фильтруем None значения, если оценка не может быть создана
        student.grades = [grade for g_data in data['grades'] if (grade := Grade.from_dict(g_data, all_subjects)) is not None]
        # Устанавливаем счетчик ID, чтобы избежать дубликатов
        Student._id_counter = max(Student._id_counter, student.id)
        return student
