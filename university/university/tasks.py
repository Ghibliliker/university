import pandas as pd

from university.celeryapp import app


@app.task(bind=True)
def create_statistic(self, doc_name, directions, groups) -> None:
    """create xlsx file"""

    direction_name = []
    direction_subjects = []
    direction_curator = []

    for direction in directions:
        direction_name.append(direction['name'])
        if direction['curator']:
            direction_curator.append(direction['curator']['username'])
        subjects = []
        if direction['subjects']:
            for subject in direction['subjects']:
                subjects.append(subject['name'])
        direction_subjects.append(subjects)

    group_name = []
    group_students = []
    group_male = []
    group_female = []
    group_free = []

    for group in groups:
        group_name.append(group['name'])
        students = group['students']
        group_free.append(20 - len(students))
        students_name = []
        male_count = 0
        female_count = 0
        if students:
            for student in students:
                students_name.append(student['username'])
                if student['gender'] == 'male':
                    male_count += 1
                if student['gender'] == 'female':
                    female_count += 1

        group_students.append(sorted(students_name))
        group_male.append(male_count)
        group_female.append(female_count)

    df = pd.DataFrame(
        {
            'Name_direction': direction_name,
            'Subjects_direction': direction_subjects,
            'Curator_direction': direction_curator,
            'Group_name': group_name,
            'Group_students': group_students,
            'Group_male': group_male,
            'Group_female': group_female,
            'Group_free': group_free
        }
    )

    df.to_excel(f'./data/{doc_name}.xlsx')
