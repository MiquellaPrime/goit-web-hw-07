import random

from faker import Faker
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import GradeORM, GroupORM, StudentORM, SubjectORM, TeacherORM


def populate_db(session: Session):
    fake_data = Faker()

    # Додавання груп
    group_names = ['Group A', 'Group B', 'Group C']
    groups = [GroupORM(name=name) for name in group_names]
    session.add_all(groups)

    # Додавання викладачів
    teachers = [
        TeacherORM(full_name=fake_data.name())
        for _ in range(random.randint(3, 5))
    ]
    session.add_all(teachers)

    session.flush()  # Присвоєння ID для груп та викладачів

    # Отримання ID викладачів
    teacher_ids = [teacher.id for teacher in teachers]

    # Додавання предметів
    subject_names = ['Math', 'Physics', 'History', 'Biology', 'Literature', 'Chemistry', 'Art', 'Philosophy']
    random_subjects = random.sample(subject_names, random.randint(5, 8))
    subjects = [
        SubjectORM(name=name, teacher_id=random.choice(teacher_ids))
        for name in random_subjects
    ]
    session.add_all(subjects)

    # Отримання ID груп
    group_ids = [group.id for group in groups]

    # Додавання студентів
    students = [
        StudentORM(full_name=fake_data.name(), group_id=random.choice(group_ids))
        for _ in range(random.randint(30, 50))
    ]
    session.add_all(students)

    session.flush()  # Присвоєння ID для предметів та студентів

    # Отримання ID студентів
    student_ids = [student.id for student in students]

    # Отримання ID предметів
    subject_ids = [subject.id for subject in subjects]

    # Додавання оцінок
    """
    Щоб уникнути надмірної кількості оцінок з одного предмета для окремого студента,
    я обмежив генерацію таким чином: кожен студент отримує по 1–3 оцінки з випадкових 4 або більше предметів.
    Це дозволяє рівномірніше розподілити оцінки між предметами, при цьому загальна кількість оцінок на студента
    все одно відповідає умові — до 20 записів.
    """
    grades = []
    for student_id in student_ids:
        subjects_for_student = random.sample(subject_ids, random.randint(4, len(subject_ids)))
        for subject_id in subjects_for_student:
            for _ in range(random.randint(1, 3)):
                grade = random.randint(60, 100)
                graded_at = fake_data.date_between(start_date='-1y', end_date='today')
                grades.append(
                    GradeORM(student_id=student_id, subject_id=subject_id, grade=grade, graded_at=graded_at)
                )

    session.add_all(grades)

    session.commit()


if __name__ == '__main__':
    with get_db() as db:
        populate_db(db)
    print("Database successfully seeded with random data.")
