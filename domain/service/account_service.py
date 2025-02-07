
from domain.model.account import Parent, Person, Student, Account 
from sqlalchemy.orm import Session
from domain.engine import db_engine
from domain.model.common import generate_uuid
from domain.manager.account_manager import AccountManager
from message.dto import AccountInfo, StudentInfo

account_manager = AccountManager()
class AccountService:

    def create_account(self, mobile, school, grade, parent_name, student_name):
        '''创建新的账号'''
        session = Session(db_engine)
        person_parent_id = generate_uuid()
        person_student_id = generate_uuid()
        parent_person = Person(id= person_parent_id, full_name=parent_name)
        student_person = Person(id= person_student_id, full_name=student_name)
        parent = Parent(id = generate_uuid(), person_id=person_parent_id)
        student = Student(person_id=person_student_id, school_name=school, parent_id=parent.id, grade=grade)
        account = Account(id=generate_uuid(), mobile=mobile, parent_id=parent.id)
        session.add_all([parent, student, student_person, parent_person, account])
        session.commit()

    def login(self, mobile, access_code = None) -> AccountInfo | None:
        '''用手机号登录，暂不需要密码'''
        account = account_manager.get_account_by_mobile(mobile)
        if account is None:
            return
        parent = account_manager.get_parent_by_id(account.parent_id)
        p1 = account_manager.get_person_by_id(parent.person_id)
        students = account_manager.get_students_by_parent_id(account.parent_id)
        
        student_info_list = []
        for student in students:
            person = account_manager.get_person_by_id(student.person_id)
            info = StudentInfo(id=student.id, 
                               name=person.full_name, 
                               school=student.school_name, 
                               grade=student.grade, 
                               parentId=parent.id)
            student_info_list.append(info) 

        return AccountInfo(id=account.id, parent_id=account.parent_id, parent_name=p1.full_name, students=student_info_list)

        