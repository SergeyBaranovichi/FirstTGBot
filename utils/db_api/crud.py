# from datetime import date, time
#
# from sqlalchemy.future import select
# from sqlalchemy.orm import Session
# from sqlalchemy import delete, update
#
# from models import User, Procedure, Workday
# from .loader import engine
#
#
# class UserCRUD(object):
#
#     @staticmethod
#     def add_user(first_name: str,
#                  last_name: str,
#                  phonenumber: str,
#                  procedure_id: int,
#                  workday_id: int):
#         with Session(bind=engine) as session:
#             session.execute(
#                 User(
#                     first_name=first_name,
#                     last_name=last_name,
#                     phonenumber=phonenumber,
#                     procedure_id=procedure_id,
#                     workday_id=workday_id
#                 )
#             )
#             session.commit()
#
#     @staticmethod
#     def get_user_by_phonenumber(phonenumber: str):
#         with Session(bind=engine) as session:
#             response = session.execute(
#                 select(User).where(User.phonenumber == phonenumber)
#             )
#             return response.first()[0]
#
#     @staticmethod
#     def delete_user_by_id(user_id: int) -> None:
#         with Session(bind=engine) as session:
#             session.execute(
#                 delete(User).where(User.id == user_id)
#             )
#             session.commit()
#
#
# class ProcedureCRUD(object):
#
#     @staticmethod
#     def add_procedure(procedure_name: str,
#                       procedure_duration: str,
#                       cost: int):
#         with Session(bind=engine) as session:
#             session.execute(
#                 Procedure(
#                     procedure_name=procedure_name,
#                     procedure_duration=procedure_duration,
#                     cost=cost,
#                 )
#             )
#             session.commit()
#
#     @staticmethod
#     def get_procedure_by_id(procedure_id: int):
#         with Session(bind=engine) as session:
#             response = session.execute(
#                 select(Procedure).where(Procedure.id == procedure_id)
#             )
#             return response.first()[0]
#
#     @staticmethod
#     def delete_procedure_by_id(procedure_id: int) -> None:
#         with Session(bind=engine) as session:
#             session.execute(
#                 delete(Procedure).where(Procedure.id == procedure_id)
#             )
#             session.commit()
#
#     @staticmethod
#     def update_procedure_by_id(procedure_id: int,
#                                procedure_name: str = None,
#                                procedure_duration: str = None,
#                                cost: int = None) -> None:
#         with Session(bind=engine) as session:
#             session.execute(
#                 update(Procedure).values(
#                     procedure_name=procedure_name if procedure_name else Procedure.procedure_name,
#                     procedure_duration=procedure_duration if procedure_duration else Procedure.procedure_duration,
#                     cost=cost if cost else Procedure.cost,
#                 ).where(Procedure.id == procedure_id)
#             )
#             session.commit()
#
#
# class WorkdayCRUD(object):
#
#     @staticmethod
#     def add_workday(workday: date,
#                     worktime: time,
#                     availability: bool = True):
#         with Session(bind=engine) as session:
#             session.execute(
#                 Workday(
#                     workday=workday,
#                     worktime=worktime,
#                     availability=availability
#                 )
#             )
#             session.commit()
#
#     @staticmethod
#     def delete_workday_by_id(workday_id: int) -> None:
#         with Session(bind=engine) as session:
#             session.execute(
#                 delete(Workday).where(Workday.id == workday_id)
#             )
#             session.commit()
#
#     @staticmethod
#     def update_workday_by_id(workday_id: int,
#                              workday: date = None,
#                              worktime: time = None,
#                              availability: bool = None) -> None:
#         with Session(bind=engine) as session:
#             session.execute(
#                 update(Workday).values(
#                     workday=workday if workday else Workday.workday,
#                     worktime=worktime if worktime else Workday.worktime,
#                     availability=availability if availability else Workday.availability,
#                 ).where(Workday.id == workday_id)
#             )
#             session.commit()
#
#     @staticmethod
#     def get_workdays() -> list:
#         with Session(bind=engine) as session:
#             response = session.execute(
#                 select(Workday).where(Workday.availability == True)
#             )
#             return response
