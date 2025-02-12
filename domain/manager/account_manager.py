
from domain.model.account import Account,Parent, Student, Person, School
from domain.model.common import PushMessage
from domain.engine import SessionLocal
from typing import List


class AccountManager:

    def get_notification_list(self, student_id) -> List[PushMessage]:
        student = self.get_student_by_id(student_id)
        if student is None:
            return []
        parents= self.get_parents_by_account_id(student.account_id)
        if parents is None or len(parents) == 0:
            return []
        
        result = []

        for parent in parents:
            target = parent.notification_id
            device_id = parent.device_id
            if (target is None or device_id is None):
                continue
            push_message = PushMessage(target=target, platform=device_id, content="")
            result.append(push_message)
        return result

    def get_school_by_name(self, school_name) -> Account:
        '''(str ) -> Account'''
        with SessionLocal() as session:
            return session.query(School).filter(School.full_name == school_name).one_or_none()

    def get_account_by_id(self, id) -> Account:
        '''(str ) -> Account'''
        with SessionLocal() as session:
            return session.query(Account).filter(Account.id== id).one_or_none()

    def get_parent_by_account_name(self, account_name) -> Parent:
        '''(str ) -> Account'''
        with SessionLocal() as session:
            return session.query(Parent).filter(Parent.account_name == account_name).one_or_none()

    def get_parent_by_id(self, parent_id) -> Parent:
        with SessionLocal() as session:
            return session.query(Parent).filter(Parent.id == parent_id).one_or_none()

    def get_parents_by_account_id(self,account_id) -> List[Parent]:
        with SessionLocal() as session:
            return session.query(Parent).filter(Parent.account_id ==account_id).all()
 
    def get_person_by_id(self, person_id) -> Person:
        with SessionLocal() as session:
            return session.query(Person).filter(Person.id == person_id).one_or_none()

    def get_student_by_id(self, student_id) -> Student:
        with SessionLocal() as session:
            return session.query(Student).filter(Student.id == student_id).one_or_none()

    def get_students_by_account_id(self, account_id) -> list[Student]:
        with SessionLocal() as session:
            return session.query(Student).filter(Student.account_id == account_id).all()