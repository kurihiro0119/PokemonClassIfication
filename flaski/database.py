from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import Column, Integer, String, Boolean

# dbファイル名と保存先を指定する（同一フォルダにdata.dbというファイルを作成するため）
database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
engine = create_engine('sqlite:///' + database_file, convert_unicode=True, echo=True)
db_session = scoped_session(
                    sessionmaker(
                        autocommit = False,
                        autoflush  = False,
                        bind       = engine
                    )
				)
Base = declarative_base()
Base.query = db_session.query_property()

#クラス
class Pokemon(Base):
    # テーブル名の設定
    __tablename__ = "pokemon"
    # Column情報の設定
    pokemon_name       = Column(String, primary_key=True)    # ポケモン名
    type          = Column(String)                     # タイプ
    wiki_url        = Column(String)                      # WikipediaのURL
    picture_path    = Column(String)                      # ポケモン画像パス

# データベース作成
if __name__ == "__main__":
    # SQLiteを指定
    Base.metadata.create_all(engine)

    engine = create_engine('sqlite:///db.sqlite3', echo=True)
    Session = sessionmaker(bind=engine)
