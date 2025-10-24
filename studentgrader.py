from enum import Enum
from dataclasses import dataclass, field, asdict
import json


class Grade(Enum):
    A = "Excellent"
    B = "Good"
    C = "Credit"
    D = "Pass"
    F = "Fail"

@dataclass
class Student:
    name: str
    subjects: dict = field(default_factory=dict)

    def add_subject(self, subject: str, score: float):
        if not 0 <= score <= 100:
            print("Score must be between 0 and 100")
        self.subjects[subject] = score

    def calculate_average(self):
        return sum(self.subjects.values()) / len(self.subjects) if self.subjects else 0
    
    def grade_summary(self):
        avg = self.calculate_average()
        if avg >= 70:
            return Grade.A
        elif 60 <= avg <=69:
            return Grade.B
        elif 50 <= avg <= 59:
            return Grade.C
        elif 40 <= avg <= 49:
            return Grade.D
        else:
            return Grade.F



class StudentGrader:
    def __init__(self, file_name="student.json"):
        self.file_name = file_name
        self.subjects = ["Basic Science", 
                "Security Education", 
                "Basic Technology", 
                "Agriculture", 
                "C.C.A", 
                "P.H.E"]
        self.students: list[Student] = []
        self.load_from_json()

    def add_student(self):
        name = input("Enter student name: ").strip().title()
        if not name:
            raise ValueError("Inavlid Name")
        student = Student(name)
        for _ in range(len(self.subjects)):
            subject = input("Enter subject: ").strip().title()
            if subject not in self.subjects:
                print("Enter a valid subject")
                continue
            try:
                score = int(input(f"Enter score for {subject}: ").strip())
                student.add_subject(subject, score)
            except ValueError:
                print("Enter a valid score")
                continue
        self.students.append(student)
    

    def view_students(self):
        for student in self.students:
            print(f"{student.name} - Average: {student.calculate_average()} - Grade: {student.grade_summary()}")

    def save_to_json(self):
        with open(self.file_name, "w") as jsonfile:
            json.dump([asdict(student) for student in self.students], jsonfile, indent=4)   
    
    def load_from_json(self):
        try:
            with open(self.file_name, "r") as jsonfile:
                data = json.load(jsonfile)
                self.students = [Student(**item) for item in data]
        except FileNotFoundError:
            self.students = []

def main():
    print("Welcome to the Student Grader menu.")
    print(1, "Enter student name")
    print(2, "View Students Grade")
    print(3, "Exit")

    while True:
        try:
            choice = int(input("Enter menu: "))
        except ValueError:
            print("Invalid Choice")
        else:
            if choice == 1:
                studentgrade = StudentGrader("studentgrades.json")
                studentgrade.add_student()
                studentgrade.save_to_json()
            elif choice == 2:
                studentgrade.view_students()
            elif choice == 3:
                print("Bye for now!")
                break
            else:
                print("Invalid Input!")


if __name__ == "__main__":
    main()

