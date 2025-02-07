
from domain.model.account import Account,Parent, Student, Person
from domain.engine import session
from sqlalchemy import select, desc


class AccountManager:

    def get_account_by_mobile(self, mobile) -> Account:
        '''(str ) -> Account'''
        return session.query(Account).filter(Account.mobile == mobile).one_or_none()


    def get_parent_by_id(self, parent_id) -> Parent:
        return session.query(Parent).filter(Parent.id == parent_id).one_or_none()
 
    def get_person_by_id(self, person_id) -> Person:
        return session.query(Person).filter(Person.id == person_id).one_or_none()
 
    

    def get_student_by_id(self, student_id) -> Student:
        return session.query(Student).filter(Student.id == student_id).one_or_none()

    def get_students_by_parent_id(self, parent_id) -> list[Student]:
        return session.query(Student).filter(Student.parent_id == parent_id).all()



