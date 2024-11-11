import csv
import traceback
from typing import Dict
import random
import math
class Student:

    def __init__(self, group_id: str, student_id: int, school: str, name: str, gender: str, cgpa: float):
        self.group_id = group_id
        self.team_id = 0 # Not set yet
        self.student_id = student_id
        self.school = school
        self.name = name
        self.gender = gender
        self.cgpa = cgpa

    def assign_team(self, team_id: int):
        self.team_id = team_id

    def __str__(self):
        return (f'{self.group_id}, Student ID: {self.student_id}, School: {self.school},'
                  f'Name:{self.name}, Gender: {self.gender}, CGPA: {self.cgpa}, Team: {self.team_id}')

class TeamGroup:
    def __init__(self, team_id: int, group_id: int):
        self.group_id = group_id
        self.team_id = team_id
        self.students: list[Student] = []

    def __str__(self):
        return f"{self.group_id}:\n{[str(student) for student in self.students]}"

    def add_student(self, student: Student):
        self.students.append(student)
    
    def remove_student(self, student: Student):
        self.students.remove(student)
    
    def get_avg_cgpa(self):
        return sum([student.cgpa for student in self.students]) / len(self.students)
    def diversity_score(self):
        score = 0
        for i in range(len(self.students)):
            for j in range(i + 1, len(self.students)):
                score += diff(self.students[i], self.students[j], 0.5, 0.5, 1)
        return score
    
class TutorialGroup:
    def __init__(self, group_id: int):
        self.group_id = group_id
        self.students_by_teams: Dict[int, TeamGroup] = {}
        self.students = []
        self.min_cpga = 0
        self.max_cpga = 0
        self.avg_cpga = 0

    def __str__(self):
        return f"{self.group_id}:\n{[str(student) for student in self.students]}"

    def add_student(self, student: Student):
        self.students.append(student)

    def get_max_cgpa(self):
        if (self.max_cpga != 0):
            return self.max_cpga
        self.max_cpga = 0
        for student in self.students:
            if student.cgpa > self.max_cpga:
                self.max_cpga = student.cgpa
        return self.max_cpga

    def get_min_cgpa(self):
        if (self.min_cpga != 0):
            return self.min_cpga
        self.min_cpga = 10
        for student in self.students:
            if student.cgpa < self.min_cpga:
                self.min_cpga = student.cgpa
        return self.min_cpga
    
    def get_avg_cgpa(self):
        if (self.avg_cpga != 0):
            return self.avg_cpga
        self.avg_cpga = sum([student.cgpa for student in self.students]) / len(self.students)
        return self.avg_cpga

    def get_group_score(self):
        score = 0
        for team in self.students_by_teams.values():
            score += team.diversity_score()
        return score

    def shuffle(self):
        random.shuffle(self.students)

    def assign_group(self, max_pax: int):
        self.shuffle()
        self.max_cpga = 0
        self.min_cpga = 0
        self.students_by_teams = {}
        for i in range(0, len(self.students), max_pax):
            team_id = i // max_pax + 1
            self.students_by_teams[team_id] = TeamGroup(team_id, self.group_id)
            for j in range(i, i + max_pax):
                if j < len(self.students):
                    self.students[j].team_id = team_id
                    self.students_by_teams[team_id].add_student(self.students[j])
                else:
                    break

students_by_groups: Dict[str, TutorialGroup] = {}
student_by_id: Dict[str, Student] = {}
students_by_groups: Dict[str, TutorialGroup] = {

}

students_by_id: Dict[str, Student] = {

}

def load_csv():
    global students_by_groups
    global students_by_id
    students_by_groups = {}
    students_by_id = {}
    with open('records.csv', mode='r') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)
        next(csv_reader)

        # Append students to corresponding tutorial groups
        for row in csv_reader:

            tutorial_group = row[0]
            student_id = int(row[1])  # Convert to int
            school = row[2]
            name = row[3]
            gender = row[4]
            cgpa = float(row[5])  # Convert to float

            if tutorial_group not in students_by_groups:
                students_by_groups[tutorial_group] = TutorialGroup(tutorial_group)

            students_by_id[str(student_id)] = Student(tutorial_group, student_id, school, name, gender, cgpa)
            students_by_groups[tutorial_group].add_student(Student(tutorial_group, student_id, school, name, gender, cgpa))

