"""
广东省体质健康管理学会 - 主应用
广州中考体育教练匹配平台
"""

import streamlit as st
from PIL import Image
import os
import base64
import hashlib
import pandas as pd
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
    .sidebar-login-btn {
        width: 100%;
        padding: 0.5rem;
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-align: center;
        font-weight: bold;
    }
    .sidebar-login-btn:hover {
        background-color: #155a8a;
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
    """管理员登录界面"""
    st.markdown("### 🔐 管理员登录")
    
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        with st.form("admin_login_form"):
            username = st.text_input("管理员用户名", placeholder="请输入管理员用户名")
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
    
    # ========== 侧边栏 ==========
    with st.sidebar:
        # 会标
        st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            {logo_html}
            <br>
            <span style="font-size: 1.2rem; font-weight: bold; color: #1f77b4;">广东省体质健康管理学会</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # ========== 菜单定义 ==========
        if is_admin():
            # 管理员：显示所有菜单（包含管理员）
            menu = ["🏠 首页", "📝 教练注册", "👨‍👩‍👧 家长注册", "🔍 匹配教练", "⚙️ 管理员"]
        else:
            # 普通用户：不显示管理员菜单
            menu = ["🏠 首页", "📝 教练注册", "👨‍👩‍👧 家长注册", "🔍 匹配教练"]
        
        # ========== 登录状态显示 ==========
        if is_logged_in():
            st.success(f"✅ 已登录: {st.session_state.username}")
            if st.button("🚪 登出", use_container_width=True):
                logout()
                st.rerun()
        else:
            if st.button("🔐 管理员登录", use_container_width=True):
                st.query_params["page"] = "管理员"
                st.rerun()
            st.caption("💡 管理员请点击上方按钮登录")
        
        st.markdown("---")
        
        # ========== 菜单选择 ==========
        if st.query_params.get("page") == "管理员":
            choice = "⚙️ 管理员"
        else:
            choice = st.selectbox(
                "📋 导航菜单",
                menu,
                index=0,
                key="main_navigation"
            )
    
    # ========== 页面路由 ==========
    if choice == "🏠 首页":
        show_home()
    elif choice == "📝 教练注册":
        show_coach_register(supabase)
    elif choice == "👨‍👩‍👧 家长注册":
        show_parent_register(supabase)
    elif choice == "🔍 匹配教练":
        show_match(supabase)
    elif choice == "⚙️ 管理员":
        if is_admin():
            show_admin(supabase)
        else:
            show_login()
    
    st.sidebar.markdown("---")
    st.sidebar.info("广东省体质健康管理学会 v1.0.0")

def show_home():
    """首页"""
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
    """教练注册 - 公开访问，不需要登录"""
    st.markdown("### 📝 教练注册")
    
    if supabase is None:
        st.error("⚠️ 数据库未连接，请稍后重试")
        return
    
    with st.form("coach_form"):
        st.subheader("基本信息")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("姓名*", placeholder="请输入真实姓名")
            phone = st.text_input("手机号码*", placeholder="请输入手机号")
            gender = st.selectbox("性别", ["男", "女"])
        with col2:
            age = st.number_input("年龄", min_value=18, max_value=65, value=25)
            email = st.text_input("邮箱", placeholder="请输入邮箱地址")
        
        st.subheader("专业信息")
        col1, col2 = st.columns(2)
        with col1:
            major = st.text_input("专业*", placeholder="体育教育/运动训练等")
            school = st.text_input("毕业院校*", placeholder="请输入毕业院校")
        with col2:
            experience = st.selectbox("教学经验", ["1-3年", "3-5年", "5-10年", "10年以上"])
            specialty = st.multiselect(
                "擅长项目",
                ["800米", "1000米", "立定跳远", "引体向上", "仰卧起坐", "跳绳", "实心球", "篮球", "足球", "排球"]
            )
        
        st.subheader("教练等级")
        level = st.selectbox(
            "选择教练等级",
            ["🥉 铜牌教练 (200元/课时)", "🥈 银牌教练 (300元/课时)", "🥇 金牌教练 (400元/课时)"]
        )
        
        st.subheader("个人介绍")
        bio = st.text_area("自我介绍", placeholder="请介绍您的教学经验和特长", height=150)
        
        st.subheader("可授课时间")
        available_times = st.multiselect(
            "选择可授课时段",
            ["周六上午", "周六下午", "周日上午", "周日下午", "节假日", "晚间 (19:00-21:00)"]
        )
        
        submitted = st.form_submit_button("提交注册")
        
        if submitted:
            if not all([name, phone, major, school]):
                st.error("请填写所有必填信息（带*号）")
            else:
                level_name = level.split()[0].replace("🥉", "").replace("🥈", "").replace("🥇", "").strip()
                price = int(level.split("(")[1].split("元")[0])
                
                coach_data = {
                    "name": name,
                    "phone": phone,
                    "gender": gender,
                    "age": age,
                    "email": email,
                    "major": major,
                    "school": school,
                    "experience": experience,
                    "specialty": ",".join(specialty),
                    "level": level_name,
                    "price": price,
                    "bio": bio,
                    "available_times": ",".join(available_times),
                    "status": "待审核"
                }
                
                try:
                    response = supabase.table('coaches').insert(coach_data).execute()
                    st.success("✅ 注册成功！请等待管理员审核")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ 注册失败: {e}")

def show_parent_register(supabase):
    """家长注册 - 公开访问，不需要登录"""
    st.markdown("### 👨‍👩‍👧 家长注册")
    
    if supabase is None:
        st.error("⚠️ 数据库未连接，请稍后重试")
        return
    
    with st.form("parent_form"):
        st.subheader("👤 家长信息")
        col1, col2 = st.columns(2)
        with col1:
            parent_name = st.text_input("家长姓名*", placeholder="请输入姓名")
            parent_phone = st.text_input("家长手机号*", placeholder="请输入手机号")
            parent_gender = st.selectbox("家长性别", ["男", "女"])
        with col2:
            parent_age = st.number_input("家长年龄", min_value=20, max_value=80, value=35)
            parent_email = st.text_input("家长邮箱", placeholder="请输入邮箱")
        
        st.subheader("👦 孩子信息")
        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input("孩子姓名*", placeholder="请输入姓名")
            student_gender = st.selectbox("孩子性别", ["男", "女"])
            student_age = st.number_input("孩子年龄", min_value=10, max_value=18, value=15)
        with col2:
            student_grade = st.selectbox("年级", ["初一", "初二", "初三"])
            district = st.selectbox("所在区", [
                "越秀区", "海珠区", "荔湾区", "天河区", "白云区", 
                "黄埔区", "番禺区", "花都区", "南沙区", "从化区", "增城区"
            ])
            school = st.text_input("所在学校*", placeholder="请输入学校名称")
        
        st.subheader("🏃 体育信息")
        sports_interest = st.multiselect(
            "体育爱好",
            ["篮球", "足球", "游泳", "田径", "羽毛球", "乒乓球", "排球", "其他"]
        )
        weak_sports = st.multiselect(
            "中考体育项目短板",
            ["800米", "1000米", "立定跳远", "引体向上", "仰卧起坐", "跳绳", "实心球", "篮球", "足球", "排球"]
        )
        
        st.subheader("🎯 训练需求")
        training_goal = st.text_area("训练目标", placeholder="请描述您的训练目标", height=100)
        preferred_time = st.multiselect(
            "偏好训练时间",
            ["周六上午", "周六下午", "周日上午", "周日下午", "节假日", "晚间 (19:00-21:00)"]
        )
        budget = st.selectbox("预算范围", ["200-300元/课时", "300-400元/课时", "400元以上/课时"])
        
        submitted = st.form_submit_button("提交注册")
        
        if submitted:
            if not all([parent_name, parent_phone, student_name, school]):
                st.error("请填写所有必填信息（带*号）")
            else:
                parent_data = {
                    "parent_name": parent_name,
                    "parent_phone": parent_phone,
                    "parent_gender": parent_gender,
                    "parent_age": parent_age,
                    "parent_email": parent_email,
                    "student_name": student_name,
                    "student_gender": student_gender,
                    "student_age": student_age,
                    "student_grade": student_grade,
                    "district": district,
                    "school": school,
                    "sports_interest": ",".join(sports_interest),
                    "weak_sports": ",".join(weak_sports),
                    "training_goal": training_goal,
                    "preferred_time": ",".join(preferred_time),
                    "budget": budget
                }
                
                try:
                    response = supabase.table('parents').insert(parent_data).execute()
                    st.success("✅ 注册成功！我们正在为您匹配合适的教练")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ 注册失败: {e}")

def show_match(supabase):
    """匹配教练 - 从 Supabase 读取真实数据，公开访问"""
    st.markdown("### 🔍 匹配教练")
    
    if supabase is None:
        st.error("⚠️ 数据库未连接，请配置环境变量")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sport_filter = st.selectbox("项目", ["全部", "800米", "1000米", "立定跳远", "引体向上", "仰卧起坐", "跳绳"])
    with col2:
        level_filter = st.selectbox("教练等级", ["全部", "金牌", "银牌", "铜牌"])
    with col3:
        district_filter = st.selectbox("区域", ["全部", "越秀区", "海珠区", "荔湾区", "天河区", "白云区"])
    
    try:
        query = supabase.table('coaches').select('*').eq('status', '已通过')
        
        if level_filter != "全部":
            query = query.eq('level', level_filter)
        
        response = query.execute()
        coaches = response.data
        
        if sport_filter != "全部":
            coaches = [c for c in coaches if sport_filter in c.get('specialty', '')]
        
        st.markdown("---")
        st.markdown(f"### 📋 推荐教练 ({len(coaches)}位)")
        
        if coaches:
            for coach in coaches:
                with st.container():
                    level_class = "gold" if coach['level'] == "金牌" else "silver" if coach['level'] == "银牌" else "bronze"
                    rating_display = f"⭐ {coach.get('rating', 0):.1f}" if coach.get('rating', 0) > 0 else "🆕 新教练"
                    
                    st.markdown(f"""
                    <div class='coach-card'>
                        <b>{coach['name']}</b> 
                        <span class='price-tag-{level_class}'>{coach['level']}</span>
                        {rating_display}
                        <br>
                        💰 {coach['price']}元/课时
                        <br>
                        🏃 擅长: {coach.get('specialty', '未填写')}
                        <br>
                        📝 {coach.get('bio', '')[:100]}{'...' if len(coach.get('bio', '')) > 100 else ''}
                        <br>
                        📅 可授课: {coach.get('available_times', '未填写')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"📅 预约 {coach['name']}", key=f"book_{coach['id']}"):
                        st.info(f"正在预约 {coach['name']}，请等待确认...")
        else:
            st.info("😅 暂无符合条件的教练，请调整筛选条件")
            
    except Exception as e:
        st.error(f"❌ 加载教练数据失败: {e}")
        st.info("💡 提示: 请确保已连接 Supabase 并添加了教练数据")

def show_admin(supabase):
    """管理员 - 教练审核 + 教练管理 + 家长管理"""
    st.markdown("### ⚙️ 管理员")
    st.warning("⚠️ 仅限管理员访问")
    
    if supabase is None:
        st.error("⚠️ 数据库未连接，请配置环境变量")
        return
    
    # 添加更多标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📋 教练审核", "👨‍🏫 教练管理", "👨‍👩‍👧 家长管理", "📊 数据统计"])
    
    # ========== Tab 1: 教练审核 ==========
    with tab1:
        st.markdown("#### 待审核教练")
        
        try:
            response = supabase.table('coaches').select('*').eq('status', '待审核').execute()
            pending_coaches = response.data
            
            if pending_coaches:
                for coach in pending_coaches:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                        with col1:
                            st.write(f"**{coach['name']}**")
                            st.caption(f"📱 {coach['phone']}")
                        with col2:
                            st.write(f"等级: {coach['level']}")
                            st.write(f"价格: {coach['price']}元/课时")
                        with col3:
                            st.write(f"专业: {coach['major']}")
                            st.write(f"经验: {coach['experience']}")
                        with col4:
                            if st.button(f"✅ 通过", key=f"approve_{coach['id']}"):
                                try:
                                    supabase.table('coaches').update({'status': '已通过'}).eq('id', coach['id']).execute()
                                    st.success(f"✅ {coach['name']} 已通过审核")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"操作失败: {e}")
                            
                            if st.button(f"❌ 拒绝", key=f"reject_{coach['id']}"):
                                try:
                                    supabase.table('coaches').update({'status': '已拒绝'}).eq('id', coach['id']).execute()
                                    st.success(f"❌ {coach['name']} 已拒绝")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"操作失败: {e}")
                        st.markdown("---")
            else:
                st.info("✅ 暂无待审核教练")
                
        except Exception as e:
            st.error(f"加载数据失败: {e}")
    
    # ========== Tab 2: 教练管理 ==========
    with tab2:
        st.markdown("#### 所有教练")
        
        try:
            response = supabase.table('coaches').select('*').execute()
            coaches = response.data
            
            if coaches:
                df = pd.DataFrame(coaches)
                
                display_columns = ['name', 'phone', 'level', 'price', 'status', 'created_at']
                available_columns = [col for col in display_columns if col in df.columns]
                
                rename_map = {
                    'name': '姓名',
                    'phone': '手机号',
                    'level': '等级',
                    'price': '价格(元)',
                    'status': '状态',
                    'created_at': '注册时间'
                }
                df_display = df[available_columns].rename(columns=rename_map)
                
                st.dataframe(df_display, use_container_width=True)
                st.caption(f"共 {len(coaches)} 位教练")
            else:
                st.info("暂无教练数据")
                
        except Exception as e:
            st.error(f"加载教练数据失败: {e}")
    
    # ========== Tab 3: 家长管理 ==========
    with tab3:
        st.markdown("#### 所有家长")
        
        try:
            response = supabase.table('parents').select('*').execute()
            parents = response.data
            
            if parents:
                df = pd.DataFrame(parents)
                
                display_columns = ['parent_name', 'parent_phone', 'student_name', 'student_grade', 'district', 'school', 'created_at']
                available_columns = [col for col in display_columns if col in df.columns]
                
                rename_map = {
                    'parent_name': '家长姓名',
                    'parent_phone': '家长手机',
                    'student_name': '孩子姓名',
                    'student_grade': '年级',
                    'district': '所在区',
                    'school': '学校',
                    'created_at': '注册时间'
                }
                df_display = df[available_columns].rename(columns=rename_map)
                
                st.dataframe(df_display, use_container_width=True)
                st.caption(f"共 {len(parents)} 位家长")
            else:
                st.info("暂无家长数据")
                
        except Exception as e:
            st.error(f"加载家长数据失败: {e}")
    
    # ========== Tab 4: 数据统计 ==========
    with tab4:
        st.markdown("#### 数据统计")
        
        try:
            coaches_count = supabase.table('coaches').select('*', count='exact').execute()
            parents_count = supabase.table('parents').select('*', count='exact').execute()
            matches_count = supabase.table('matches').select('*', count='exact').execute()
            payments_count = supabase.table('payments').select('*', count='exact').execute()
            reviews_count = supabase.table('reviews').select('*', count='exact').execute()
            
            stats = {
                '表名': ['教练', '家长', '匹配记录', '支付记录', '评价'],
                '数量': [
                    coaches_count.count,
                    parents_count.count,
                    matches_count.count,
                    payments_count.count,
                    reviews_count.count
                ]
            }
            df_stats = pd.DataFrame(stats)
            st.dataframe(df_stats, use_container_width=True)
            
            level_response = supabase.table('coaches').select('level', 'status').execute()
            if level_response.data:
                df_level = pd.DataFrame(level_response.data)
                if 'level' in df_level.columns:
                    level_counts = df_level['level'].value_counts().reset_index()
                    level_counts.columns = ['等级', '数量']
                    st.markdown("---")
                    st.markdown("#### 教练等级分布")
                    st.dataframe(level_counts, use_container_width=True)
                
        except Exception as e:
            st.error(f"加载统计数据失败: {e}")

if __name__ == "__main__":
    main()
