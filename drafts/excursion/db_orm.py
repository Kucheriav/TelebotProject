from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import csv
import os

Base = declarative_base()
DB_NAME = 'excursion_bot.db'
FILE_INFO_NAME = 'test_data.csv'
ENGINE = create_engine(f'sqlite:///{DB_NAME}')
SessionLocal = sessionmaker(bind=ENGINE)


class ExcursionName(Base):
    __tablename__ = 'excursion_names'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    # backref для дат экскурсий
    dates = relationship("ExcursionDate", back_populates="excursion_name")


class ExcursionDate(Base):
    __tablename__ = 'excursion_dates'

    id = Column(Integer, primary_key=True)
    excursion_name_id = Column(Integer, ForeignKey('excursion_names.id'))
    date = Column(DateTime)

    # связи
    excursion_name = relationship("ExcursionName", back_populates="dates")
    users = relationship("UserInExcursion", back_populates="excursion_date")


class UserInExcursion(Base):
    __tablename__ = 'user_in_excursion'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    excursion_date_id = Column(Integer, ForeignKey('excursion_dates.id'))

    # backref для удобного доступа
    excursion_date = relationship("ExcursionDate", back_populates="users")


def drop_db(db_name):
    if os.path.exists(db_name):
        os.remove(db_name)


def create_db():
    Base.metadata.create_all(ENGINE)


def insert_info_from_file(file_name):
    session = SessionLocal()

    with open(file_name, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)

        exc_names_set = set()
        for row in csv_reader:
            name, desc, date_str = row[1], row[2], row[3]

            if name not in exc_names_set:
                excursion = ExcursionName(name=name, description=desc)
                session.add(excursion)
                session.flush()
                exc_names_set.add(name)
                excursion_id = excursion.id
            else:
                excursion = session.query(ExcursionName).filter_by(name=name).first()
                excursion_id = excursion.id

            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')  # подставьте нужный формат
            date_entry = ExcursionDate(excursion_name_id=excursion_id, date=date_obj)
            session.add(date_entry)

    session.commit()
    session.close()


def select_all_excursions():
    session = SessionLocal()
    data = session.query(ExcursionName).all()
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


def get_user_excursions( user_id):  # НОВЫЙ запрос!
    """Возвращает все экскурсии пользователя: название, описание, дату"""
    session = SessionLocal()

    result = (session.query(ExcursionName.name, ExcursionName.description, ExcursionDate.date)
              .join(ExcursionDate, ExcursionName.id == ExcursionDate.excursion_name_id)
              .join(UserInExcursion, ExcursionDate.id == UserInExcursion.excursion_date_id)
              .filter(UserInExcursion.user_id == user_id).all())

    session.close()
    return result


def insert_user_in_excursion(user_id, excursion_date_id):
    session = SessionLocal()
    user_entry = UserInExcursion(user_id=user_id, excursion_date_id=excursion_date_id)
    session.add(user_entry)
    session.commit()
    session.close()


def reinit_scenario():
    drop_db(DB_NAME)
    create_db()
    insert_info_from_file(DB_NAME)


if __name__ == '__main__':
    from datetime import datetime

    reinit_scenario()

    print("Все экскурсии:", select_all_excursions())
    print("Все даты:", select_all_excursion_dates())

    # Тест нового запроса
    insert_user_in_excursion(12345, 1)  # пример
    print("Экскурсии пользователя 12345:", get_user_excursions(12345))
