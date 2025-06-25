from students.models import Department, Student

def get_schema_with_departments():
    """
    Returns a schema description string for Gemini prompt with actual department names from the database.
    """
    schema = """
Tables:
students_student(
    id, name, admission_number, parent_mobile, student_mobile, door_number, street, city, state, country,
    scholar_type, hostel_block, tenth_hallticket, tenth_marks, twelfth_hallticket, twelfth_branch, twelfth_marks,
    degree_hallticket, degree_branch, degree_marks,
    present_department, -- department name as string, not id!
    present_branch, present_year, present_semester, present_sem_marks,
    total_fees, paid_fees, balance
)
students_department(id, name)
Notes:
- students_student.present_department stores the department NAME (text), not the department id.
- To filter students by department, compare students_student.present_department = students_department.name
"""
    department_names = list(Department.objects.values_list('name', flat=True))
    if department_names:
        schema += f"Current department names: {department_names}\n"
    return schema

def get_schema_with_sample_data():
    schema = get_schema_with_departments()
    student_names = list(Student.objects.values_list('name', flat=True)[:5])
    if student_names:
        schema += f"Sample student names: {student_names}\n"
    return schema