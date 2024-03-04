import pytest
from student import Student, NameDescriptor

def test_name_descriptor():
    student = Student("Иван Иванов", "subjects.csv")
    assert student.name == "Иван Иванов"
    with pytest.raises(ValueError):
        student.name = "иван иванов"
    with pytest.raises(ValueError):
        student.name = "И555533"

def test_add_grade():
    student = Student("Иван Иванов", "subjects.csv")
    student.add_grade("Математика", 5)
    student.add_grade("Математика", 4)
    student.add_grade("Физика", 3)
    assert student.subjects["Математика"]["grades"] == [5, 4]
    assert student.subjects["Физика"]["grades"] == [3]
def test_add_test_score():
    student = Student("Иван Иванов", "subjects.csv")
    student.add_test_score("Физика", 80)
    assert student.subjects["Физика"]["test_scores"] == [80]
    student.add_test_score("Физика", 90)
    assert student.subjects["Физика"]["test_scores"] == [80, 90]
    with pytest.raises(ValueError):
        student.add_test_score("Физика", 101)
    with pytest.raises(ValueError):
        student.add_test_score("Физика", "B")
    with pytest.raises(ValueError):
        student.add_test_score("Химия", 70)