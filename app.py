"""
app.py - LinkedIn Profile Advisor Streamlit Web Application

A complete, beginner-friendly AI-powered advisor for optimizing LinkedIn profiles,
identifying skill gaps, auditing projects, comparing resumes, and planning career roadmaps.
"""

import os
import json
import streamlit as st
from agent import LinkedInAdvisorAgent, get_sample_profile

# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="LinkedIn Profile Advisor",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Custom CSS for LinkedIn-inspired Clean Styling
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Main container styling */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0A66C2;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    /* Metric card styles */
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-score {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0A66C2;
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Badge styling */
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        background-color: #e0f2fe;
        color: #0369a1;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    /* Quick prompt button style */
    .quick-chip {
        font-size: 0.85rem;
        padding: 6px 12px;
        border-radius: 20px;
        border: 1px solid #cbd5e1;
        background: white;
        cursor: pointer;
        display: inline-block;
        margin: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "",
        "education": "",
        "degree": "",
        "current_year": "",
        "career_goal": "",
        "target_role": "",
        "headline": "",
        "about": "",
        "skills": "",
        "projects": "",
        "certifications": "",
        "experience": "",
        "achievements": "",
        "portfolio_url": "",
    }

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------------------------------------------------------
# Sidebar Configuration & Profile Quick Actions
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("💼 Advisor Settings")
    st.markdown("Backend model configuration & status.")

    model_choice = st.selectbox(
        "Select Gemini Model",
        ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-flash-lite-latest", "gemini-3.1-flash-lite"],
        index=0,
    )

    # Initialize AI Agent strictly on the backend using server-side environment variables
    # The API key is securely loaded from .env on the server and never exposed in the UI
    agent = LinkedInAdvisorAgent(model_name=model_choice)

    # Clean connection status without exposing keys or credentials
    if agent.is_ready():
        st.success("🟢 AI Service: Online & Ready")
    else:
        st.error("🔴 AI Service: Offline\n`GEMINI_API_KEY` missing in server `.env`")

    st.markdown("---")
    st.subheader("⚡ Quick Actions")

    if st.button("📥 Load Sample Profile", use_container_width=True):
        st.session_state.profile = get_sample_profile()
        st.session_state.analysis_results = None
        st.success("Loaded Alex Chen's sample student profile!")
        st.rerun()

    if st.button("🗑️ Reset Profile Data", use_container_width=True):
        st.session_state.profile = {k: "" for k in st.session_state.profile}
        st.session_state.analysis_results = None
        st.session_state.chat_history = []
        st.info("Profile data reset.")
        st.rerun()

    # Profile Completeness Gauge
    filled_fields = sum(1 for v in st.session_state.profile.values() if str(v).strip())
    total_fields = len(st.session_state.profile)
    completeness = int((filled_fields / total_fields) * 100)

    st.markdown("---")
    st.markdown(f"**Profile Completeness:** `{completeness}%` ({filled_fields}/{total_fields} fields)")
    st.progress(completeness / 100)

    st.markdown("---")
    st.caption("🔒 **Accuracy Guarantee**: This application never invents false experiences, companies, or credentials.")

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">💼 LinkedIn Profile Advisor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Optimize your profile, uncover skill gaps, craft high-impact descriptions, and get recruiter-ready with Gemini AI.</div>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Navigation Tabs
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "📋 Profile Input",
    "📊 Profile Analysis",
    "💡 Headline Advisor",
    "✍️ About Section",
    "🎯 Skills Advisor",
    "🚀 Project Advisor",
    "📜 Certs & Experience",
    "🎓 Internship Readiness",
    "🗺️ Career Roadmap",
    "📄 Resume Comparison",
    "🔍 Career Research",
    "💬 Interactive AI Advisor",
])

