import sqlite3

CONN = sqlite3.connect('school.db')
CURSOR = CONN.cursor()


class Student:
        def __init__(self, name, age, course, fees, id=None):
            # Instance attributes representing the columns in the database table
            self.id = id
            self.name = name
            self.age = age
            self.course = course
            self.fees = fees
            
        @classmethod
        def create_table(cls):
            sql = "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY,name TEXT,age INTEGER,course TEXT,fees REAL)"
            CURSOR.execute(sql)
            CONN.commit()

        @classmethod
        def drop_table(cls):
            sql = """
                DROP TABLE IF EXISTS students;
            """
            CURSOR.execute(sql)
            CONN.commit()

        @classmethod
        def create(cls, name, age, course, fees):
            student = cls(name, age, course, fees)
            
            sql = "INSERT INTO students (name, age, course, fees) VALUES (?, ?, ?, ?)"
            CURSOR.execute(sql, (student.name, student.age, student.course, student.fees))
            CONN.commit()
            
            student.id = CURSOR.lastrowid
            return student


        @classmethod
        def fetch_all(cls):
            sql = "SELECT * FROM students"
            CURSOR.execute(sql)
            rows = CURSOR.fetchall()
            return [cls(*row[1:], id=row[0]) for row in rows]

        @classmethod
        def fetch_one(cls, student_id):
            sql = "SELECT * FROM students WHERE id = ?"
            CURSOR.execute(sql, (student_id,))
            row = CURSOR.fetchone()
            if row:
                return cls(*row[1:], id=row[0])
            return None

        @classmethod
        def update(cls, student_id, name, age, course, fees):
            sql = """
                UPDATE students
                SET name = ?, age = ?, course = ?, fees = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (name, age, course, fees, student_id))
            CONN.commit()

        @classmethod
        def delete(cls, student_id):
            sql = """
                DELETE FROM students
                WHERE id = ?
            """
            CURSOR.execute(sql, (student_id,))
            CONN.commit()



# Testing
# Student.drop_table()
Student.create_table()


# ------------  Add some students
# Uncomment this if want to add data
# student1 = Student.create("Mike", 20, "Computer Science", 1500.50)
# student2 = Student.create("Johnson", 22, "Mathematics", 1200.75)

# ------------ Updating a new student
Student.update(1, " Michael", 21, "Software Engineering", 1500.50)

#------------- Fetch all students
all_students = Student.fetch_all()
print("All Students:")
for student in all_students:
    print(vars(student))


#------------- Fetch a single student
single_student = Student.fetch_one(1)
print("\nFetched Student:")

# ------------ Delete a student
print("Delete student ")
Student.delete(6)