"""Student Management System - Bleep Project 01.

Demonstrates classes/objects, encapsulation, inheritance, abstraction,
CSV file handling, and exception handling.
Run: python student_management.py
"""

from abc import ABC, abstractmethod
import csv
from pathlib import Path


# -------------------- ABSTRACTION --------------------
class Person(ABC):
    """Abstract base class for people in the system."""

    def __init__(self, name):
        self.name = name  # validated through the setter

    @property
    def name(self):
        """Getter for the protected name attribute."""
        return self._name

    @name.setter
    def name(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @abstractmethod
    def get_details(self):
        """Return a readable description of the person."""
        raise NotImplementedError


# -------------------- INHERITANCE + ENCAPSULATION --------------------
class Student(Person):
    """A student inherits common person details and stores academic data."""

    def __init__(self, student_id, name, class_name, marks):
        super().__init__(name)
        self.__student_id = ""
        self._class_name = ""
        self.__marks = []
        self.student_id = student_id
        self.class_name = class_name
        self.marks = marks

    @property
    def student_id(self):
        """Getter for private student ID."""
        return self.__student_id

    @student_id.setter
    def student_id(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Student ID cannot be empty.")
        self.__student_id = value

    @property
    def class_name(self):
        """Getter for protected class name."""
        return self._class_name

    @class_name.setter
    def class_name(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Class cannot be empty.")
        self._class_name = value

    @property
    def marks(self):
        """Return a copy so callers cannot silently change internal marks."""
        return self.__marks.copy()

    @marks.setter
    def marks(self, values):
        if not isinstance(values, (list, tuple)) or not values:
            raise ValueError("Enter at least one mark.")
        try:
            converted = [float(mark) for mark in values]
        except (TypeError, ValueError) as exc:
            raise ValueError("Marks must be numeric.") from exc
        if any(mark < 0 or mark > 100 for mark in converted):
            raise ValueError("Each mark must be between 0 and 100.")
        self.__marks = converted

    def calculate_average(self):
        return sum(self.__marks) / len(self.__marks) if self.__marks else 0.0

    def get_details(self):
        marks_text = ", ".join(f"{mark:g}" for mark in self.__marks)
        return (
            f"ID: {self.student_id} | Name: {self.name} | "
            f"Class: {self.class_name} | Marks: {marks_text} | "
            f"Average: {self.calculate_average():.2f}"
        )


# -------------------- ABSTRACTION: STORAGE CONTRACT --------------------
class StudentStorage(ABC):
    """Abstract interface for loading and saving student records."""

    @abstractmethod
    def load_students(self):
        """Load and return a list of Student objects."""
        raise NotImplementedError

    @abstractmethod
    def save_students(self, students):
        """Save a collection of Student objects."""
        raise NotImplementedError


# -------------------- FILE HANDLING + INHERITANCE --------------------
class CSVStudentStorage(StudentStorage):
    """Concrete storage class that reads and writes CSV files."""

    FIELDNAMES = ["student_id", "name", "class_name", "marks"]

    def __init__(self, file_path="data/students.csv"):
        self.file_path = Path(file_path)

    def load_students(self):
        if not self.file_path.exists():
            return []

        students = []
        try:
            with self.file_path.open("r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                required = set(self.FIELDNAMES)
                if not reader.fieldnames or not required.issubset(reader.fieldnames):
                    raise ValueError("CSV file is missing required column headers.")

                for line_number, row in enumerate(reader, start=2):
                    try:
                        marks_text = row["marks"].strip()
                        marks = [float(part.strip()) for part in marks_text.split(";") if part.strip()]
                        students.append(
                            Student(
                                row["student_id"],
                                row["name"],
                                row["class_name"],
                                marks,
                            )
                        )
                    except (ValueError, TypeError, KeyError) as exc:
                        print(f"Skipping invalid CSV row {line_number}: {exc}")
        except OSError as exc:
            raise OSError(f"Could not read '{self.file_path}': {exc}") from exc
        return students

    def save_students(self, students):
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with self.file_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                for student in students:
                    writer.writerow({
                        "student_id": student.student_id,
                        "name": student.name,
                        "class_name": student.class_name,
                        "marks": ";".join(f"{mark:g}" for mark in student.marks),
                    })
        except OSError as exc:
            raise OSError(f"Could not write '{self.file_path}': {exc}") from exc


# -------------------- APPLICATION / CRUD OPERATIONS --------------------
class StudentManagementSystem:
    def __init__(self, storage):
        self.storage = storage
        self.students = {}
        self.load_records()

    def load_records(self):
        try:
            loaded_students = self.storage.load_students()
            self.students = {student.student_id: student for student in loaded_students}
            if loaded_students:
                print(f"Loaded {len(loaded_students)} student record(s).")
        except (OSError, csv.Error, ValueError) as exc:
            print(f"Warning: records could not be loaded: {exc}")
            self.students = {}

    def save_records(self):
        try:
            self.storage.save_students(list(self.students.values()))
            print("Records saved successfully.")
            return True
        except (OSError, csv.Error) as exc:
            print(f"Error saving records: {exc}")
            return False

    def add_student(self):
        try:
            student_id = input("Student ID: ").strip()
            if student_id in self.students:
                print("Error: that student ID already exists.")
                return
            name = input("Student name: ").strip()
            class_name = input("Class: ").strip()
            marks = self._read_marks(input("Marks (comma-separated, 0-100): "))
            student = Student(student_id, name, class_name, marks)
            self.students[student.student_id] = student
            if self.save_records():
                print("Student added successfully.")
        except ValueError as exc:
            print(f"Invalid student details: {exc}")

    @staticmethod
    def _read_marks(raw_text):
        parts = [part.strip() for part in raw_text.split(",") if part.strip()]
        if not parts:
            raise ValueError("Enter at least one mark.")
        try:
            return [float(part) for part in parts]
        except ValueError as exc:
            raise ValueError("Marks must be numbers separated by commas.") from exc

    def display_students(self):
        if not self.students:
            print("No student records found.")
            return
        print("\n--- STUDENT RECORDS ---")
        for student in sorted(self.students.values(), key=lambda item: item.student_id):
            print(student.get_details())

    def search_student(self):
        student_id = input("Enter student ID to search: ").strip()
        student = self.students.get(student_id)
        print(student.get_details() if student else "Student not found.")

    def update_student(self):
        student_id = input("Enter student ID to update: ").strip()
        student = self.students.get(student_id)
        if not student:
            print("Student not found.")
            return

        print("Press Enter to keep an existing value.")
        try:
            name = input(f"Name [{student.name}]: ").strip()
            class_name = input(f"Class [{student.class_name}]: ").strip()
            marks_text = input(
                f"Marks [{';'.join(f'{mark:g}' for mark in student.marks)}] "
                "(comma-separated): "
            ).strip()

            # Validate all new values before changing the object.
            new_name = name if name else student.name
            new_class = class_name if class_name else student.class_name
            new_marks = self._read_marks(marks_text) if marks_text else student.marks

            student.name = new_name
            student.class_name = new_class
            student.marks = new_marks
            if self.save_records():
                print("Student updated successfully.")
        except ValueError as exc:
            print(f"Update cancelled: {exc}")

    def delete_student(self):
        student_id = input("Enter student ID to delete: ").strip()
        if student_id not in self.students:
            print("Student not found.")
            return
        confirm = input("Confirm deletion? (yes/no): ").strip().lower()
        if confirm == "yes":
            deleted = self.students.pop(student_id)
            if self.save_records():
                print(f"Student {deleted.student_id} deleted successfully.")
        else:
            print("Deletion cancelled.")

    def show_average(self):
        student_id = input("Enter student ID: ").strip()
        student = self.students.get(student_id)
        if student:
            print(f"Average marks for {student.name}: {student.calculate_average():.2f}")
        else:
            print("Student not found.")

    def run(self):
        actions = {
            "1": self.add_student,
            "2": self.display_students,
            "3": self.search_student,
            "4": self.update_student,
            "5": self.delete_student,
            "6": self.show_average,
        }

        while True:
            print(
                "\n===== STUDENT MANAGEMENT SYSTEM =====\n"
                "1. Add student\n"
                "2. Display all students\n"
                "3. Search student\n"
                "4. Update student\n"
                "5. Delete student\n"
                "6. Calculate average marks\n"
                "7. Save records\n"
                "8. Exit"
            )
            choice = input("Choose an option (1-8): ").strip()
            if choice in actions:
                actions[choice]()
            elif choice == "7":
                self.save_records()
            elif choice == "8":
                self.save_records()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 8.")


def main():
    storage = CSVStudentStorage()
    app = StudentManagementSystem(storage)
    app.run()


if __name__ == "__main__":
    main()
