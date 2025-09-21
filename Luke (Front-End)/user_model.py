from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base
import datetime as dt

Base=declarative_base()

class User(Base):
    __tablename__="Users"

    id=Column("id", Integer, primary_key=True, autoincrement=True)
    Name=Column("Name", String, nullable=False)
    Username=Column("Username", String, nullable=False)
    Password=Column("Password", Integer, nullable=False)
    MySkills=Column("MySkills", String, nullable=False, default="None")
    NeededSkills=Column("NeededSkills", String,nullable=False, default="None")
    Schedule=Column("Schedule",String,nullable=False, default="000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    data_created=Column("date_created", Date, nullable=False, default=dt.datetime.utcnow)
    current_Matches=Column("CurrentMatches",String, nullable=False, default="None")
    