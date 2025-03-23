import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from conf.db import SessionLocal
from entity.models import Student, Grade, Subject, Teacher, Group

fake = Faker("en_US")
Faker.seed(42)


def seed_database():
    session: Session = SessionLocal()
    try:
        groups = create_group(session)
        teachers = create_teacher(session)
        subjects = create_subject(session, teachers)
        students = create_student(session, groups)
        create_grades(session, students, subjects)

        session.commit()
        print("Database seeded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def create_group(session: Session):
    group_name = ["CSS-01", "CSS-02", "CSS-03"]
    groups = []
    for name in group_name:
        group = Group(name=name)
        session.add(group)
        groups.append(group)
    session.flush()
    return groups


def create_teacher(session: Session):
    teachers = []
    for _ in range(5):
        teacher = Teacher(
            first_name=fake.first_name()[:100],
            second_name=fake.last_name()[:100],
            email=fake.email()[:100],
            phone=fake.phone_number()[:20],
        )
        session.add(teacher)
        teachers.append(teacher)
    session.flush()
    return teachers


def create_subject(session: Session, teachers: list):
    subject_names = [
        "Programming",
        "Mathematical Analysis",
        "Databases",
        "Web Development",
        "Algorithms and Data Structures",
        "Computer Networks",
        "Operating Systems",
    ]
    subjects = []
    for name in subject_names:
        subject = Subject(name=name, teacher=random.choice(teachers))
        session.add(subject)
        subjects.append(subject)
    session.flush()
    return subjects


def create_student(session: Session, groups: list):
    students = []
    for _ in range(50):
        student = Student(
            first_name=fake.first_name()[:100],
            last_name=fake.last_name()[:100],
            email=fake.email()[:100],
            phone=fake.phone_number()[:20],
            group=random.choice(groups),
        )
        session.add(student)
        students.append(student)
    session.flush()
    return students


def create_grades(session: Session, students: list, subjects: list):
    start_date = (datetime.now() - timedelta(days=180)).date()
    end_date = datetime.now().date()

    for student in students:
        num_grades = random.randint(10, 20)
        for _ in range(num_grades):
            subject = random.choice(subjects)
            grade = Grade(
                student_id=student.id,
                subject_id=subject.id,
                grade=random.randint(60, 100),
                date_received=start_date
                + timedelta(days=random.randint(0, (end_date - start_date).days)),
            )
            session.add(grade)
    session.flush()


if __name__ == "__main__":
    seed_database()
