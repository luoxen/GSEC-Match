"""
广东省体质健康管理学会 - 主应用
广州中考体育教练匹配平台
"""

import streamlit as st
from PIL import Image
import os

# 页面配置
st.set_page_config(
    page_title="广东省体质健康管理学会 - 广州中考体育教练匹配",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 10px;
    }
    .header-logo {
        display: inline-block;
        vertical-align: middle;
    }
    .header-title {
        display: inline-block;
        vertical-align: middle;
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    # 显示学会会标和标题在同一行
    logo_path = "/Users/Admin/Documents/运动营养+抗衰老/中考体育/学会会标.png"
    
    # 使用HTML让图片和标题在同一行
    logo_html = ""
    try:
        if os.path.exists(logo_path):
            import base64
            with open(logo_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{img_data}" style="height:60px; vertical-align:middle; margin-right:10px;">'
        else:
            logo_html = '<span style="font-size:40px; vertical-align:middle; margin-right:10px;">🏛️</span>'
    except Exception:
        logo_html = '<span style="font-size:40px; vertical-align:middle; margin-right:10px;">🏛️</span>'
    
    # 标题和图标在同一行
    st.markdown(f"""
    <div style="text-align: center; padding: 10px;">
        {logo_html}
        <span style="font-size: 2.5rem; color: #1f77b4; font-weight: bold; vertical-align:middle;">广东省体质健康管理学会</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 副标题居中
    st.markdown("<h3 style='text-align: center;'>广州中考体育教练精准匹配平台</h3>", unsafe_allow_html=True)
    
    # 侧边栏导航
    st.sidebar.title("🏛️ 广东省体质健康管理学会")
    st.sidebar.markdown("---")
    
    menu = ["🏠 首页", "📝 教练注册", "👨‍👩‍👧 家长注册", "🔍 匹配教练", "👤 个人中心", "⚙️ 管理员"]
    choice = st.sidebar.radio("导航菜单", menu)
    
    if choice == "🏠 首页":
        show_home()
    elif choice == "📝 教练注册":
        show_coach_register()
    elif choice == "👨‍👩‍👧 家长注册":
        show_parent_register()
    elif choice == "🔍 匹配教练":
        show_match()
    elif choice == "👤 个人中心":
        show_profile()
    elif choice == "⚙️ 管理员":
        show_admin()
    
    st.sidebar.markdown("---")
    st.sidebar.info("广东省体质健康管理学会 v1.0.0")

def show_home():
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

def show_coach_register():
    st.markdown("### 📝 教练注册")
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
                st.success("✅ 注册成功！请等待管理员审核")
                st.balloons()

def show_parent_register():
    st.markdown("### 👨‍👩‍👧 家长注册")
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
                st.success("✅ 注册成功！我们正在为您匹配合适的教练")
                st.balloons()

def show_match():
    st.markdown("### 🔍 匹配教练")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sport = st.selectbox("项目", ["全部", "800米", "1000米", "立定跳远", "引体向上", "仰卧起坐", "跳绳"])
    with col2:
        level = st.selectbox("教练等级", ["全部", "金牌", "银牌", "铜牌"])
    with col3:
        district = st.selectbox("区域", ["全部", "越秀区", "海珠区", "荔湾区", "天河区", "白云区"])
    
    if st.button("🔍 搜索教练"):
        st.success("搜索完成！")
    
    st.markdown("---")
    st.markdown("### 📋 推荐教练")
    
    coaches = [
        {"name": "王教练", "level": "金牌", "price": 400, "rating": "⭐ 4.9", "specialty": "800米, 1000米", "district": "天河区"},
        {"name": "李教练", "level": "银牌", "price": 300, "rating": "⭐ 4.7", "specialty": "立定跳远, 跳绳", "district": "越秀区"},
        {"name": "张教练", "level": "铜牌", "price": 200, "rating": "⭐ 4.5", "specialty": "引体向上, 仰卧起坐", "district": "海珠区"},
    ]
    
    for coach in coaches:
        with st.container():
            level_class = "gold" if coach['level'] == "金牌" else "silver" if coach['level'] == "银牌" else "bronze"
            st.markdown(f"""
            <div class='coach-card'>
                <b>{coach['name']}</b> 
                <span class='price-tag-{level_class}'>{coach['level']}</span>
                {coach['rating']}
                <br>
                💰 {coach['price']}元/课时 | 📍 {coach['district']}
                <br>
                🏃 擅长: {coach['specialty']}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"📅 预约 {coach['name']}", key=f"book_{coach['name']}"):
                st.info(f"正在预约 {coach['name']}...")

def show_profile():
    st.markdown("### 👤 个人中心")
    st.info("个人中心开发中...")

def show_admin():
    st.markdown("### ⚙️ 管理员")
    st.warning("⚠️ 仅限管理员访问")
    
    tab1, tab2, tab3 = st.tabs(["教练审核", "订单管理", "数据统计"])
    with tab1:
        st.dataframe({
            "姓名": ["赵教练", "刘教练", "陈教练"],
            "手机": ["138****1234", "139****5678", "137****9012"],
            "等级": ["金牌", "银牌", "铜牌"],
            "状态": ["待审核", "待审核", "已通过"]
        })
        if st.button("审核通过"):
            st.success("审核完成！")

if __name__ == "__main__":
    main()