# =============================================================================
# TAB 1: USER PROFILE INPUT
# =============================================================================
with tabs[0]:
    st.header("1. User Profile Information")
    st.markdown("Enter your genuine academic, career, and LinkedIn details below. You can also click **'Load Sample Profile'** in the sidebar.")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=st.session_state.profile.get("name", ""))
            education = st.text_input("University / Institution", value=st.session_state.profile.get("education", ""))
            degree = st.text_input("Degree & Major / Specialization", value=st.session_state.profile.get("degree", ""))
            current_year = st.text_input("Current Academic Year / Status (e.g. 3rd Year)", value=st.session_state.profile.get("current_year", ""))

        with col2:
            target_role = st.text_input("Target Job Role (e.g., Full-Stack Engineer Intern)", value=st.session_state.profile.get("target_role", ""))
            career_goal = st.text_input("Career Goal", value=st.session_state.profile.get("career_goal", ""))
            portfolio_url = st.text_input("GitHub / Portfolio / Personal Website URL", value=st.session_state.profile.get("portfolio_url", ""))

        st.markdown("### Profile Content")
        headline = st.text_input(
            "Current LinkedIn Headline",
            value=st.session_state.profile.get("headline", ""),
            help="Max 220 characters recommended by LinkedIn.",
        )
        about = st.text_area(
            "About / Summary Section",
            value=st.session_state.profile.get("about", ""),
            height=120,
            help="Your current personal summary on LinkedIn.",
        )
        skills = st.text_area(
            "Skills (comma-separated)",
            value=st.session_state.profile.get("skills", ""),
            height=80,
            help="e.g., Python, React, SQL, Git, REST APIs, Docker",
        )

        st.markdown("### Projects, Certifications & Work History")
        projects = st.text_area(
            "Projects (Title, Tech Stack, What you built)",
            value=st.session_state.profile.get("projects", ""),
            height=130,
            help="Include your best academic, personal, or hackathon projects.",
        )
        certifications = st.text_area(
            "Certifications & Courses",
            value=st.session_state.profile.get("certifications", ""),
            height=80,
            help="e.g. CS50, AWS Certified Cloud Practitioner, Coursera Specializations",
        )
        experience = st.text_area(
            "Experience / Internships / Campus Roles",
            value=st.session_state.profile.get("experience", ""),
            height=120,
            help="Include past internships, teaching assistantships, club leadership, etc.",
        )
        achievements = st.text_area(
            "Achievements / Honors / Extracurriculars",
            value=st.session_state.profile.get("achievements", ""),
            height=80,
            help="Competitions, hackathons, academic honors, open source contributions",
        )

        submitted = st.form_submit_button("💾 Save Profile Data", use_container_width=True)
        if submitted:
            st.session_state.profile = {
                "name": name,
                "education": education,
                "degree": degree,
                "current_year": current_year,
                "target_role": target_role,
                "career_goal": career_goal,
                "portfolio_url": portfolio_url,
                "headline": headline,
                "about": about,
                "skills": skills,
                "projects": projects,
                "certifications": certifications,
                "experience": experience,
                "achievements": achievements,
            }
            st.success("✅ Profile details saved successfully! Head to any advisor tab or run an Analysis.")

# Helper to check if profile is sufficiently filled
def require_profile():
    if not st.session_state.profile.get("target_role"):
        st.warning("⚠️ Please provide at least your **Target Job Role** in the Profile Input tab (or click 'Load Sample Profile' in the sidebar) to generate recommendations.")
        return False
    return True

# Helper to verify agent ready
def require_agent():
    if not agent.is_ready():
        st.error("⚠️ AI Backend service is offline. Please ensure `GEMINI_API_KEY` is configured in your server's `.env` file.")
        return False
    return True

