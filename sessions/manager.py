"""
会话管理器
管理所有活跃会话
"""

from typing import Dict, Optional
from .models import ChessSession
import time


class SessionManager:
    """会话管理器类"""
    
    def __init__(self, session_timeout: int = 3600):
        """
        初始化会话管理器
        
        Args:
            session_timeout: 会话超时时间（秒）
        """
        self._sessions: Dict[str, ChessSession] = {}
        self._session_timeout = session_timeout
        self._last_access: Dict[str, float] = {}
    
    def get_session(self, session_id: str = "default") -> ChessSession:
        """
        获取或创建会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            会话对象
        """
        # 清理过期会话
        self._clean_expired()
        
        # 获取或创建会话
        if session_id not in self._sessions:
            self._sessions[session_id] = ChessSession(session_id)
        
        # 更新访问时间
        self._last_access[session_id] = time.time()
        
        return self._sessions[session_id]
    
    def clear_session(self, session_id: str):
        """
        清除指定会话
        
        Args:
            session_id: 会话ID
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
        if session_id in self._last_access:
            del self._last_access[session_id]
    
    def clear_all(self):
        """清除所有会话"""
        self._sessions.clear()
        self._last_access.clear()
    
    def _clean_expired(self):
        """清理过期会话"""
        current_time = time.time()
        expired = []
        
        for session_id, last_time in self._last_access.items():
            if current_time - last_time > self._session_timeout:
                expired.append(session_id)
        
        for session_id in expired:
            self.clear_session(session_id)
    
    def get_active_count(self) -> int:
        """获取活跃会话数量"""
        self._clean_expired()
        return len(self._sessions)
    
    def get_all_sessions(self) -> Dict[str, Dict]:
        """获取所有会话信息"""
        return {
            sid: session.to_dict() 
            for sid, session in self._sessions.items()
        }


# 全局会话管理器单例
session_manager = SessionManager()