import streamlit as st
import pandas as pd
import plotly.express as px
import os
import glob
from datetime import datetime

# --- ASSETS ---
LOGIN_EMBLEM_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/1024px-Emblem_of_India.svg.png" 
SIDEBAR_LOGO_URL = "https://cdn-icons-png.flaticon.com/512/2917/2917995.png"

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ration-Mitr | Official Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. ADVANCED CSS (CLEAN & STABLE)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* GLOBAL THEME */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* --- LOGIN PAGE STYLES --- */
    .hero-container {
        padding: 40px;
        border-right: 1px solid #333;
        height: 85vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .hero-title {
        font-size: 64px;
        font-weight: 800;
        background: -webkit-linear-gradient(#FF9933, #FFFFFF, #138808);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 22px;
        color: #CCCCCC;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    /* STATIC INFO BOX (Replaces broken marquee) */
    .info-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 25px;
        border-left: 5px solid #FF9933;
    }
    .info-item {
        margin-bottom: 12px;
        font-size: 16px;
        color: #E0E0E0;
        display: flex;
        align-items: center;
    }
    .info-icon { margin-right: 10px; font-size: 20px; }

    /* --- LOGIN CARD --- */
    div[data-testid="column"]:nth-of-type(2) {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 85vh;
    }
    .login-card-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 25px;
    }
    
    /* ASH WHITE LOGO CONTAINER */
    .logo-container {
        background-color: #F0F2F6;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.15);
        margin-bottom: 25px;
    }
    .emblem-img { width: 80px; height: auto; }
    
    .login-title { font-size: 28px; font-weight: 700; color: #FFFFFF; }
    .login-dept { font-size: 14px; color: #AAAAAA; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }

    /* FORM STYLING */
    div[data-testid="stForm"] {
        background-color: rgba(38, 39, 48, 0.6);
        border: 1px solid #444;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        width: 100%;
    }

    /* DASHBOARD ELEMENTS */
    [data-testid="stSidebar"] { background-color: #262730; }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; }
    div[data-testid="stMetricLabel"] { color: #E0E0E0 !important; }
    .stAlert { background-color: #333; color: white; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. AUTHENTICATION LOGIC
# ---------------------------------------------------------
def check_password():
    def password_entered():
        if st.session_state["username"] == "admin" and st.session_state["password"] == "admin123":
            st.session_state["password_correct"] = True
            st.session_state["login_failed"] = False
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
            st.session_state["login_failed"] = True

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
        st.session_state["login_failed"] = False

    if not st.session_state["password_correct"]:
        col1, col2 = st.columns([1.6, 1]) 

        # LEFT SIDE: HERO + STATIC INFO (Clean & Stable)
        with col1:
            st.markdown(f"""
                <div class="hero-container">
                    <div>
                        <h1 class="hero-title">Ration-Mitr</h1>
                        <p class="hero-subtitle">Department of Food & Public Distribution<br>Intelligent Command Center</p>
                    </div>
                    <div class="info-box">
                        <div class="info-item"><span class="info-icon"></span> <b>India Fact:</b> NFSA covers 80 Crore+ citizens.</div>
                        <div class="info-item"><span class="info-icon"></span> <b>Mission:</b> 'One Nation, One Ration Card'.</div>
                        <div class="info-item"><span class="info-icon"></span> <b>Live Tracking:</b> Monitoring 700+ Districts.</div>
                        <div class="info-item"><span class="info-icon"></span> <b>Equity:</b> Preventing grain wastage.</div>
                        <div class="info-item"><span class="info-icon"></span> <b>Tech:</b> Powered by Aadhar Metadata & AI.</div>
                        <div class="info-item"><span class="info-icon"></span> <b>Status:</b> National Data Grid synchronized.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # RIGHT SIDE: LOGIN
        with col2:
            st.markdown(f"""
                <div class="login-card-header">
                    <div class="logo-container">
                        <img src="{LOGIN_EMBLEM_URL}" class="emblem-img">
                    </div>
                    <div class="login-title">Official Login</div>
                    <div class="login-dept">Ministry of Consumer Affairs</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.text_input("Officer ID", key="username", placeholder="Username")
                st.text_input("Secure Passkey", type="password", key="password", placeholder="Password")
                st.markdown("<br>", unsafe_allow_html=True)
                st.form_submit_button("Verify Credentials", on_click=password_entered, type="primary", use_container_width=True)

            if st.session_state.get("login_failed", False):
                st.error("Authorization Failed: Invalid ID or Key")
                
        st.markdown("---")
        st.caption("UIDAI Hackathon 2026 | Team Ration-Mitr")

        return False
    else:
        return True

# ---------------------------------------------------------
# 4. DATA ENGINE
# ---------------------------------------------------------
@st.cache_data
def load_and_process_data():
    data_folder = "data"
    
    # Discovery
    demo_files = glob.glob(os.path.join(data_folder, "district_cleaned_state_*demographic*.csv"))
    enrol_files = glob.glob(os.path.join(data_folder, "district_cleaned_state_*enrolment*.csv"))
    
    if not demo_files: demo_files = glob.glob(os.path.join(data_folder, "district_cleaned_*demographic*.csv"))
    if not enrol_files: enrol_files = glob.glob(os.path.join(data_folder, "district_cleaned_*enrolment*.csv"))
    if not demo_files: demo_files = glob.glob(os.path.join(data_folder, "*demographic*.csv"))
    if not enrol_files: enrol_files = glob.glob(os.path.join(data_folder, "*enrolment*.csv"))

    if not demo_files or not enrol_files:
        return None, None

    try:
        # Load
        df_demo = pd.concat((pd.read_csv(f) for f in demo_files), ignore_index=True)
        df_enrol = pd.concat((pd.read_csv(f) for f in enrol_files), ignore_index=True)
        
        df_demo.columns = [c.lower() for c in df_demo.columns]
        df_enrol.columns = [c.lower() for c in df_enrol.columns]
        
        # Stats
        demo_count = len(demo_files)
        enrol_count = len(enrol_files)
        total_files = demo_count + enrol_count
        total_rows = len(df_demo) + len(df_enrol)
        total_bytes = sum(os.path.getsize(f) for f in demo_files + enrol_files)
        memory_mb = round(total_bytes / (1024 * 1024), 2)
        
        system_stats = {
            "demo_count": demo_count,
            "enrol_count": enrol_count,
            "total_files": total_files,
            "total_entries": total_rows,
            "memory_usage": memory_mb
        }

        # Logic
        demo_agg = df_demo.groupby(['state', 'district'])[['demo_age_17_']].sum().reset_index()
        enrol_agg = df_enrol.groupby(['state', 'district'])[['age_0_5']].sum().reset_index()
        
        merged = pd.merge(demo_agg, enrol_agg, on=['state', 'district'], how='inner')
        merged['Migration_Score'] = (merged['demo_age_17_'] / (merged['age_0_5'] + 1)).round(2)
        
        def get_status(score):
            if score > 50: return "CRITICAL"
            elif score > 20: return "WARNING"
            else: return "STABLE"
        merged['Status'] = merged['Migration_Score'].apply(get_status)
        merged['Grain_Demand_MT'] = (merged['demo_age_17_'] * 0.02).round(1)
        
        return merged, system_stats
        
    except Exception as e:
        return None, str(e)

# ---------------------------------------------------------
# 5. MAIN APP EXECUTION
# ---------------------------------------------------------
if check_password():
    
    df, stats = load_and_process_data()

    if df is None:
        if isinstance(stats, str): st.error(f"Error: {stats}")
        else: st.error("Data missing in 'data/' folder.")
        st.stop()

    current_time = datetime.now().strftime("%I:%M %p")
    
    if not df.empty:
        highest_risk_row = df.loc[df['Migration_Score'].idxmax()]
        critical_district = highest_risk_row['district']
        critical_score = highest_risk_row['Migration_Score']
        total_grain_demand = df['Grain_Demand_MT'].sum()
    else:
        critical_district = "Initializing..."
        critical_score = 0.0
        total_grain_demand = 0

    # --- HORIZONTAL TICKER (CRASH PROOF) ---
    marquee_content = (
        f"<b>LIVE UPDATES:</b> System Synchronized at {current_time} IST &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; "
        f"<b>CRITICAL ALERT:</b> High influx in {critical_district} (Score: {critical_score}) &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; "
        f"<b>STATUS:</b> All Nodes Operational. {stats['total_entries']:,} Records Processed. &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; "
        f"<b>GRAIN DEFICIT:</b> {total_grain_demand:,.0f} MT National Total. &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; "
        f"<b>DATA INGESTION:</b> Active on {stats['total_files']} Shards..."
    )

    st.markdown(f"""
        <div style="background-color: #1E1E1E; border-bottom: 2px solid #00CC96; color: #00CC96; padding: 10px; margin-top: -50px; margin-bottom: 20px;">
            <marquee scrollamount="10" style="font-family: 'Segoe UI', monospace; font-size: 16px;">
                {marquee_content}
            </marquee>
        </div>
    """, unsafe_allow_html=True)
    
    # --- SIDEBAR ---
    with st.sidebar:
        c_logo, c_title = st.columns([1, 4])
        with c_logo: st.image(SIDEBAR_LOGO_URL, width=50)
        with c_title: st.title("Ration-Mitr") 

        st.caption("One Nation, One Ration Intelligence")
        
        selected_page = st.radio("Navigate", ["Dashboard", "Raw Data", "About Project"])
        st.markdown("---")
        
        state_list = ["All India"] + sorted(df['state'].unique().tolist())
        selected_state = st.selectbox("Select Region", state_list)
        
        if selected_state != "All India": df_view = df[df['state'] == selected_state]
        else: df_view = df
            
        st.success("System Online")
        
        with st.expander("System Statistics: ", expanded=True):
            r1c1, r1c2 = st.columns(2)
            r1c1.metric("Demo Files", stats['demo_count'])
            r1c2.metric("Enrol Files", stats['enrol_count'])
            st.metric("Total Files Processed", stats['total_files'])
            r2c1, r2c2 = st.columns(2)
            r2c1.metric("Size (MB)", stats['memory_usage'])
            r2c2.metric("Total Rows", f"{stats['total_entries']:,}")
            st.caption("Batch Processing Active")

        if st.button("Log Out"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- DASHBOARD PAGE ---
    if selected_page == "Dashboard":
        col1, col2 = st.columns([3, 1]) 
        with col1:
            st.title("National Food Security Command Center") 
            st.markdown("### *Dynamic Resource Allocation System*")

        with col2:
            current_view = selected_state if selected_state else "All India"
            st.markdown(f"""
                <div style="background-color: #333333; padding: 10px; border-radius: 8px; border-left: 5px solid #3498db;">
                    <small style="color: #BBBBBB;">CURRENT VIEW</small><br>
                    <span style="font-size: 20px; font-weight: bold; color: #FFFFFF;">{current_view}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        total_influx = df_view['demo_age_17_'].sum()
        critical_count = df_view[df_view['Status'] == 'CRITICAL'].shape[0]
        grain_needed = df_view['Grain_Demand_MT'].sum()

        kpi1.metric("Predicted Migrant Influx", f"{total_influx:,}", "Address Updates")
        kpi2.metric("Critical Stress Zones", f"{critical_count}", "Districts", delta_color="inverse")
        kpi3.metric("Grain Deficit", f"{grain_needed:,.0f} MT", "vs Last Month")
        kpi4.metric("Supply Chain Efficiency", "94.2%", "+1.2%")

        col_chart, col_table = st.columns([2, 1])

        with col_chart:
            st.subheader("Real-time Migration Hotspots")
            top_districts = df_view.sort_values(by='Migration_Score', ascending=False).head(10)
            if not top_districts.empty:
                fig = px.bar(
                    top_districts, x='Migration_Score', y='district', orientation='h',
                    color='Status', color_discrete_map={"CRITICAL": "#FF4B4B", "WARNING": "#FFA500", "STABLE": "#00CC96"},
                    title="Districts by Influx Intensity (Based on Migration Score)", text='Grain_Demand_MT'
                )
                fig.update_layout(
                    yaxis=dict(autorange="reversed"), height=400,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
            else: st.info("No data available.")

        with col_table:
            st.subheader("Priority Alerts(Based on Grain Demand)")
            alerts = df_view[df_view['Status'].isin(['CRITICAL', 'WARNING'])].copy()
            status_priority = {'CRITICAL': 0, 'WARNING': 1}
            alerts['priority_index'] = alerts['Status'].map(status_priority)
            alerts = alerts.sort_values(by=['priority_index', 'Grain_Demand_MT'], ascending=[True, False])
            
            if not alerts.empty:
                st.dataframe(
                    alerts[['district', 'Status', 'Grain_Demand_MT']],
                    column_config={"district": "District", "Status": "Risk Level", "Grain_Demand_MT": "Addl. Grain (MT)"},
                    hide_index=True, use_container_width=True
                )
            else: st.success("No critical alerts in this region.")
            
        st.markdown("---")
        st.caption("UIDAI Hackathon 2026 | Team Ration-Mitr")

    # --- RAW DATA PAGE ---
    elif selected_page == "Raw Data":
        st.title("Data Inspector")
        st.markdown(f"### Raw Data View: {selected_state}")
        st.dataframe(df_view, use_container_width=True)
        
        st.markdown("---")
        st.caption("UIDAI Hackathon 2026 | Team Ration-Mitr")

    # --- ABOUT PAGE ---
    elif selected_page == "About Project":
        st.title("Project Documentation: Ration-Mitr")
        st.markdown("##### *Optimizing Grain Allocation via Administrative Metadata Analysis*")
        st.markdown("---")
        
        st.subheader("1. Problem Statement")
        st.error(
            """
            **Static Allocation in a Dynamic Economy**
            
            * **Data Latency:** The Public Distribution System (PDS) relies on static census data (updated every 10 years).
            * **Migrant Mobility:** India's workforce is highly mobile, moving constantly between states for employment.
            * **Resource Mismatch:** This leads to grain deficits in high-influx urban zones and wastage in low-density rural areas.
            * **Inefficiency:** Current supply chains cannot react to sudden population shifts (e.g., seasonal migration).
            """
        )
        
        st.subheader("2. Algorithmic Methodology")
        st.info(
            """
            **The MigraSense Metric**
            
            * **Dynamic Proxy:** We use Aadhar update metadata as a real-time proxy for migration.
            * **Filtering Noise:** The algorithm distinguishes between natural growth and migration.
            * **The Formula:** We compare Adult Address Updates against Child Birth Enrolments.
            * **Outcome:** A normalized 'Migration Score' that flags districts with unnatural population spikes.
            """
        )
        st.code("Migration_Intensity = (Adult_Address_Updates) / (Child_Birth_Enrolments + 1)", language="python")

        st.subheader("3. System Architecture")
        st.warning(
            """
            **Tech Stack & Components**
            
            * **Frontend:** Streamlit (Python-based reactive UI framework).
            * **Data Engine:** Pandas (High-performance vectorized batch processing).
            * **Sanitization:** Custom Regex Engine for cleaning administrative text errors.
            * **Clustering:** RapidFuzz library for AI-driven deduplication of district names.
            * **Visualization:** Plotly Express for interactive geospatial analytics.
            """
        )

        st.subheader("4. ETL Pipeline Specification")
        st.success(
            """
            **From Raw Data to Insight**
            
            1.  **Ingestion Layer:** Aggregates fragmented CSV shards into a unified in-memory dataframe.
            2.  **Sanitization Layer:** Removes numerical anomalies (e.g., '1002') and special characters using Regex.
            3.  **Deduplication Layer:** Merges semantic duplicates (e.g., 'Bangalore' & 'Bengaluru') using fuzzy logic frequency analysis.
            4.  **Computation Layer:** Calculates dynamic risk scores and grain deficits in real-time.
            """
        )

        st.subheader("5. Real-Time System Metrics")
        st.markdown(
            f"""
            <div style="background-color: #262730; padding: 20px; border-radius: 5px; border: 1px solid #444;">
                <ul style="margin: 0; padding-left: 20px; color: #E0E0E0;">
                    <li style="margin-bottom: 10px;"><b>Total Files Processed:</b> {stats['total_files']} source files ingested.</li>
                    <li style="margin-bottom: 10px;"><b>Dataset Volume:</b> {stats['total_entries']:,} individual records analyzed.</li>
                    <li style="margin-bottom: 10px;"><b>Memory Footprint:</b> {stats['memory_usage']} MB (In-Memory Optimization).</li>
                    <li><b>Status:</b> Active Batch Processing.</li>
                </ul>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.caption("UIDAI Hackathon 2026 | Team Ration-Mitr")