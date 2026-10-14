# 💼 LinkedIn Profile Advisor

An intelligent, AI-powered career assistant and profile optimization tool built with **Streamlit** and the **Google Gemini API**. It provides automated scoring, ATS-friendly rewrites, skills gap analysis, internship readiness checks, and interactive career coaching—without ever hallucinating fake credentials.

---

## 🌟 Key Features

1. **User Profile Management**
   - Clean, structured form to input education, target role, headline, about section, skills, projects, certifications, internships, and portfolio URLs.
   - Built-in **"Load Sample Profile"** button for instant one-click testing without manual data entry.
   - Profile completeness meter to track missing sections.

2. **Multi-Dimensional Profile Analysis & Scoring**
   - Overall profile score out of 100.
   - 8 individual sub-scores:
     - 💡 *Headline Score*
     - ✍️ *About Section Score*
     - 🎯 *Skills Match Score*
     - 🚀 *Projects Score*
     - 📜 *Certifications Score*
     - 💼 *Experience Score*
     - 🎓 *Education Score*
     - 🎯 *Career Alignment Score*
   - Explains the exact reason behind every score and gives concrete improvement suggestions.
   - Summarizes top 3 immediate action priorities.

3. **Headline Advisor**
   - Generates 3–5 professional headline options (Direct, Keyword-rich / SEO, Value-driven, Hybrid).
   - Character count tracker ensuring adherence to LinkedIn's 220-character limit.
   - Clear explanations of why each headline works and when to use it.

4. **About / Summary Section Advisor**
   - Identifies strengths, structural weaknesses, and missing elements.
   - Provides a professionally rewritten About section featuring an engaging hook, background narrative, core competencies, real achievements, and a clear call-to-action (CTA).
   - **Zero Hallucination Guarantee:** Never invents fake awards, metrics, or employers.

5. **Skills Gap & Alignment Advisor**
   - Compares your current skills against industry benchmarks for your target job role.
   - Categorizes skills into:
     - Existing relevant skills
     - High-priority missing skills
     - Optional / nice-to-have skills
   - Explains why each recommended skill matters and suggests how to acquire it.

6. **Project Advisor (Google XYZ Formula)**
   - Audits existing projects for weaknesses or vague language.
   - Suggests searchable project titles.
   - Rewrites descriptions into recruiter-friendly bullet points using Google's XYZ formula (*Accomplished [X], measured by [Y], by doing [Z]*).
   - Recommends relevant skill tags and real-world deployment/impact ideas.

7. **Certifications & Experience Advisor**
   - Advises on how to showcase credentials and link associated skills on LinkedIn.
   - Transforms passive experience descriptions into high-impact bullets with strong action verbs and quantified impact.

8. **Internship Readiness Assessment**
   - Calculates an internship readiness score (0–100).
   - Highlights strengths, skill gaps, project complexity gaps, and experience gaps.
   - Provides a 4-week fast-track preparation plan to get recruiter-ready.

9. **Personalized Career Roadmap**
   - Choose between **30-day**, **60-day**, or **90-day** roadmaps.
   - Week-by-week actionable milestones covering technical upskilling, project milestones, networking targets, and interview prep.

10. **Resume vs. LinkedIn Comparison**
    - Compare pasted resume text against your LinkedIn profile.
    - Flags discrepancies, missing skills, omitted projects, and inconsistent phrasing to ensure seamless cross-platform alignment.

11. **Real-World Career Market Research**
    - Analyzes current industry hiring trends and in-demand skills for your target role.
    - Clearly distinguishes live market benchmarks from personalized user recommendations.

12. **Interactive AI Career Coach (Chat)**
    - Real-time conversational coach grounded in your profile details.
    - One-click prompt chips:
      - *"Improve my headline"*
      - *"Rewrite my About section"*
      - *"What skills am I missing?"*
      - *"Am I ready for an internship?"*
      - *"Improve my project description"*
      - *"Give me a 30-day improvement plan"*

---

## 🛠️ Technologies Used

