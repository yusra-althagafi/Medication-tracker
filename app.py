import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="نظام متابعة الأدوية", layout="wide")

st.title("نظام متابعة وتنظيم جرعات الأدوية للمرضى")
st.caption("قسم المعلوماتية الصحية - المستشفى")

if 'medications' not in st.session_state:
    st.session_state.medications = []

st.sidebar.header("إدخال بيانات دواء جديد")
with st.sidebar.form("med_form", clear_on_submit=True):
    patient_name = st.text_input("اسم المريض")
    file_num = st.text_input("رقم الملف الطبي")
    med_name = st.text_input("اسم الدواء")
    dosage = st.text_input("الجرعة")
    time_schedule = st.time_input("وقت الجرعة القادمة")
    notes = st.text_area("ملاحظات خاصة")
    
    submitted = st.form_submit_button("إضافة الدواء للجدول")
    
    if submitted:
        if patient_name and med_name:
            st.session_state.medications.append({
                "اسم المريض": patient_name,
                "رقم الملف": file_num,
                "الدواء": med_name,
                "الجرعة": dosage,
                "الوقت": time_schedule.strftime("%H:%M"),
                "الملاحظات": notes,
                "الحالة": "قيد الانتظار"
            })
            st.success("تمت إضافة الدواء بنجاح")
        else:
            st.error("يرجى إدخال اسم المريض واسم الدواء على الأقل")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("قائمة الأدوية المسجلة لليوم")
    if len(st.session_state.medications) > 0:
        df = pd.DataFrame(st.session_state.medications)
        st.dataframe(df, use_container_width=True)
        
        st.write("---")
        st.subheader("تحديث حالة تناول الجرعة")
        selected_idx = st.selectbox(
            "اختر رقم السجل لتغيير حالته:", 
            range(len(df)), 
            format_func=lambda x: f"{df.iloc[x]['اسم المريض']} - {df.iloc[x]['الدواء']}"
        )
        
        status_action = st.radio("تحديث الحالة إلى:", ["تم إعطاء الجرعة", "تم التأجيل أو الإلغاء"], horizontal=True)
        if st.button("تحديث الحالة"):
            st.session_state.medications[selected_idx]["الحالة"] = status_action
            st.rerun()
    else:
        st.info("لا توجد أدوية مسجلة حاليا")

with col2:
    st.subheader("تنبيهات الجرعات القادمة")
    now_str = datetime.now().strftime("%H:%M")
    st.write(f"الوقت الحالي: {now_str}")
    
    if len(st.session_state.medications) > 0:
        pending = [m for m in st.session_state.medications if m["الحالة"] == "قيد الانتظار"]
        if pending:
            for item in pending:
                st.warning(f"الدواء: {item['الدواء']} | المريض: {item['اسم المريض']} | الوقت: {item['الوقت']}")
        else:
            st.success("جميع الأدوية المسجلة تم إعطاؤها بنجاح")
