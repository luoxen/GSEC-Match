"""
用户认证工具
"""
import streamlit as st
import hashlib
import time
from supabase import Client

def init_session_state():
    """初始化会话状态"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'guest'
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None

def login(supabase: Client, username: str, password: str) -> bool:
    """用户登录"""
    try:
        # 查询用户
        response = supabase.table('users').select('*').eq('username', username).execute()
        users = response.data
        
        if not users:
            return False
        
        user = users[0]
        
        # 验证密码（简单哈希，生产环境建议用 bcrypt）
        hashed = hashlib.sha256(password.encode()).hexdigest()
        if user['password_hash'] != hashed:
            return False
        
        # 设置会话状态
        st.session_state.logged_in = True
        st.session_state.user_role = user['role']
        st.session_state.user_id = user['id']
        st.session_state.username = user['username']
        
        return True
        
    except Exception as e:
        st.error(f"登录失败: {e}")
        return False

def logout():
    """用户登出"""
    st.session_state.logged_in = False
    st.session_state.user_role = 'guest'
    st.session_state.user_id = None
    st.session_state.username = None

def get_user_role() -> str:
    """获取当前用户角色"""
    return st.session_state.get('user_role', 'guest')

def is_admin() -> bool:
    """判断当前用户是否是管理员"""
    return st.session_state.get('user_role') == 'admin'

def is_logged_in() -> bool:
    """判断用户是否已登录"""
    return st.session_state.get('logged_in', False)

def require_admin():
    """需要管理员权限的装饰器"""
    if not is_admin():
        st.error("⚠️ 需要管理员权限")
        st.stop()