- **Language:** Python (>= 3.9)
- **AI Model:** Google Gemini API (`gemini-3.8-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`)
- **SDKs:** `google-genai` (current official SDK) and `google-generativeai` (fallback)
- **UI Framework:** Streamlit
- **Configuration:** `python-dotenv` for environment variable security

---

## 📁 Project Structure

```text
AI Agent/
├── .env.example          # Environment variable template
├── .env                  # Your private API key (not tracked in Git)
├── requirements.txt      # Python dependencies
├── prompts.py            # Prompt engineering, safety guidelines, and system prompts
├── agent.py              # Gemini client wrapper, agent logic, and sample data
├── app.py                # Streamlit user interface and interactive tabs
└── README.md             # Complete documentation and setup guide
```

---

## 🚀 Getting Started

Follow these steps to set up and run the application locally on your computer.

### Step 1: Open the Project in VS Code
Open the project directory in VS Code or your terminal:
```bash
cd "c:\Users\Shreya\Documents\AI Agent"
```

### Step 2: Create and Activate a Virtual Environment (Recommended)

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Run pip to install the required libraries:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Gemini API Key

1. Get a free API key from Google AI Studio:
   👉 **[https://aistudio.google.com/](https://aistudio.google.com/)**
2. Create a `.env` file in the project root directory by copying `.env.example`:

**On Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**On macOS / Linux:**
```bash
cp .env.example .env
```

3. Open `.env` in VS Code and paste your actual Gemini API key:
```ini
GEMINI_API_KEY=AIzaSyYourActualGeminiAPIKeyHere
GEMINI_MODEL=gemini-3.8-flash
```

*(Security Note: The API key is securely loaded on the backend from `.env` and is never exposed in the browser or frontend UI).*

### Step 5: Run the Streamlit Application

Start the Streamlit development server:
```bash
streamlit run app.py
```

The app will automatically launch in your default web browser at:
👉 `http://localhost:8501`

---

## 💡 How to Use the Application

1. **Load or Enter Your Profile:**
   - In the sidebar, click **"📥 Load Sample Profile"** to instantly test with realistic student profile data, or fill in your own credentials in the **📋 Profile Input** tab.
   - Click **"💾 Save Profile Data"** to persist your profile.
2. **Audit Your Profile:**
   - Navigate to **📊 Profile Analysis** and click **"🚀 Run Full Profile Audit"** to view your overall score and breakdown across all 8 dimensions.
3. **Optimize Specific Sections:**
   - Go to **💡 Headline Advisor** to generate recruiter-ready headlines under 220 characters.
   - Go to **✍️ About Section** to review your current summary and get a high-converting rewritten pitch.
   - Go to **🎯 Skills Advisor** to view high-priority missing skills with specific justifications.
   - Go to **🚀 Project Advisor** to rewrite your projects using the Google XYZ impact format.
4. **Prepare for Opportunities:**
   - Check **🎓 Internship Readiness** for a readiness score and a 4-week prep schedule.
   - Generate a custom 30, 60, or 90-day action plan in **🗺️ Career Roadmap**.
   - Paste your resume into **📄 Resume Comparison** to identify missing skills or discrepancies.
5. **Chat with the Interactive Advisor:**
   - Head to **💬 Interactive AI Advisor** to chat freely or click any of the 6 quick prompt chips.

---

## 🔒 Safety and Accuracy Policy

This application is strictly built with anti-hallucination guardrails:
- **Never fabricates** past employers, company names, credentials, awards, or personal achievements.
- **Strictly separates** existing verified skills from *[RECOMMENDED SKILLS TO LEARN]*.
- All project and experience rewrites preserve truthfulness while optimizing for clarity, action verbs, and structure.

---

## 🤝 Troubleshooting

- **`GEMINI_API_KEY is not configured`:** Ensure your `.env` file exists in the project root and contains `GEMINI_API_KEY=your_key`.
- **Model quota or rate limit:** Switch the model in the sidebar dropdown (e.g. between `gemini-3.8-flash` and `gemini-2.0-flash`).
- **ModuleNotFoundError:** Ensure your virtual environment is activated and run `pip install -r requirements.txt`.