load_csv()

# for group_id, tutorial in students_by_groups.items():
#     print(f'Group: {group_id}')
#     for student in tutorial.students:
#         print(student)
#     print()

def dividing_group(students_by_groups: Dict[str, TutorialGroup] = {}):
    for group_id, tutorial_group in students_by_groups.items():
        tutorial_group.assign_group(5)


dividing_group(students_by_groups)


# for group_id, tutorial in students_by_groups.items():
#     print(f'Group: {group_id}')
#     for i in range(len(tutorial.teams)):
#         print(f'Team: {i+1}')
#         for student in tutorial.teams[i].students_of_team:
#             print(student)
#     print()
def diff(A: Student, B: Student, w_s: float, w_g: float, w_c: float) -> float:
    # A and B are in the same team and group
    res = 0
    # If the school is not the same, then add w_s^2 to the result
    if A.school != B.school:
        res += w_s * w_s
    # If the gender is not the same, then add w_g^2 to the result
    d_gender = 0
    if A.gender != B.gender:
        d_gender = w_g * w_g
    elif A.gender == B.gender and A.gender == "Female":
        d_gender += w_g * w_g / 4

    # CGPA Diversity Score
    Group: TutorialGroup = students_by_groups[A.group_id]
    
    d_cgpa = abs(A.cgpa - B.cgpa) / (Group.get_max_cgpa() - Group.get_min_cgpa())
    d_avg = 0
    # CGPA Mean Score
    if A.team_id and A.team_id in Group.students_by_teams:
        Team: TeamGroup = Group.students_by_teams[A.team_id]

        avg_team = Team.get_avg_cgpa()
        avg_group = Group.get_avg_cgpa()
        d_avg = abs(avg_team - avg_group) / (Group.get_max_cgpa() - Group.get_min_cgpa())
    else:
        d_avg = 0

    diff = d_cgpa * 0.5 - d_avg * 1.5 + 1.5
    diff /= 3 / 2
    diff *= w_c
    res = res + d_gender * d_gender + diff * diff
    return math.sqrt(res)

def swap(A: Student, B: Student, group: TutorialGroup):
    ref_A = A.team_id
    ref_B = B.team_id
    A.team_id = B.team_id
    B.team_id = ref_A
    group.students_by_teams[ref_A].remove_student(A)
    group.students_by_teams[ref_A].add_student(B)
    group.students_by_teams[ref_B].remove_student(B)
    group.students_by_teams[ref_B].add_student(A)

# swap(student_by_id['5002'], student_by_id['5708'])

# for group_id, TutorialGroup in students_by_groups.items():
#     print(f'Score of group: {group_id}')
#     for team in TutorialGroup.teams:
#         print(team.get_team_score())
#     print(f'Total score: {TutorialGroup.get_group_score()}')
#     print()

def local_improve(swap_student: Student, group: TutorialGroup):
    improve = False
    group_score = group.get_group_score()
    for team in group.students_by_teams.values():
        for student in team.students:
            if student.team_id != swap_student.team_id:
                swap(swap_student, student, group)
                current_group_score = group.get_group_score()
                if current_group_score > group_score:
                    group_score = current_group_score
                    improve = True    
                else:
                    swap(swap_student, student, group)
    return improve

# Multiprocessing
import concurrent.futures
from multiprocessing import cpu_count

def group_improve(group: TutorialGroup):
    group_score = group.get_group_score()
    print(group.group_id, f'Before: {group_score}', end=' ')
    for student in group.students:
        while local_improve(student, group):
            pass
        else:
            continue
    group_score = group.get_group_score()
    print(f'After: {group_score}')

def group_improve_wrapper(group: TutorialGroup):
    try:
        group_improve(group)
    except Exception as e:
        print(f"An error occurred in group {group.group_id}: {e}")
        print(traceback.format_exc())   

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        # Convert dict_values to a list before slicing
        TutorialGroups_list = list(students_by_groups.values())
        futures = [executor.submit(group_improve, TutorialGroup) for TutorialGroup in TutorialGroups_list]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
                for group in TutorialGroups_list:
                    print(group.get_group_score(), group.get_avg_cgpa())
                    for team in group.students_by_teams.values():
                        for student in team.students:
                            print(student)
            except Exception as e:
                print(f"An error occurred: {e}")


    
# student_by_id