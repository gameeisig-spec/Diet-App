import streamlit as st
from PIL import Image

# --- 1. 營養需求計算公式 (Mifflin-St Jeor) ---
def calculate_tdee(age, weight, height, gender, activity_level):
    if gender == '男':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
    activity_multiplier = {'低活動量': 1.2, '中活動量': 1.55, '高活動量': 1.725}
    return bmr * activity_multiplier[activity_level]

# --- 網頁介面開始 ---
st.set_page_config(page_title="AI 智能營養師", layout="wide")
st.title("🥗 AI 智能飲食追蹤小幫手")

# --- 側邊欄：個人資訊輸入 ---
with st.sidebar:
    st.header("👤 你的基本資料")
    age = st.number_input("年齡", min_value=10, max_value=100, value=25)
    gender = st.selectbox("性別", ["男", "女"])
    weight = st.number_input("體重 (kg)", min_value=30.0, max_value=200.0, value=65.0)
    height = st.number_input("身高 (cm)", min_value=100.0, max_value=250.0, value=170.0)
    activity = st.selectbox("活動量", ["低活動量", "中活動量", "高活動量"])
    
    if st.button("計算每日需求"):
        tdee = calculate_tdee(age, weight, height, gender, activity)
        st.success(f"🎯 你的每日建議熱量 (TDEE)：**{int(tdee)} 大卡**")
        st.info(f"💡 建議：蛋白質約 {int(weight * 1.5)}g | 鈉含量建議低於 2300mg")

# --- 主畫面：照片辨識區 ---
st.header("📸 紀錄今天的餐點")

# 使用 Tabs 讓使用者選擇要「直接拍照」還是「從相簿上傳」
tab1, tab2 = st.tabs(["📸 直接拍照", "📁 從相簿上傳"])

image_to_process = None

# 分頁 1：相機功能
with tab1:
    camera_pic = st.camera_input("拍下你眼前的食物")
    if camera_pic:
        image_to_process = camera_pic

# 分頁 2：上傳功能
with tab2:
    uploaded_pic = st.file_uploader("從手機相簿選擇照片", type=["jpg", "png", "jpeg"])
    if uploaded_pic:
        image_to_process = uploaded_pic

# --- 處理圖片並顯示結果 ---
if image_to_process is not None:
    # 顯示圖片
    image = Image.open(image_to_process)
    st.image(image, caption='已接收照片！', use_container_width=True)
    
    with st.spinner('AI 正在仔細分析這道菜的營養成分...'):
        # 備註：此處目前為模擬數據，未來可接上真實 AI API
        mock_nutrition_data = {
            "食物名稱": "排骨便當",
            "熱量": "750 大卡",
            "蛋白質": "35 g",
            "糖分": "15 g",
            "鈉含量": "1200 mg"
        }
        
    st.success("分析完成！")
    
    # --- 顯示營養成分表 ---
    st.subheader("📊 營養成分估算")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("熱量", mock_nutrition_data["熱量"])
    col2.metric("蛋白質", mock_nutrition_data["蛋白質"])
    col3.metric("糖分", mock_nutrition_data["糖分"])
    col4.metric("鈉含量", mock_nutrition_data["鈉含量"])
    
    # --- 顯示改善建議 ---
    st.subheader("💡 營養師建議")
    st.warning("⚠️ **建議改善：** 這份餐點的**鈉含量偏高**（達每日建議量一半以上），且蔬菜比例偏少。建議下一餐以清淡、水煮為主，並多補充水分與深綠色蔬菜來平衡。")
