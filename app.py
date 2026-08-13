import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import io
import zipfile
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    # --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Kr8tiv AI Studios | Pro Studio Shots Instantly",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('kr8tiv_ai.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        email TEXT, 
                        image_name TEXT,
                        created_at TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        date TEXT, 
                        event_type TEXT, 
                        revenue REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS spots (
                        id INTEGER PRIMARY KEY, 
                        remaining INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS refunds (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        email TEXT, 
                        reason TEXT, 
                        status TEXT)''')
    
    # Initialize spots if empty
    cursor.execute("SELECT COUNT(*) FROM spots")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO spots (id, remaining) VALUES (1, 14)") # 14 spots left of 50
        conn.commit()
    conn.commit()
    return conn

conn = init_db()

# --- HELPER FUNCTIONS ---
def log_metric(event_type, revenue=0.0):
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO metrics (date, event_type, revenue) VALUES (?, ?, ?)", (today, event_type, revenue))
    conn.commit()

def get_remaining_spots():
    cursor = conn.cursor()
    cursor.execute("SELECT remaining FROM spots WHERE id=1")
    return cursor.fetchone()[0]

def decrement_spot():
    cursor = conn.cursor()
    current = get_remaining_spots()
    if current > 0:
        cursor.execute("UPDATE spots SET remaining = ? WHERE id=1", (current - 1,))
        conn.commit()

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://images.unsplash.com/photo-1542038784456-1ea8e935640e?auto=format&fit=crop&w=300&q=80", use_container_width=True)
st.sidebar.title("Kr8tiv AI Studios")
st.sidebar.markdown("*“Turn crappy phone pics into pro studio shots with AI.”*")

menu = st.sidebar.radio("Navigation", ["Home & Landing", "Free AI Glow-Up (Trial)", "Pricing & Upgrades", "Customer Dashboard", "Admin Analytics"])

# --- GUARANTEE BANNER ---
st.sidebar.markdown("---")
st.sidebar.markdown("🛡️ **100% Satisfaction Guarantee**\n*Money Back + Free Reshoot if not satisfied.*")

# ==========================================
# 1. HOME & LANDING PAGE
# ==========================================
if menu == "Home & Landing":
    # Scarcity Counter Header
    spots_left = get_remaining_spots()
    st.error(f"🚨 **URGENT SCARCITY**: Only **{spots_left} spots** remaining out of 50 for this month's cohort!")

    # Hero Section - 5 Ad Angles Rotator
    ad_angles = [
        "🔥 Angle 1: Stop losing clients to competitors with better profile pictures.",
        "🚀 Angle 2: 3x your social media engagement with zero photography budget.",
        "⚡ Angle 3: Transform a selfie taken on an old phone into a Hollywood-grade headshot in 10 minutes.",
        "💼 Angle 4: The ultimate personal branding secret used by top 1% creators in South Africa.",
        "🎨 Angle 5: Instant studio-quality product photos for e-commerce without renting a studio."
    ]
    st.info(random.choice(ad_angles))

    st.title("Instant Studio-Quality Photos Powered by AI")
    st.subheader("Boost your online engagement by 3-5x without the studio hassle or expensive equipment.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ❌ The Problem")
        st.markdown("Bad lighting, grainy phone snaps, and amateur backgrounds kill your trust, lower your click-through rates, and lose you valuable customers and leads.")
    with col2:
        st.markdown("### ✅ The AI Solution")
        st.markdown("Our neural rendering engine instantly enhances lighting, optimizes composition, and replaces backgrounds to deliver pristine, pro-grade assets in under 10 minutes.")

    st.markdown("---")
    st.markdown("### 🌟 Proof Stack & Testimonials")
    tcol1, tcol2, tcol3 = st.columns(3)
    with tcol1:
        st.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80", caption="Sarah J. (Digital Marketer) - 'Engagement up 400%!'")
    with tcol2:
        st.image("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80", caption="Marcus T. (Founder) - 'Closed 2 enterprise deals using my new headshot.'")
    with tcol3:
        st.image("https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=80", caption="Lerato M. (Creator) - 'Saved R5,000 on my first photoshoot.'")

# ==========================================
# 2. FREE AI GLOW-UP (LEAD MAGNET & TRIAL)
# ==========================================
elif menu == "Free AI Glow-Up (Trial)":
    st.header("✨ Try It Free: Instant AI Headshot Upgrade")
    st.markdown("Upload any selfie or product photo. No credit card required. Experience the power of the Value Equation firsthand.")

    uploaded_file = st.file_uploader("Upload your photo (JPG, PNG)", type=["jpg", "png", "jpeg"])
    user_email = st.text_input("Enter your email address to receive your enhanced photo:")

    if uploaded_file and user_email:
        if st.button("🚀 Generate AI Glow-Up Now"):
            with st.spinner("Analyzing image lighting, neural sharpening, and rendering studio background... (Simulating AI processing)"):
                # Simulate processing delay
                import time
                time.sleep(2)
                
                # Log lead
                cursor = conn.cursor()
                cursor.execute("INSERT INTO leads (email, image_name, created_at) VALUES (?, ?, ?)", 
                               (user_email, uploaded_file.name, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                log_metric("Free Trial Lead")
                decrement_spot()

                st.success("🎉 Success! Your AI-enhanced photo is ready.")
                
                # Show mock comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.image(uploaded_file, caption="Original Upload", use_column_width=True)
                with col2:
                    st.image("https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80", caption="AI Studio Enhancement (Preview)", use_column_width=True)

                # Moat Feature: Engagement Optimizer Caption Generator
                st.markdown("### 🤖 Proprietary AI Engagement Optimizer")
                st.info("**Generated High-Converting Caption for your post:**\n\n*“First impressions matter. Leveling up my digital workspace and brand identity with studio-quality visuals. How do you maintain consistency across your channels? Let me know below! 👇 #PersonalBranding #AIInnovation #Growth”*")

                # Bonus 1: Social Media Template Pack Downloadable ZIP
                st.markdown("### 🎁 Bonus 1: Engagement Booster Template Pack")
                
                # Create zip in memory
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    zf.writestr("Template_1_Hook.txt", "Hook: Stop scrolling if you want 3x more engagement...")
                    zf.writestr("Template_2_CTA.txt", "Call to Action: Comment 'READY' below for the full guide.")
                
                st.download_button(
                    label="📥 Download 50 Social Templates (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="Kr8tiv_Templates.zip",
                    mime="application/zip"
                )

# ==========================================
# 3. PRICING & UPGRADES
# ==========================================
elif menu == "Pricing & Upgrades":
    st.header("💎 Choose Your Grand Slam Offer")
    st.markdown("Lock in your spot before monthly cohorts fill up. Billed securely in South African Rand (ZAR).")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Starter Glow")
        st.markdown("## **ZAR 495** / mo")
        st.markdown("* 10 Shoots / month\n* Basic AI enhancements\n* 1 Bonus Template Pack\n* Standard email support")
        if st.button("Select Starter Glow"):
            log_metric("Subscription Starter", 495.0)
            st.success("Redirecting to Stripe Checkout... (Payment link simulation successful!)")

    with col2:
        st.markdown("### 🌟 Pro Creator (Most Popular)")
        st.markdown("## **ZAR 995** / mo")
        st.markdown("* **Unlimited** shoots\n* All AI models & backgrounds\n* Priority Processing\n* All Bonuses + AI Optimizer")
        if st.button("Select Pro Creator"):
            log_metric("Subscription Pro", 995.0)
            st.success("Redirecting to Stripe Checkout... (Payment link simulation successful!)")

    with col3:
        st.markdown("### Enterprise Brand")
        st.markdown("## **ZAR 4,995** / yr")
        st.markdown("* *(10% Annual Discount Applied)*\n* Custom brand models\n* Multi-user team access\n* Dedicated support manager\n* *Or pay 3x ZAR 1,695 installments*")
        if st.button("Select Enterprise Brand"):
            log_metric("Subscription Enterprise", 4995.0)
            st.success("Redirecting to Stripe Checkout... (Payment link simulation successful!)")

    st.markdown("---")
    st.markdown("### 🚀 Post-Purchase Ascension Upsells")
    upcol1, upcol2 = st.columns(2)
    with upcol1:
        st.info("**Custom Brand Pack** — ZAR 1,995 one-time\nAdd custom corporate colors, typography, and branded overlays to all generated studio assets.")
        if st.button("Add Custom Brand Pack"):
            log_metric("Upsell Brand Pack", 1995.0)
            st.success("Upsell added successfully!")
    with upcol2:
        st.info("**AI Video Edits Cross-Sell** — ZAR 795 / mo\nAutomatically convert your static enhanced photos into talking-head video avatars.")
        if st.button("Add AI Video Edits"):
            log_metric("Upsell Video Edits", 795.0)
            st.success("Cross-sell added successfully!")

# ==========================================
# 4. CUSTOMER DASHBOARD
# ==========================================
elif menu == "Customer Dashboard":
    st.header("📊 Your Customer Studio Dashboard")
    st.markdown("Track your usage, view past uploads, and manage your plan.")

    # Usage meter
    st.markdown("### Usage This Month")
    st.progress(65)
    st.caption("65 of 100 AI Generation Credits Used (Renews in 12 days)")

    st.markdown("### 📈 Engagement Analytics Preview")
    chart_data = pd.DataFrame(
        [120, 210, 340, 450, 520, 680, 890],
        columns=["Simulated Engagement Boost Index"]
    )
    st.line_chart(chart_data)

    st.markdown("### 🔄 Need Support or Refund?")
    with st.form("refund_form"):
        r_email = st.text_input("Account Email")
        r_reason = st.text_area("Reason for refund request (Covered by our 100% Money Back Guarantee):")
        r_submit = st.form_submit_button("Submit Refund / Reshoot Request")
        if r_submit and r_email:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO refunds (email, reason, status) VALUES (?, ?, ?)", (r_email, r_reason, "Pending"))
            conn.commit()
            st.success("Your request has been logged. Our support team will process your money back + free reshoot within 24 hours.")

# ==========================================
# 5. ADMIN ANALYTICS
# ==========================================
elif menu == "Admin Analytics":
    st.header("🔐 Admin Metrics & Business Health")
    st.markdown("Real-time telemetry tracking for daily leads, trials, revenue, and churn metrics.")

    cursor = conn.cursor()
    cursor.execute("SELECT SUM(revenue) FROM metrics")
    total_rev = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT COUNT(*) FROM leads")
    total_leads = cursor.fetchone()[0] or 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Gross Revenue", f"ZAR {total_rev:,.2f}")
    col2.metric("Total Free Leads Captured", total_leads)
    col3.metric("Estimated MRR (Monthly Recurring)", f"ZAR {total_rev * 0.7:,.2f}")

    st.markdown("### 📋 Recent Transaction & Lead Logs")
    df_metrics = pd.read_sql_query("SELECT * FROM metrics ORDER BY id DESC LIMIT 10", conn)
    st.dataframe(df_metrics, use_container_width=True)

    st.markdown("### ⚠️ Pending Refund Requests")
    df_refunds = pd.read_sql_query("SELECT * FROM refunds WHERE status='Pending'", conn)
    st.dataframe(df_refunds, use_container_width=True)

