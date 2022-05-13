from datetime import date, time

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy import delete, update

from .loader import engine
from .models import User, Procedure, Workday


class UserCRUD(object):

    @staticmethod
    def add_user(user: dict):
        with Session(bind=engine) as session:
            session.add(
                User(**user)
            )
            session.commit()

    @staticmethod
    def get_user_by_tgid(tg_id: int):
        with Session(bind=engine) as session:
            response = session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            if response.first():
                return response.first()[0]
            else:
                return None

    @staticmethod
    def delete_user_by_tg_id(tg_id: int) -> None:
        with Session(bind=engine) as session:
            session.execute(
                delete(User).where(User.tg_id == tg_id)
            )
            session.commit()


class ProcedureCRUD(object):

    @staticmethod
    def add_procedure(procedure_name: str,
                      procedure_duration: time,
                      cost: int) -> None:
        with Session(bind=engine) as session:
            session.add(Procedure(
                procedure_name=procedure_name,
                procedure_duration=procedure_duration,
                cost=cost
                )
            )
            session.commit()

    @staticmethod
    def get_procedure_by_id(procedure_id: int):
        with Session(bind=engine) as session:
            response = session.execute(
                select(Procedure).where(Procedure.id == procedure_id)
            )
            return response.first()[0]

    @staticmethod
    def get_all_procedures():
        with Session(bind=engine) as session:
            response = session.execute(
                select(Procedure).where()
            )
            return response.all()

    @staticmethod
    def delete_procedure_by_id(procedure_id: int) -> None:
        with Session(bind=engine) as session:
            session.execute(
                delete(Procedure).where(Procedure.id == procedure_id)
            )
            session.commit()

    @staticmethod
    def update_procedure_by_id(procedure_id: int,
                               procedure_name: str = None,
                               procedure_duration: str = None,
                               cost: int = None) -> None:
        with Session(bind=engine) as session:
            session.execute(
                update(Procedure).values(
                    procedure_name=procedure_name if procedure_name else Procedure.procedure_name,
                    procedure_duration=procedure_duration if procedure_duration else Procedure.procedure_duration,
                    cost=cost if cost else Procedure.cost,
                ).where(Procedure.id == procedure_id)
            )
            session.commit()


class WorkdayCRUD(object):

    @staticmethod
    def add_workday(workday: date,
                    worktime: time,
                    availability: bool = True):
        with Session(bind=engine) as session:
            session.add(
                Workday(
                    workday=workday,
                    worktime=worktime,
                    availability=availability
                )
            )
            session.commit()

    @staticmethod
    def delete_workday_by_id(workday_id: int) -> None:
        with Session(bind=engine) as session:
            session.execute(
                delete(Workday).where(Workday.id == workday_id)
            )
            session.commit()

    @staticmethod
    def update_workday_by_id(workday_id: int,
                             workday: date = None,
                             worktime: time = None,
                             availability: bool = None) -> None:
        with Session(bind=engine) as session:
            session.execute(
                update(Workday).values(
                    workday=workday if workday else Workday.workday,
                    worktime=worktime if worktime else Workday.worktime,
                    availability=availability if availability is not None else Workday.availability
                ).where(Workday.id == workday_id)
            )
            session.commit()
            # session.query(Workday).filter(Workday.id == workday_id).update(
            #     workday=workday if workday else Workday.workday,
            #     worktime=worktime if worktime else Workday.worktime,
            #     availability=availability if availability else Workday.availability
            # )

    @staticmethod
    def get_workdays() -> list:
        with Session(bind=engine) as session:
            response = session.execute(
                select(Workday).where(Workday.availability == True)
            )
            return response.all()

    @staticmethod
    def get_workday_by_id(work_id: int) -> Workday:
        with Session(bind=engine) as session:
            response = session.execute(
                select(Workday).where(Workday.id == work_id)
            )
            return response.first()[0]

    @staticmethod
    def get_my_workdays() -> list:
        with Session(bind=engine) as session:
            response = session.execute(
                select(Workday).where(Workday.availability == False)
            )
            return response.all()
