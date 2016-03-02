"""Real Name을 위한 초석입니다! 단계 2. 이름이 될 값을 기존 값들을 통해 만듭니다.

Revision ID: 57a8604ea770
Revises: f836b8597d20
Create Date: 2016-03-02 12:33:41.232775

"""

# revision identifiers, used by Alembic.
revision = '57a8604ea770'
down_revision = 'f836b8597d20'

import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Base = declarative_base()
N = 50

class User(Base):
    __tablename__ = 'user'
    username = sa.Column(sa.String(N), primary_key=True)
    password_hash = sa.Column(sa.String(N + 10), nullable=False)
    realname = sa.Column(sa.String(N), nullable=False)
    first_name_kr = sa.Column(sa.String(N), nullable=False)
    last_name_kr = sa.Column(sa.String(N), nullable=False)
    first_name_en = sa.Column(sa.String(N), nullable=False)
    middle_name_en = sa.Column(sa.String(N))
    last_name_en = sa.Column(sa.String(N), nullable=False)
    student_number = sa.Column(sa.Integer, nullable=False)
    last_login = sa.Column(sa.DateTime, nullable=False)


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    for user in session.query(User):
        user.realname = user.last_name_kr + user.first_name_kr

    session.commit()

def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    for user in session.query(User):
        user.realname = ""

    session.commit()

    pass