# =============================================================================
# TAB 2: PROFILE ANALYSIS
# =============================================================================
with tabs[1]:
    st.header("2. Comprehensive Profile Analysis & Scoring")
    st.markdown("Audits your profile across 8 core dimensions and provides actionable improvements.")

    if require_profile() and require_agent():
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            run_analysis = st.button("🚀 Run Full Profile Audit", type="primary", use_container_width=True)

        if run_analysis:
            with st.spinner("Analyzing profile with Gemini AI..."):
                try:
                    results = agent.analyze_profile(st.session_state.profile)
                    st.session_state.analysis_results = results
                    st.success("Analysis complete!")
                except Exception as e:
                    st.error(f"Error analyzing profile: {str(e)}")

        if st.session_state.analysis_results:
            res = st.session_state.analysis_results
            scores = res.get("scores", {})

            # Overall Score Banner
            overall_score = scores.get("overall", 0)
            score_color = "#16a34a" if overall_score >= 80 else "#d97706" if overall_score >= 60 else "#dc2626"
            st.markdown(
                f"""
                <div style="background-color: #f1f5f9; padding: 20px; border-radius: 12px; border-left: 8px solid {score_color}; margin-bottom: 25px;">
                    <div style="font-size: 1.1rem; color: #475569; font-weight: 600;">OVERALL LINKEDIN PROFILE SCORE</div>
                    <div style="font-size: 3rem; font-weight: 800; color: {score_color};">{overall_score} <span style="font-size: 1.5rem; color: #64748b;">/ 100</span></div>
                    <div style="font-size: 1rem; color: #334155; margin-top: 8px;">{res.get('summary', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Sub-Scores Grid
            st.subheader("Category Score Breakdown")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Headline", f"{scores.get('headline', 0)}/100")
            c2.metric("About Section", f"{scores.get('about', 0)}/100")
            c3.metric("Skills", f"{scores.get('skills', 0)}/100")
            c4.metric("Projects", f"{scores.get('projects', 0)}/100")

            c5, c6, c7, c8 = st.columns(4)
            c5.metric("Certifications", f"{scores.get('certifications', 0)}/100")
            c6.metric("Experience", f"{scores.get('experience', 0)}/100")
            c7.metric("Education", f"{scores.get('education', 0)}/100")
            c8.metric("Career Alignment", f"{scores.get('career_alignment', 0)}/100")

            # Top Priorities
            if "top_priorities" in res and res["top_priorities"]:
                st.markdown("---")
                st.subheader("🎯 Top 3 Immediate Action Priorities")
                for i, prio in enumerate(res["top_priorities"], 1):
                    st.markdown(f"**{i}.** {prio}")

            # Category Deep-Dives
            if "category_feedback" in res:
                st.markdown("---")
                st.subheader("Detailed Category Feedback & Suggestions")
                for cat, fb in res["category_feedback"].items():
                    with st.expander(f"📌 {cat.replace('_', ' ').title()} - Score: {fb.get('score', 'N/A')}/100", expanded=False):
                        st.markdown(f"**Analysis:** {fb.get('analysis', '')}")
                        st.markdown("**Suggestions:**")
                        for s in fb.get("suggestions", []):
                            st.markdown(f"- {s}")

# =============================================================================
# TAB 3: HEADLINE ADVISOR
# =============================================================================
with tabs[2]:
    st.header("3. LinkedIn Headline Advisor")
    st.markdown("Craft 3-5 high-converting headline options optimized for searchability and recruiter clicks (within LinkedIn's 220 character limit).")

    if require_profile() and require_agent():
        if st.button("✨ Generate Headline Options", type="primary"):
            with st.spinner("Generating headline options..."):
                try:
                    result = agent.generate_headlines(st.session_state.profile)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error generating headlines: {str(e)}")

# =============================================================================
# TAB 4: ABOUT SECTION ADVISOR
# =============================================================================
with tabs[3]:
    st.header("4. About / Summary Section Advisor")
    st.markdown("Analyze strengths, fix weaknesses, and generate a compelling rewritten personal pitch based strictly on your real credentials.")

    if require_profile() and require_agent():
        if st.button("✍️ Audit & Rewrite About Section", type="primary"):
            with st.spinner("Auditing About section..."):
                try:
                    result = agent.improve_about(st.session_state.profile)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error auditing About section: {str(e)}")

# =============================================================================
# TAB 5: SKILLS ADVISOR
# =============================================================================
with tabs[4]:
    st.header("5. Skills Gap & Alignment Advisor")
    st.markdown("Compare your current skills with industry requirements for your target role and discover missing high-priority competencies.")

    if require_profile() and require_agent():
        if st.button("🎯 Analyze Skills & Find Gaps", type="primary"):
            with st.spinner("Analyzing skills match..."):
                try:
                    result = agent.analyze_skills(st.session_state.profile)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error analyzing skills: {str(e)}")

# =============================================================================
# TAB 6: PROJECT ADVISOR
# =============================================================================
with tabs[5]:
    st.header("6. Project Advisor")
    st.markdown("Turn academic and personal projects into recruiter-friendly portfolio assets with impact metrics, better titles, and Google XYZ formatting.")

    if require_profile() and require_agent():
        if st.button("🚀 Optimize Projects for LinkedIn", type="primary"):
            with st.spinner("Analyzing and optimizing projects..."):
                try:
                    result = agent.analyze_projects(st.session_state.profile)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error optimizing projects: {str(e)}")

# =============================================================================
# TAB 7: CERTIFICATIONS & EXPERIENCE
# =============================================================================
with tabs[6]:
    st.header("7. Certifications & Experience Advisor")
    st.markdown("Refine how certifications and professional experiences are highlighted.")

    col_c, col_e = st.columns(2)
    with col_c:
        st.subheader("📜 Certification Strategy")
        if st.button("Analyze Certifications"):
            if require_profile() and require_agent():
                with st.spinner("Reviewing certifications..."):
                    try:
                        result = agent.advise_certifications(st.session_state.profile)
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"Error analyzing certifications: {str(e)}")

    with col_e:
        st.subheader("💼 Experience Phrasing & Impact")
        if st.button("Elevate Experience Descriptions"):
            if require_profile() and require_agent():
                with st.spinner("Polishing experience descriptions..."):
                    try:
                        result = agent.improve_experience(st.session_state.profile)
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"Error improving experience: {str(e)}")

# =============================================================================
# TAB 8: INTERNSHIP READINESS
# =============================================================================
with tabs[7]:
    st.header("8. Internship Readiness Assessment")
    st.markdown("Evaluate whether your profile is ready to apply for internships, identify core gaps, and get a 4-week fast-track prep plan.")

    if require_profile() and require_agent():
        if st.button("🎓 Check Internship Readiness", type="primary"):
            with st.spinner("Assessing internship readiness..."):
                try:
                    result = agent.assess_internship_readiness(st.session_state.profile)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error evaluating readiness: {str(e)}")

# =============================================================================
# TAB 9: CAREER ROADMAP
# =============================================================================
with tabs[8]:
    st.header("9. Personalized Career Roadmap")
    st.markdown("Get a week-by-week actionable plan to bridge skill gaps and prepare for your target role.")

    timeframe = st.radio("Select Roadmap Horizon:", ["30", "60", "90"], horizontal=True, format_func=lambda x: f"{x}-Day Action Plan")

    if require_profile() and require_agent():
        if st.button(f"🗺️ Generate {timeframe}-Day Career Roadmap", type="primary"):
            with st.spinner(f"Generating personalized {timeframe}-day roadmap..."):
                try:
                    result = agent.generate_career_roadmap(st.session_state.profile, timeframe=timeframe)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error generating roadmap: {str(e)}")

# =============================================================================
# TAB 10: RESUME VS LINKEDIN COMPARISON
# =============================================================================
with tabs[9]:
    st.header("10. Resume vs. LinkedIn Profile Comparison")
    st.markdown("Ensure 100% alignment between your resume and LinkedIn profile to prevent ATS conflicts or recruiter confusion.")

    resume_text = st.text_area(
        "Paste your Resume Text here:",
        height=200,
        placeholder="Paste your education, skills, projects, and work experience text from your resume...",
    )

    if require_profile() and require_agent():
        if st.button("⚖️ Compare Resume with LinkedIn Profile", type="primary"):
            if not resume_text.strip():
                st.warning("Please paste your resume text to compare.")
            else:
                with st.spinner("Auditing cross-platform consistency..."):
                    try:
                        result = agent.compare_resume(st.session_state.profile, resume_text)
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"Error comparing resume: {str(e)}")

# =============================================================================
# TAB 11: CAREER MARKET RESEARCH
# =============================================================================
with tabs[10]:
    st.header("11. Real-World Career Market Research")
    st.markdown("Research industry requirements, in-demand technical frameworks, and hiring criteria for your target role.")

    if require_profile() and require_agent():
        target = st.session_state.profile.get("target_role", "Software Engineer")
        st.info(f"Target Role for Market Research: **{target}**")
        if st.button(f"🔍 Research Market Demands for '{target}'", type="primary"):
            with st.spinner("Synthesizing market hiring intelligence..."):
                try:
                    result = agent.research_career_market(st.session_state.profile)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error researching market: {str(e)}")

# =============================================================================
# TAB 12: INTERACTIVE AI ADVISOR (CHAT)
# =============================================================================
with tabs[11]:
    st.header("12. Interactive AI Career Coach")
    st.markdown("Ask any question regarding your profile, interview strategy, or career growth.")

    # Quick prompt chips
    st.markdown("**Suggested Quick Questions:**")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    quick_col4, quick_col5, quick_col6 = st.columns(3)

    q1 = quick_col1.button("✨ Improve my headline", use_container_width=True)
    q2 = quick_col2.button("✍️ Rewrite my About section", use_container_width=True)
    q3 = quick_col3.button("🎯 What skills am I missing?", use_container_width=True)
    q4 = quick_col4.button("🎓 Am I ready for an internship?", use_container_width=True)
    q5 = quick_col5.button("🚀 Improve my project description", use_container_width=True)
    q6 = quick_col6.button("🗺️ Give me a 30-day improvement plan", use_container_width=True)

    triggered_prompt = None
    if q1:
        triggered_prompt = "Improve my headline with 3 options based on my target role."
    elif q2:
        triggered_prompt = "Rewrite my About section into a compelling personal pitch using my actual details."
    elif q3:
        triggered_prompt = "What skills am I missing for my target role, and why do they matter?"
    elif q4:
        triggered_prompt = "Am I ready for an internship? What are my biggest gaps?"
    elif q5:
        triggered_prompt = "Improve my project descriptions using the Google XYZ impact format."
    elif q6:
        triggered_prompt = "Give me a practical 30-day improvement plan to get recruiter-ready."

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_prompt = st.chat_input("Ask a question about your LinkedIn profile...")
    prompt_to_send = triggered_prompt or user_prompt

    if prompt_to_send:
        if require_agent():
            # Add user message to state
            st.session_state.chat_history.append({"role": "user", "content": prompt_to_send})
            with st.chat_message("user"):
                st.markdown(prompt_to_send)

            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        reply = agent.chat_advisor(
                            st.session_state.profile,
                            st.session_state.chat_history[:-1],
                            prompt_to_send,
                        )
                        st.markdown(reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"Error during advisor chat: {str(e)}")

    if st.session_state.chat_history:
        if st.button("🧹 Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
