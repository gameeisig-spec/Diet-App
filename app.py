import streamlit as st
from PIL import Image

# --- 頁面設定 ---
st.set_page_config(page_title="AI 燃脂教練", layout="wide")

# --- 5. 運動風格 CSS 設計 (深色底 + 螢光橘/綠) ---
st.markdown("""
<style>
    /* 整個背景改成深色 */
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    /* 標題改成運動風的粗斜體 + 螢光橘 */
    h1, h2, h3 {
        color: #FF5722 !important; 
        font-weight: 900 !important;
        font-style: italic;
    }
    /* 按鈕設計 */
    .stButton>button {
        background-color: #FF5722;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #E64A19;
        color: white;
        border: 1px solid white;
    }
    /* 數據顯示改成螢光綠 */
    div[data-testid="stMetricValue"] {
        color: #00E676; 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 初始化「今日總結」的記憶功能 ---
if 'total_cals' not in st.session_state:
    st.session_state.total_cals = 0
if 'total_protein' not in st.session_state:
    st.session_state.total_protein = 0
if 'total_sodium' not in st.session_state:
    st.session_state.total_sodium = 0
if 'show_camera' not in st.session_state:
    st.session_state.show_camera = False

# --- 營養需求計算公式 ---
def calculate_tdee(age, weight, height, gender, activity_level):
    if gender == '男':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    activity_multiplier = {'低活動量': 1.2, '中活動量': 1.55, '高活動量': 1.725}
    return bmr * activity_multiplier[activity_level]

st.title("⚡ AI 燃脂教練 & 營養追蹤")

# --- 側邊欄：個人資訊與目標 ---
with st.sidebar:
    st.header("👤 你的運動檔案")
    age = st.number_input("年齡", min_value=10, max_value=100, value=25)
    gender = st.selectbox("性別", ["男", "女"])
    weight = st.number_input("體重 (kg)", min_value=30.0, max_value=200.0, value=65.0)
    height = st.number_input("身高 (cm)", min_value=100.0, max_value=250.0, value=170.0)
    activity = st.selectbox("活動量", ["低活動量", "中活動量", "高活動量"])
    
    # 計算每日目標
    tdee = int(calculate_tdee(age, weight, height, gender, activity))
    goal_protein = int(weight * 1.5)
    goal_sodium = 2300
    goal_water = int(weight * 35) # 4. 加入每日水分需求 (體重 x 35ml)

    st.markdown("---")
    st.subheader("🎯 每日作戰目標")
    st.info(f"🔥 熱量上限：{tdee} kcal\n\n💪 蛋白質：{goal_protein} g\n\n💧 水分攝取：{goal_water} ml\n\n🧂 鈉含量：低於 {goal_sodium} mg")

# --- 建立上方頁籤 (切換紀錄與總結) ---
tab1, tab2 = st.tabs(["📸 紀錄新餐點", "📊 今日戰績 (總結)"])

# ====== 頁籤 1：紀錄新餐點 ======
with tab1:
    st.header("🥊 新增一餐")
    
    # 1. 拍照功能隱藏，點擊按鈕才顯示
    if st.button("📸 點我開啟相機 / 上傳照片"):
        st.session_state.show_camera = not st.session_state.show_camera
        
    if st.session_state.show_camera:
        uploaded_file = st.file_uploader("請選擇照片或拍照", type=["jpg", "png", "jpeg"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='掃描中...', use_container_width=True)
            
            with st.spinner('⚡ AI 教練正在解析這份餐點...'):
                # 這裡未來會接真實 AI，目前以模擬數字示範
                food_cals = 750
                food_protein = 35
                food_sodium = 1200
                
            st.subheader("📋 營養成分估算")
            c1, c2, c3 = st.columns(3)
            c1.metric("熱量", f"{food_cals} kcal")
            c2.metric("蛋白質", f"{food_protein} g")
            c3.metric("鈉含量", f"{food_sodium} mg")
            
            # 2. 額度計算機功能：提前警告
            st.subheader("⚖️ 額度計算機")
            rem_cals = tdee - st.session_state.total_cals - food_cals
            
            if rem_cals < 0:
                st.error(f"⚠️ 【教練警告】如果吃下這餐，你今天的熱量會超標 {abs(rem_cals)} 大卡！建議減半份量或改吃別的。")
            else:
                st.success(f"✅ 【安全過關】吃完這餐後，今天熱量還剩下 {rem_cals} 大卡的扣打。")

            # 確認按鈕：把這餐的數值加到今天總結裡
            if st.button("➕ 確認吃這餐！(加入今日戰績)"):
                st.session_state.total_cals += food_cals
                st.session_state.total_protein += food_protein
                st.session_state.total_sodium += food_sodium
                st.session_state.show_camera = False # 紀錄完自動收起相機
                st.success("✅ 已成功記錄！請切換到「今日戰績」查看進度。")
                st.rerun() # 重新整理畫面

# ====== 頁籤 2：今日總結與重置 ======
with tab2:
    st.header("🏆 今天的戰鬥表現")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("🔥 總熱量 (kcal)")
        # 顯示已攝取，並計算剩餘額度 (delta)
        st.metric("已攝取 / 目標", f"{st.session_state.total_cals} / {tdee}", 
                  delta=f"剩餘 {tdee - st.session_state.total_cals} kcal", delta_color="inverse")
        
        st.subheader("💪 蛋白質 (g)")
        st.metric("已攝取 / 目標", f"{st.session_state.total_protein} / {goal_protein}", 
                  delta=f"還差 {max(0, goal_protein - st.session_state.total_protein)} g")

    with col_t2:
        st.subheader("💧 喝水進度 (ml)")
        st.info(f"今日目標：{goal_water} ml\n(請記得隨時補充水分！)")
        
        st.subheader("🧂 鈉含量 (mg)")
        st.metric("已攝取 / 上限", f"{st.session_state.total_sodium} / {goal_sodium}", 
                  delta=f"剩餘 {goal_sodium - st.session_state.total_sodium} mg", delta_color="inverse")

    st.markdown("---")
    # 3. 提供一鍵重置當日數據的功能
    if st.button("🔄 新的一天！重置所有紀錄"):
        st.session_state.total_cals = 0
        st.session_state.total_protein = 0
        st.session_state.total_sodium = 0
        st.success("✅ 紀錄已清空，今天也要繼續保持熱血！")
        st.rerun()

