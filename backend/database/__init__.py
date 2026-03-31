"""数据库模块初始化"""
from .db import get_db, close_db, init_db

__all__ = ['get_db', 'close_db', 'init_db']
