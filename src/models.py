from datetime import datetime

from sqlalchemy import (
    Column, ForeignKey,
    Integer, String, Date
)
from sqlalchemy.orm import declarative_base, relationship

from .database import engine
from .settings import settings

Base = declarative_base()


class GroupORM(Base):
    __tablename__ = "groups"

    id   = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, nullable=False)

    students = relationship("StudentORM", backref="group")


class StudentORM(Base):
    __tablename__ = "students"

    id        = Column(Integer, primary_key=True)
    full_name = Column(String(30), nullable=False)
    group_id  = Column(Integer, ForeignKey("groups.id"))

    grades = relationship("GradeORM", backref="student")


class TeacherORM(Base):
    __tablename__ = "teachers"

    id        = Column(Integer, primary_key=True)
    full_name = Column(String(30), nullable=False)

    subjects = relationship("SubjectORM", backref="teacher")


class SubjectORM(Base):
    __tablename__ = "subjects"

    id         = Column(Integer, primary_key=True)
    name       = Column(String(15), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    grades = relationship("GradeORM", backref="subject")


class GradeORM(Base):
    __tablename__ = "grades"

    id         = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    grade      = Column(Integer)
    graded_at  = Column(Date, default=datetime.today)


if settings.IS_DEV:
    Base.metadata.create_all(bind=engine)
