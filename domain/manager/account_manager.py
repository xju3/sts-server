
from domain.model.account import Account,Parent, Student, Person
from domain.engine import db_engine
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

read_session = Session(db_engine)

class AccountManager:

    def get_account_by_mobile(self, mobile) -> Account:
        '''(str ) -> Account'''
        return read_session.execute(select(Account).where(Account.mobile == mobile)).scalar_one_or_none()


    def get_parent_by_id(self, parent_id) -> Parent:
        return read_session.execute(select(Parent).where(Parent.id == parent_id)).scalar_one_or_none()
 
    def get_person_by_id(self, person_id) -> Person:
        return read_session.execute(select(Person).where(Person.id == person_id)).scalar_one_or_none()
    

    def get_student_by_id(self, student_id) -> Student:
        return read_session.execute(select(Student).where(Student.id == student_id)).scalar_one_or_none()

    def get_students_by_parent_id(self, parent_id) -> list[Student]:
        return read_session.execute(select(Student).where(Student.parent_id == parent_id)).scalars().all()



