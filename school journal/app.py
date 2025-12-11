# app.py

from flask import Flask, render_template, request, redirect, url_for, abort
import json
from models import Student, Subject, Grade

# --- Инициализация приложения и создание данных-примеров ---

app = Flask(__name__)

# Создадим несколько предметов (в реальном приложении они бы хранились в базе данных)
math = Subject("Математика", "fa-solid fa-calculator")
literature = Subject("Литература", "fa-solid fa-book-open")
physics = Subject("Физика", "fa-solid fa-atom")
history = Subject("История", "fa-solid fa-landmark")
ALL_SUBJECTS = [math, literature, physics, history]

DATA_FILE = 'data.json'

def load_data():
    """Загружает данные учеников из JSON файла."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f) # Пытаемся загрузить данные
            if not data: # Если файл пуст, вызываем ошибку, чтобы создать данные по умолчанию
                raise FileNotFoundError
            students = [Student.from_dict(s_data, ALL_SUBJECTS) for s_data in data]
            return {s.id: s for s in students}
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или пуст/некорректен, создаем полный список учеников
        student1 = Student("Алишер Абдықасым")
        student1.add_grade(Grade(5, math))
        student2 = Student("Мария Сидорова")
        student2.add_grade(Grade(4, physics))
        student3 = Student("Айзере Ким")
        student3.add_grade(Grade(5, literature))
        student4 = Student("Нурсултан Омаров")
        student4.add_grade(Grade(3, physics))
        student5 = Student("Дильназ Ахметова")
        student6 = Student("Санжар Болатов")
        student6.add_grade(Grade(5, math))

        default_students = {s.id: s for s in [student1, student2, student3, student4, student5, student6]}
        # Сохраняем созданный список в файл
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            student_list = [s.to_dict() for s in default_students.values()]
            json.dump(student_list, f, ensure_ascii=False, indent=4)
        return default_students

def save_data():
    """Сохраняет данные учеников в JSON файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        student_list = [s.to_dict() for s in STUDENTS_DB.values()]
        json.dump(student_list, f, ensure_ascii=False, indent=4)

# Наша "база данных" учеников, загружаемая из файла
STUDENTS_DB = load_data()

# --- Определение маршрутов (страниц сайта) ---

@app.route('/')
def index():
    """Главная страница со списком всех учеников."""
    students = list(STUDENTS_DB.values())
    return render_template('index.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Страница для добавления нового ученика."""
    if request.method == 'POST':
        student_name = request.form.get('name')
        if student_name:
            new_student = Student(student_name)
            STUDENTS_DB[new_student.id] = new_student
            save_data()
        return redirect(url_for('index'))
    return render_template('add_student.html')


@app.route('/student/<int:student_id>')
def student_details(student_id):
    """Страница с детальной информацией об ученике."""
    student = STUDENTS_DB.get(student_id)
    if not student:
        abort(404, description="Ученик с таким ID не найден.")
    return render_template('student.html', student=student, subjects=ALL_SUBJECTS)


@app.route('/student/<int:student_id>/add_grade', methods=['POST'])
def add_grade(student_id):
    """Обработчик для добавления новой оценки."""
    student = STUDENTS_DB.get(student_id)
    if not student:
        abort(404, description="Ученик с таким ID не найден.")

    # Получаем данные из формы
    subject_name = request.form.get('subject')
    grade_value = request.form.get('grade')

    # Находим объект предмета по его имени
    subject = next((s for s in ALL_SUBJECTS if s.name == subject_name), None)

    if subject and grade_value:
        new_grade = Grade(int(grade_value), subject)
        student.add_grade(new_grade)
        save_data()

    return redirect(url_for('student_details', student_id=student.id))


@app.route('/student/<int:student_id>/delete', methods=['DELETE'])
def delete_student(student_id):
    """Удаляет ученика."""
    if student_id in STUDENTS_DB:
        del STUDENTS_DB[student_id]
        save_data()
    return redirect(url_for('index'))


@app.route('/student/<int:student_id>/report')
def generate_report(student_id):
    """Страница с отчетом для родителей."""
    student = STUDENTS_DB.get(student_id)
    if not student:
        abort(404, description="Ученик с таким ID не найден.")
    return render_template('report.html', student=student)


if __name__ == '__main__':
    # Запуск веб-сервера для разработки
    app.run(debug=True)
