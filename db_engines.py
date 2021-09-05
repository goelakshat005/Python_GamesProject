import logging
import os
import sqlalchemy
import sqlalchemy_utils as sa_utils

ENGINE_KEY = 'SQLALCHEMY_ENGINE'
USER_KEY = 'USER'
PASSWORD_KEY = 'PASSWORD'
HOST_KEY = 'HOST'
PORT_KEY = 'PORT'
DBNAME_KEY = 'NAME'

class DBEngines:
	"""Database Engeine Manager.

		This class creates and keep database engines.
		It can be used as a singleton class, by calling the get_instance()
		to get the static instance.  Extra copies can also be created as needed.
	"""

	# Singleton instance
	_INSTANCE_ = None

	def __init__(self):
		self.db_engines = dict()      # singleton as need to keep engines list common

	@classmethod
	def get_instance(cls):
		"""Get the singleton instance."""
		if not cls._INSTANCE_:
			cls._INSTANCE_ = DBEngines()
		return cls._INSTANCE_

	@classmethod
	def create_engine(cls, db: dict, create_db: bool = False):
		"""Create a database engine."""
		print(db)
		url = sqlalchemy.engine.url.URL(
			drivername=db[ENGINE_KEY],
			username=db[USER_KEY],
			password=db[PASSWORD_KEY],
			host=db[HOST_KEY],
			port=db[PORT_KEY],
			database=db[DBNAME_KEY]
		)
		engine = sqlalchemy.create_engine(url)

		# Check if the database exists
		if not sa_utils.database_exists(engine.url):
			if create_db:
				cls.create_database(engine)
			else:
				raise Exception(f"Database does not exist - {url}")
		return engine

	@classmethod
	def create_database(cls, engine):
		if sa_utils.database_exists(engine.url):
			print("Database already exists: {}".format(engine.url))
		else:
			print("Creating database: {}".foramt(engine.url))
			sa_utils.create_database(engine.url)
		if not sa_utils.database_exists(engine.url):
			raise Exception(f"Failed to create database: {engine.url}")

	@classmethod
	def database_exists(cls, engine):
		return sa_utils.database_exists(engine.url)

	def get_engine(self, db: dict, create_db: bool = False):
		"""Get a DB engine based on the connection specification."""
		name = db['NAME']
		if name in self.db_engines:
			engine = self.db_engines[name]
		else:
			engine = self.create_engine(db, create_db)
			self.db_engines[name] = engine
		return engine