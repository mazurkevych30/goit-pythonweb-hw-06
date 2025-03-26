from sqlalchemy import select, func, desc, cast, Integer
from sqlalchemy.orm import Session

from conf.db import SessionLocal
from entity.models import Student, Grade, Group, Teacher, Subject


def select_1(session: Session) -> list:
    query = (
        select(Student, cast(func.avg(Grade.grade).label("avg_grade"), Integer))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(query).all()


def select_2(session: Session, subject_id: int) -> list:
    query = (
        select(Student, cast(func.avg(Grade.grade).label("avg_grade"), Integer))
        .join(Grade)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
    )
    return session.execute(query).first()


def select_3(session: Session, subject_id: int) -> list:
    query = (
        select(Group.name, cast(func.avg(Grade.grade).label("avg_grade"), Integer))
        .join(Group.students)
        .join(Student.grades)
        .where(Grade.subject_id == subject_id)
        .group_by(Group.name)
        .order_by(Group.name)
    )
    return session.execute(query).all()


def select_4(session: Session) -> int:
    query = select(cast(func.avg(Grade.grade).label("avg_grade"), Integer))
    return session.execute(query).scalar()


def select_5(session: Session, teacher_id: int) -> list:
    query = (
        select(Teacher.id, Teacher.first_name, Teacher.second_name, Subject.name)
        .join(Subject.teacher)
        .where(Subject.teacher_id == teacher_id)
    )
    return session.execute(query).all()


def select_6(session: Session, group_id: int) -> list:
    query = select(Student).join(Student.group).where(Group.id == group_id)
    return session.execute(query).all()


def select_7(session: Session, group_id: int, subject_id: int) -> list:
    query = (
        select(Student.full_name, Grade.grade, Grade.date_received)
        .join(Group.students)
        .join(Student.grades)
        .where(Group.id == group_id, Grade.subject_id == subject_id)
    )
    return session.execute(query).all()


def select_8(session: Session, techer_id: int) -> list:
    query = (
        select(Subject.name, cast(func.avg(Grade.grade).label("avg_grade"), Integer))
        .join(Grade.subject)
        .where(Subject.teacher_id == techer_id)
        .group_by(Subject.name)
    )
    return session.execute(query).all()


def select_9(session: Session, student_id: int) -> list:
    query = (
        select(Subject.name)
        .join(Student.grades)
        .join(Grade.subject)
        .where(Student.id == student_id)
        .group_by(Subject.name)
    )
    return session.execute(query).all()


def select_10(session: Session, student_id: int, techer_id: int) -> list:
    query = (
        select(Subject.name)
        .join(Student.grades)
        .join(Grade.subject)
        .where(Student.id == student_id, Subject.teacher_id == techer_id)
        .group_by(Subject.name)
    )
    return session.execute(query).all()


def select_11(session: Session, student_id: int, teacher_id: int) -> float:
    query = (
        select(cast(func.avg(Grade.grade).label("avg_grade"), Integer))
        .join(Grade.subject)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
    )
    return session.execute(query).scalar()


def select_12(session: Session, group_id: int, subject_id: int):
    subq = (
        select(func.max(Grade.date_received).label("max_date"))
        .join(Student)
        .where(Grade.subject_id == subject_id, Student.group_id == group_id)
        .scalar_subquery()
    )
    query = (
        select(Student.full_name, Grade.grade, Grade.date_received)
        .join(Grade.student)
        .where(
            Grade.subject_id == subject_id,
            Student.group_id == group_id,
            Grade.date_received == subq,
        )
    )
    return session.execute(query).all()


def show_rows(rows):
    for row in rows:
        print(row)


if __name__ == "__main__":
    session: Session = SessionLocal()

    result_1 = select_1(session)
    print("Знайти 5 студентів із найбільшим середнім балом з усіх предметів:")
    show_rows(result_1)
    print("\n")

    result_2 = select_2(session, 4)
    print("Знайти студента із найвищим середнім балом з певного предмета:")
    show_rows(result_2)
    print("\n")

    result_3 = select_3(session, 2)
    print("Знайти середній бал у групах з певного предмета:")
    show_rows(result_3)
    print("\n")

    result_4 = select_4(session)
    print("Знайти середній бал на потоці (по всій таблиці оцінок):")
    print(result_4)
    print("\n")

    result_5 = select_5(session, 5)
    print("Знайти які курси читає певний викладач:")
    show_rows(result_5)
    print("\n")

    result_6 = select_6(session, 13)
    print("Знайти список студентів у певній групі:")
    show_rows(result_6)
    print("\n")

    result_7 = select_7(session, 15, 2)
    print("Знайти оцінки студентів у окремій групі з певного предмета:")
    show_rows(result_7)
    print("\n")

    result_8 = select_8(session, 6)
    print("Знайти всіх викладачів з їхніми предметами:")
    show_rows(result_8)
    print("\n")

    result_9 = select_9(session, 4)
    print("Знайти список курсів, які відвідує певний студент:")
    show_rows(result_9)
    print("\n")

    result_10 = select_10(session, 10, 6)
    print("Список курсів, які певному студенту читає певний викладач:")
    show_rows(result_10)
    print("\n")

    result_11 = select_11(session, 10, 6)
    print("Середній бал, який певний викладач ставить певному студентові:")
    print(result_11)
    print("\n")

    result_12 = select_12(session, 13, 7)
    print("Оцінки студентів у певній групі з певного предмета на останньому занятті:")
    show_rows(result_12)
    print("\n")
