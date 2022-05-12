# from sqlalchemy.orm import declarative_base
# from sqlalchemy import Column, ForeignKey, Integer, Text, Date, Time, Boolean
#
# Base = declarative_base()
#
#
# class User(Base):
#
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True)
#     first_name = Column(Text, nullable=False)
#     last_name = Column(Text, nullable=False)
#     phonenumber = Column(Text, nullable=False, unique=True)
#     procedure_id = Column(Integer, ForeignKey('procedures.id', ondelete='CASCADE'))
#     workday_id = Column(Integer, ForeignKey('workdays.id', ondelete='CASCADE'))
#
#
# class Procedure(Base):
#
#     __tablename__ = 'procedures'
#
#     id = Column(Integer, primary_key=True)
#     procedure_name = Column(Text, nullable=False)
#     procedure_duration = Column(Text, nullable=False)
#     cost = Column(Integer, nullable=False)
#
#
# class Workday(Base):
#
#     __tablename__ = 'workdays'
#
#     id = Column(Integer, primary_key=True)
#     workday = Column(Date, nullable=False)
#     worktime = Column(Time, nullable=False)
#     availability = Column(Boolean, nullable=False)
