import sqlite3
from abc import ABCMeta, abstractmethod
from lib.generic import typehint
from lib.config import Config

config = Config()
config.parse()


class Database:

    class Methods(object,metaclass=ABCMeta):

        def __init__(self,name=config.db_name):
            self.__db = sqlite3.connect(name)

        @abstractmethod
        def delete(self):
            pass

        @abstractmethod
        @typehint
        def drop(self) -> None:
            if self.table_exists():
                cursor = self.__db.cursor()
                cursor.execute('DROP TABLE %s' % (
                    self.__class__.__name__.lower(),))
                self.__db.commit()
        
        @abstractmethod
        @typehint
        def create(self, sql: str) -> None:
            if not self.table_exists():
                self.__db.cursor().execute(sql)
                self.__db.cursor().execute("PRAGMA foreign_keys = ON")
                self.__db.cursor().execute("PRAGMA synchronous = OFF")
                self.__db.cursor().execute("PRAGMA journal_mode = MEMORY")
                self.__db.commit()

        def conn(self):
            return self.__db
       
        def sql(self, *args) -> None:
            self.conn().cursor().execute(*args)
            self.conn().commit()

        @abstractmethod
        def all(self):
            pass

        @abstractmethod
        def add(self):
            pass

        def delete(self):
            self.sql('DELETE FROM key WHERE key = ?', (key,))

        @typehint
        def table_exists(self) -> bool:
                cursor = self.__db.cursor()
                cursor.execute('''
                        SELECT name 
                        FROM sqlite_master 
                        WHERE type="table" AND 
                        name="%s" ''' % (self.__class__.__name__.lower(),)
                        )
                return bool(cursor.fetchone())