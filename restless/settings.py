from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


Base = declarative_base()

dbtype = "mysql+pymysql"
dbuser = "root"
dbpass = ""
dbhost = "localhost"
dbname = "restless"

dbstring = "{dbtype}://{user}:{dbpass}@{host}/{name}".format(dbtype=dbtype,
                                                             user=dbuser,
                                                             dbpass=dbpass,
                                                             host=dbhost,
                                                             name=dbname)
engine = create_engine(dbstring)
session = Session(engine)
