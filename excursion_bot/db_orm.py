import csv
import os
import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker

DB_NAME = 'excursion_orm_bot.db'
FILE_INFO_NAME = 'test_data.csv'
Base = declarative_base()
ENGINE = create_engine(f'sqlite:///{DB_NAME}')
SessionLocal = sessionmaker(bind=ENGINE)


class ExcursionName(Base):
    __tablename__ = 'excursion_names'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __str__(self):
        return f'{self.name} {self.description}'

    def __repr__(self):
        return f'{self.name} {self.description}'


class ExcursionDate(Base):
    __tablename__ = 'excursion_dates'
    id = Column(Integer, primary_key=True)
    excursion_name_id = Column(Integer, ForeignKey('excursion_names.id'))
    date = Column(DateTime)


class UserInExcursion(Base):
    __tablename__ = 'user_in_excursion'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    excursion_date_id = Column(Integer, ForeignKey('excursion_dates.id'))


def create_db():
    Base.metadata.create_all(bind=ENGINE)


def drop_db(db_name):
    if os.path.exists(db_name):
        os.remove(db_name)


def insert_info_from_file(file_name):
    session = SessionLocal()
    file = open(file_name)
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)
    exc_names_set = set()
    for row in csv_reader:
        id_, name, description, date = row
        if name not in exc_names_set:
            excursion = ExcursionName(name=name, description=description)
            exc_names_set.add(name)
            session.add(excursion)
            session.flush()
            excursion_id = excursion.id
        else:
            excursion = session.query(ExcursionName).filter_by(name=name).first()
            excursion_id = excursion.id

        date = datetime.datetime.strptime(date, "%d.%m.%Y")
        ex_date = ExcursionDate(excursion_name_id=excursion_id, date=date)
        session.add(ex_date)
    session.commit()
    session.close()

def select_all_excursions():
    session = SessionLocal()
    data = session.query(ExcursionName).all()
    session.close()
    return data

def select_all_users():
    session = SessionLocal()
    data = session.query(UserInExcursion).all()
    session.close()
    return data

def select_all_excursion_dates():
    session = SessionLocal()
    data = session.query(ExcursionDate).all()
    session.close()
    return data

def select_description_by_id(id_):
    session = SessionLocal()
    result = session.query(ExcursionName.description).filter(ExcursionName.id == id_).scalar()
    session.close()
    return result

def select_dates_by_id(id_):
    session = SessionLocal()
    data = session.query(ExcursionDate.id, ExcursionDate.date).filter(ExcursionDate.excursion_name_id == id_).all()
    session.close()
    return data


def insert_user_in_excursion(user_id, excursion_date_id):
    session = SessionLocal()
    user_entry = UserInExcursion(user_id=user_id, excursion_date_id=excursion_date_id)
    session.add(user_entry)
    session.commit()
    session.close()

def select_user_excursion(id_):
    session = SessionLocal()
    result = (session.query(ExcursionName.name, ExcursionDate.date)
              .join(ExcursionDate, ExcursionName.id == ExcursionDate.excursion_name_id)
              .join(UserInExcursion, ExcursionDate.id == UserInExcursion.excursion_date_id)
              .filter(UserInExcursion.user_id == id_).all())
    session.close()
    return result



def reinit_scenario():
    drop_db(DB_NAME)
    create_db()
    insert_info_from_file(FILE_INFO_NAME)


if __name__ == '__main__':
    # reinit_scenario()
    pass



