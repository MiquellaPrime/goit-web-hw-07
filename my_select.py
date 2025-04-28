from sqlalchemy import select, func, desc, and_
from sqlalchemy.orm import Session, aliased

from src.database import get_db
from src.models import GradeORM, GroupORM, StudentORM, SubjectORM, TeacherORM


def select_1(session: Session):
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    stmt = (
        select(
            StudentORM.full_name.label("student"),
            func.round(func.avg(GradeORM.grade), 2).label("avg_grade"),
        )
        .select_from(GradeORM)
        .join(StudentORM)
        .group_by(StudentORM.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(stmt).mappings().all()


def select_2(session: Session, subject_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    stmt = (
        select(
            SubjectORM.name.label("subject"),
            StudentORM.full_name.label("student"),
            func.round(func.avg(GradeORM.grade), 2).label("avg_grade"),
        )
        .select_from(GradeORM)
        .join(SubjectORM)
        .join(StudentORM)
        .where(GradeORM.subject_id == subject_id)
        .group_by(GradeORM.subject_id, GradeORM.student_id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    return session.execute(stmt).mappings().all()


def select_3(session: Session, subject_id: int):
    """Знайти середній бал у групах з певного предмета."""
    stmt = (
        select(
            SubjectORM.name.label("subject"),
            GroupORM.name.label("group"),
            func.round(func.avg(GradeORM.grade), 2).label("avg_grade"),
        )
        .select_from(GradeORM)
        .join(SubjectORM)
        .join(StudentORM)
        .join(GroupORM)
        .where(GradeORM.subject_id == subject_id)
        .group_by(GroupORM.name)
    )
    return session.execute(stmt).mappings().all()


def select_4(session: Session):
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    stmt = select(func.round(func.avg(GradeORM.grade), 2).label("avg_grade")).select_from(GradeORM)
    return session.execute(stmt).mappings()


def select_5(session: Session, teacher_id: int):
    """Знайти які курси читає певний викладач."""
    stmt = (
        select(
            TeacherORM.full_name.label("teacher"),
            SubjectORM.name.label("subject"),
        )
        .select_from(SubjectORM)
        .join(TeacherORM)
        .where(SubjectORM.teacher_id == teacher_id)
        .order_by(SubjectORM.name)
    )
    return session.execute(stmt).mappings().all()


def select_6(session: Session, grade_id: int):
    """Знайти список студентів у певній групі."""
    stmt = (
        select(
            GroupORM.name.label("group"),
            StudentORM.full_name.label("student"),
        )
        .select_from(StudentORM)
        .join(GroupORM)
        .where(GroupORM.id == grade_id)
        .order_by(StudentORM.full_name)
    )
    return session.execute(stmt).mappings().all()


def select_7(session: Session, group_id: int, subject_id: int):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    stmt = (
        select(
            SubjectORM.name.label("subject"),
            GroupORM.name.label("group"),
            StudentORM.full_name.label("student"),
            GradeORM.grade,
            GradeORM.graded_at,
        )
        .select_from(StudentORM)
        .join(GroupORM)
        .join(GradeORM)
        .join(SubjectORM)
        .where(and_(
            StudentORM.group_id == group_id,
            SubjectORM.id == subject_id,
        ))
        .order_by(StudentORM.full_name, GradeORM.graded_at)
    )
    return session.execute(stmt).mappings().all()


def select_8(session: Session, teacher_id: int):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    stmt = (
        select(
            TeacherORM.full_name.label("teacher"),
            SubjectORM.name.label("subject"),
            func.round(func.avg(GradeORM.grade), 2).label("avg_grade"),
        )
        .select_from(GradeORM)
        .join(SubjectORM)
        .join(TeacherORM)
        .where(TeacherORM.id == teacher_id)
        .group_by(SubjectORM.name)
    )
    return session.execute(stmt).mappings().all()


def select_9(session: Session, student_id: int):
    """Знайти список курсів, які відвідує певний студент."""
    stmt = (
        select(
            StudentORM.full_name.label("student"),
            SubjectORM.name.label("subject"),
        )
        .select_from(StudentORM)
        .join(GradeORM)
        .join(SubjectORM)
        .where(StudentORM.id == student_id)
        .group_by(SubjectORM.name)
    )
    return session.execute(stmt).mappings().all()


def select_10(session: Session, student_id: int, teacher_id: int):
    """Список курсів, які певному студенту читає певний викладач."""
    stmt = (
        select(
            StudentORM.full_name.label("student"),
            TeacherORM.full_name.label("teacher"),
            SubjectORM.name.label("subject"),
        )
        .select_from(GradeORM)
        .join(StudentORM)
        .join(SubjectORM)
        .join(TeacherORM)
        .where(and_(
            GradeORM.student_id == student_id,
            TeacherORM.id == teacher_id,
        ))
        .group_by(SubjectORM.name)
    )
    return session.execute(stmt).mappings().all()


def select_11(session: Session, student_id: int, teacher_id: int):
    """Середній бал, який певний викладач ставить певному студентові."""
    stmt = (
        select(
            StudentORM.full_name.label("student"),
            TeacherORM.full_name.label("teacher"),
            SubjectORM.name.label("subject"),
            func.round(func.avg(GradeORM.grade), 2).label("avg_grade"),
        )
        .select_from(GradeORM)
        .join(StudentORM)
        .join(SubjectORM)
        .join(TeacherORM)
        .where(and_(
            GradeORM.student_id == student_id,
            TeacherORM.id == teacher_id,
        ))
        .group_by(SubjectORM.name)
    )
    return session.execute(stmt).mappings().all()


def select_12(session: Session, group_id: int, subject_id: int):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    AliasGradeORM = aliased(GradeORM)  # Аліас, необхідний для підзапиту

    subq = (
        select(func.max(AliasGradeORM.graded_at))
        .where(and_(
            AliasGradeORM.student_id == GradeORM.student_id,
            AliasGradeORM.subject_id == GradeORM.subject_id,
        ))
        .scalar_subquery()
    )

    stmt = (
        select(
            SubjectORM.name.label("subject"),
            GroupORM.name.label("group"),
            StudentORM.full_name.label("student"),
            GradeORM.grade,
            GradeORM.graded_at,
        )
        .select_from(GradeORM)
        .join(SubjectORM)
        .join(StudentORM)
        .join(GroupORM)
        .where(and_(
            StudentORM.group_id == group_id,
            GradeORM.subject_id == subject_id,
            GradeORM.graded_at == subq
        ))
        .order_by(StudentORM.full_name)
    )
    return session.execute(stmt).mappings().all()


if __name__ == '__main__':
    with get_db() as db:
        for row in select_12(db, 2, 4):
            print(row)
