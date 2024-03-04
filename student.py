import csv
import argparse
import logging
import pytest

logging.basicConfig(level=logging.INFO)

class NameDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if not value.istitle() or not value.replace(" ", "").isalpha():
            raise ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы")
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

class Student:
    name = NameDescriptor()

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)

    def load_subjects(self, subjects_file):
        logging.info(f"Загрузка предметов из файла {subjects_file}")
        with open(subjects_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for subject in row:
                    self.subjects[subject] = {"grades": [], "test_scores": []}

    def add_grade(self, subject, grade):
        if not isinstance(grade, int) or grade < 2 or grade > 5:
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        if subject not in self.subjects:
            self.subjects[subject] = {"grades": [], "test_scores": []}
        self.subjects[subject]["grades"].append(grade)

    def add_test_score(self, subject, test_score):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
            raise ValueError("Результат теста должен быть целым числом от 0 до 100")
        self.subjects[subject]["test_scores"].append(test_score)

    def get_average_test_score(self, subject):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        return sum(self.subjects[subject]["test_scores"]) / len(self.subjects[subject]["test_scores"])

    def get_average_grade(self):
        total_grades = [grade for subject in self.subjects.values() for grade in subject["grades"]]
        return sum(total_grades) / len(total_grades)

    def __str__(self):
        return f"Студент: {self.name}\nПредметы: {', '.join(self.get_active_subjects().keys())}"
    
    def get_active_subjects(self):
        return {k: v for k, v in self.subjects.items() if v["grades"] or v["test_scores"]}

 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Имя студента")
    parser.add_argument("subjects_file", help="CSV-файл с предметами")
    parser.add_argument("subject", help="Предмет для расчета среднего балла")
    parser.add_argument("grades", help="Оценки для добавления, разделенные запятыми")
    parser.add_argument("test_score", help="Результаты теста для добавления, разделенные запятыми", default = None)
    args = parser.parse_args()

    student = Student(args.name, args.subjects_file)
    if args.test_score:
        test_score = map(int, args.test_score.split(','))
        for score in test_score:
            student.add_test_score(args.subject, score)
        print(f"Средний результат теста по предмету {args.subject}: {sum(student.subjects[args.subject]['test_scores']) / len(student.subjects[args.subject]['test_scores'])}")
    grades = map(int, args.grades.split(','))
    for grade in grades:
        student.add_grade(args.subject, grade)
    print(f"Средний балл по предмету {args.subject}: {sum(student.subjects[args.subject]['grades']) / len(student.subjects[args.subject]['grades'])}")

if __name__ == "__main__":
    main()