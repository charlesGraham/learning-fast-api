import database
import models

def init_db():
  models.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
  init_db()