from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import JSON
from server.database.mysqlDB import Base
# declarative base class


class PolicyModel(Base):
    __tablename__ = "iam_policy"
    name = Column(String(64), primary_key=True)
    description = Column(String(512), nullable=True, default="No description")
    policy = Column(JSON, nullable=False)
    expanded_policy = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Policy(name={self.name}, description={self.description}"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "policy": self.policy,
            "expanded_policy": self.expanded_policy
        }


class GroupModel(Base):
    __tablename__ = "iam_group"
    name = Column(String(64), primary_key=True)
    description = Column(String(64), nullable=True, default="No description")
    policy = Column(String(64), ForeignKey("iam_policy.name"), nullable=False)

    def __repr__(self):
        return f"<Group(name={self.name}, description={self.description}, policy={self.policy})"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "policy": self.policy,
        }


class UserModel(Base):
    __tablename__ = "iam_user"
    email = Column(String(128), primary_key=True)
    name = Column(String(64), nullable=False)
    group = Column(String(64), ForeignKey("iam_group.name"), nullable=False)

    def __repr__(self):
        return f"<User(email={self.email}, name={self.name}, group={self.group})"

    def to_dict(self):
        return {
            "email": self.email,
            "name": self.name,
            "group": self.group,
        }


class APIKeyModel(Base):
    __tablename__ = "iam_apikey"
    key_id = Column(String(128), primary_key=True)
    key_value = Column(String(256), nullable=False)
    key_salt = Column(String(256), nullable=False)
    key_group = Column(String(64), ForeignKey("iam_group.name"), nullable=False)
    key_owner = Column(String(128), ForeignKey("iam_user.email"), nullable=False)
    key_rate_limit = Column(String(128), nullable=False, default="3")
    key_last_time_used = Column(DateTime(), nullable=False)


    def __repr__(self):
        return f"<APIKey(key_id={self.key_id}, key_secret={self.key_value}, key_group={self.key_group})"

    def to_dict(self):
        return {
            "key_id": self.key_id,
            "key_value": self.key_value,
            "key_salt": self.key_salt,
            "key_group": self.key_group,
            "key_owner": self.key_owner,
            "key_rate_limit": self.key_rate_limit,
            "key_last_time_used": self.key_last_time_used.strftime("%m/%d/%Y %H:%M:%S")
        }


class IAMCustomerModel(Base):
    __tablename__ = "iam_customer"
    id = Column(String(64), primary_key=True)
    name = Column(String(64), nullable=False)
    config = Column(JSON(), nullable=False)

    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name}, config={self.config})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "config": self.config,
        }