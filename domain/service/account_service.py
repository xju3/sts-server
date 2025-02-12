
from domain.model.account import Parent, Person, Student, Account, School, Login
from sqlalchemy.orm import sessionmaker
import logging, sys
from datetime import datetime
from domain.engine import engine
from domain.model.common import generate_uuid
from domain.manager.account_manager import AccountManager
from domain.manager.location_manager import baidu_get_schools_nearby
from routers.model.output import AccountInfo_O, StudentInfo_O, Parent_O
from routers.model.input import Registration_I, LoginHistory_I
import uuid

account_manager = AccountManager()
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger()

class AccountService:
    def create_account(self, registration : Registration_I):
        '''创建新的账号'''
        try:
            account_id = generate_uuid()
            person_parent_id = generate_uuid()
            person_student_id = generate_uuid()

            parent_person = Person(id= person_parent_id, full_name=registration.parent)
            student_person = Person(id= person_student_id, full_name=registration.student)

            parent = Parent(id = generate_uuid(), 
                            account_id= account_id, 
                            account_name= registration.account,
                            person_id=person_parent_id)
            
            student = Student(person_id=person_student_id, 
                            school_id=registration.schoolId, 
                            school_name=registration.schoolName, 
                            account_id= account_id,
                            grade=registration.grade)
            account = Account(id=account_id)

            Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            with Session() as session:
                session.add_all([parent, student, student_person, parent_person, account])
                session.commit()
        except Exception as e:
            logger.error(e)
            session.rollback()  
        finally:
            session.close() 

    def create_login_history(self, history : LoginHistory_I):
        """更新推送消息"""
        login = Login(parent_id=history.parentId, 
                      device_id=history.deviceId, 
                      notification_id=history.notificationId, 
                      trans_time=datetime.now())
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with Session() as session: 
            session.query(Parent).filter(Parent.id == history.parentId).update({"device_id": history.deviceId, "notification_id": history.notificationId})
            session.add(login)
            session.commit()


    def login(self, account_name, access_code = None) -> AccountInfo_O | None:
        '''用手机号登录，暂不需要密码'''
        parent = account_manager.get_parent_by_account_name(account_name)
        if parent is None:
            return None
        
        p1 = account_manager.get_person_by_id(parent.person_id)
        parent_o = Parent_O(id=parent.id, name=p1.full_name, accountId=parent.account_id)
        student_list = account_manager.get_students_by_account_id(parent.account_id)
        
        students = []
        for student in student_list:
            person = account_manager.get_person_by_id(student.person_id)
            info = StudentInfo_O(id=student.id, 
                               name=person.full_name, 
                               school=student.school_name, 
                               grade=student.grade, accountId=student.account_id )
            students.append(info) 
        return AccountInfo_O(parent_o, students=students)


    def get_schools(self, latitude, longitude):
        results = baidu_get_schools_nearby(latitude, longitude, 5)
        if len(results) == 0:
            return []
        
        new_schools = []
        for item in results:
            school = account_manager.get_school_by_name(item['name'])
            if school is None:
                id = uuid.uuid1()
                data = School(id=id, full_name=item['name'], 
                    lat=item['lat'],
                    lng=item['lng'],
                              phone=item['phone'], addr=item['addr'])
                item['fullName'] = item['name']
                new_schools.append(data)
                item['id'] = id
            else:
                item['id'] = school.id
                item['fullName'] = school.full_name

            try:
                Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
                with Session() as session:
                    session.add_all(new_schools)
                    session.commit()
                    session.close()
            except Exception as e: 
                print(e)
        return results