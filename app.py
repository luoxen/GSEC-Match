"""
广东省体质健康管理学会 - 主应用
广州中考体育教练匹配平台
"""

import streamlit as st
from PIL import Image
import os
import base64
from supabase import create_client
from dotenv import load_dotenv
from src.utils.auth import init_session_state, login, logout, is_admin, is_logged_in

# 加载环境变量
load_dotenv()

# 初始化 Supabase 客户端
def init_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        st.warning("⚠️ 请配置 SUPABASE_URL 和 SUPABASE_KEY 环境变量")
        return None
    return create_client(url, key)

# 页面配置
st.set_page_config(
    page_title="广东省体质健康管理学会 - 广州中考体育教练匹配",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
init_session_state()

# 自定义CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .coach-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .price-tag-gold {
        background-color: #ffd700;
        color: #000;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .price-tag-silver {
        background-color: #c0c0c0;
        color: #000;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .price-tag-bronze {
        background-color: #cd7f32;
        color: #fff;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .login-box {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        max-width: 400px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

def get_logo_html():
    """获取会标图片的HTML"""
    logo_path = "学会会标.png"
    try:
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            return f'<img src="data:image/png;base64,{img_data}" style="height:50px; vertical-align:middle; margin-right:10px;">'
        else:
            return '<span style="font-size:40px; vertical-align:middle; margin-right:10px;">🏛️</span>'
    except Exception:
        return '<span style="font-size:40px; vertical-align:middle; margin-right:10px;">🏛️</span>'

def show_login():
    """登录界面"""
    st.markdown("### 🔐 管理员登录")
    
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            submitted = st.form_submit_button("登录", use_container_width=True)
            
            if submitted:
                if username and password:
                    supabase = init_supabase()
                    if supabase and login(supabase, username, password):
                        st.success("✅ 登录成功！")
                        st.rerun()
                    else:
                        st.error("❌ 用户名或密码错误")
                else:
                    st.warning("请输入用户名和密码")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    load_css()
    
    # 初始化 Supabase
    supabase = init_supabase()
    
    # 获取会标HTML
    logo_html = get_logo_html()
    
    # 显示标题和会标在同一行
    st.markdown(f"""
    <div style="text-align: center; padding: 10px;">
        {logo_html}
        <span style="font-size: 2.5rem; color: #1f77b4; font-weight: bold; vertical-align:middle;">广东省体质健康管理学会</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 副标题居中
    st.markdown("<h3 style='text-align: center;'>广州中考体育教练精准匹配平台</h3>", unsafe_allow_html=True)
    
    # 侧边栏
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 10px;">
        {logo_html}
        <br>
        <span style="font-size: 1.2rem; font-weight: bold; color: #1f77b4;">广东省体质健康管理学会</span>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    # ========== 权限控制 ==========
    # 根据用户角色显示不同菜单
    if is_admin():
        # 管理员：显示所有菜单
        menu = ["🏠 首页", "📝 教练注册", "👨‍👩‍👧 家长注册", "🔍 匹配教练", "👤 个人中心", "⚙️ 管理员"]
    else:
        # 普通用户：不显示管理员菜单
        menu = ["🏠 首页", "📝 教练注册", "👨‍👩‍👧 家长注册", "🔍 匹配教练", "👤 个人中心"]
    
    # 登录状态显示
    if is_logged_in():
        st.sidebar.success(f"✅ 已登录: {st.session_state.username}")
        if st.sidebar.button("🚪 登出"):
            logout()
            st.rerun()
    else:
        st.sidebar.info("🔐 未登录")
    
    st.sidebar.markdown("---")
    
    # 如果是管理员页面，检查登录状态
    choice = st.sidebar.radio("导航菜单", menu)
    
    # 页面路由
    if choice == "🏠 首页":
        show_home()
    elif choice == "📝 教练注册":
        show_coach_register(supabase)
    elif choice == "👨‍👩‍👧 家长注册":
        show_parent_register(supabase)
    elif choice == "🔍 匹配教练":
        show_match(supabase)
    elif choice == "👤 个人中心":
        show_profile(supabase)
    elif choice == "⚙️ 管理员":
        # 管理员页面需要登录验证
        if is_admin():
            show_admin(supabase)
        else:
            show_login()
    
    st.sidebar.markdown("---")
    st.sidebar.info("广东省体质健康管理学会 v1.0.0")

# ========== 其他函数保持不变 ==========
def show_home():
    # ... 首页内容 ...
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 注册教练", "50+", delta="+5 本月")
    with col2:
        st.metric("👨‍👩‍👧 服务家庭", "200+", delta="+20 本月")
    with col3:
        st.metric("⭐ 好评率", "98.5%", delta="+0.5%")
    
    st.markdown("---")
    st.markdown("### 🎯 平台特色")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **🎓 专业教练团队**
        - 🥇 金牌教练 (400元/课时)
        - 🥈 银牌教练 (300元/课时)  
        - 🥉 铜牌教练 (200元/课时)
        """)
    with col2:
        st.markdown("""
        **🏅 中考体育专项**
        - 必考: 800米/1000米 (30分)
        - 选考: 立定跳远、引体向上等 (20分)
        """)
    with col3:
        st.markdown("""
        **🕐 灵活时间安排**
        - 周末全天
        - 节假日
        - 晚间时段
        """)

def show_coach_register(supabase):
    # ... 教练注册代码（保持不变） ...
    st.markdown("### 📝 教练注册")
    # ... 完整代码 ...

def show_parent_register(supabase):
    # ... 家长注册代码（保持不变） ...
    st.markdown("### 👨‍👩‍👧 家长注册")
    # ... 完整代码 ...

def show_match(supabase):
    # ... 匹配教练代码（保持不变） ...
    st.markdown("### 🔍 匹配教练")
    # ... 完整代码 ...

def show_profile(supabase):
    st.markdown("### 👤 个人中心")
    st.info("个人中心开发中...")

def show_admin(supabase):
    # ... 管理员代码（保持不变） ...
    st.markdown("### ⚙️ 管理员")
    # ... 完整代码 ...

if __name__ == "__main__":
    main()
