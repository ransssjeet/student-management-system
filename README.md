# Student Management System (Python OOP)

## Project overview
A console-based Student Management System for Bleep Project 01. It demonstrates the four pillars/ideas of OOP requested in the project brief, along with CSV file handling and exception handling.

## Features
- Add a student with ID, name, class, and marks
- Display all students
- Search by student ID
- Update name, class, or marks
- Delete a student after confirmation
- Calculate average marks
- Save and load records from a CSV file
- Validate student data and handle common input/file errors

## OOP concepts demonstrated
1. **Classes and objects:** `Student`, `StudentManagementSystem`, and storage classes.
2. **Encapsulation:** `Student.__student_id` and `Student.__marks` are private; `name`, `student_id`, `class_name`, and `marks` use properties as getters/setters.
3. **Inheritance:** `Student` inherits from `Person`; `CSVStudentStorage` inherits from `StudentStorage`.
4. **Abstraction:** `Person` and `StudentStorage` are abstract base classes using `abc.ABC` and `@abstractmethod`.
5. **File handling:** `CSVStudentStorage` reads/writes CSV using `csv` and `pathlib`.
6. **Exception handling:** invalid marks/fields, malformed CSV rows, and file read/write errors are handled.

## Files
- `student_management.py` — complete application source code
- `data/students.csv` — sample student records
- `screenshots/` — sample console output captures for key operations

## Requirements
- Python 3.9 or later
- No third-party packages required

## How to run
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python student_management.py
   ```

The program creates `data/students.csv` if it needs to save records and the folder does not exist.

## CSV format
The file uses these columns: `student_id`, `name`, `class_name`, `marks`.
Multiple marks are separated by semicolons within the marks cell.

## Sample data
The sample CSV contains fictional students only. You can edit or delete these records while testing.

## Testing checklist
- Add a new student and verify it appears in the display.
- Search for an existing and a missing ID.
- Update a student's marks and confirm the average changes.
- Delete a student after confirming.
- Restart the program and verify that saved records load.
- Try invalid marks (text, negative values, or values over 100).
