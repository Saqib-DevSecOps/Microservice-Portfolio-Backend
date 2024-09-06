from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from passlib.hash import bcrypt

from app.database import Base


class User(Base):
    """
    A professional user model for FastAPI portfolio application.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(128))
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def verify_password(self, password: str) -> bool:
        """
        Verify the hashed password using bcrypt.
        """
        return bcrypt.verify(password, self.hashed_password)

    def set_password(self, password: str):
        """
        Hash and set the password using bcrypt.
        """
        self.hashed_password = bcrypt.hash(password)



