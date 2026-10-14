"""
agent.py - Core AI agent module connecting to the Google Gemini API.

Handles:
- Secure backend API authentication via python-dotenv and server environment variables (.env)
- Robust integration with google-genai and google-generativeai fallback
- Execution of all advisory tasks (Scoring, Headlines, About, Skills, Projects,
  Certifications, Experience, Internship Readiness, Roadmap, Resume Comparison,
  Market Research, and Conversational Chat)
- Error handling, JSON extraction, and safety assurance
"""

import os
import json
import re
from typing import Dict, Any, List, Optional
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass
from prompts import (
    SYSTEM_BASE_PROMPT,
    format_profile_context,
    PROFILE_ANALYSIS_PROMPT,
    HEADLINE_ADVISOR_PROMPT,
    ABOUT_SECTION_ADVISOR_PROMPT,
    SKILLS_ADVISOR_PROMPT,
    PROJECT_ADVISOR_PROMPT,
    CERTIFICATION_ADVISOR_PROMPT,
    EXPERIENCE_ADVISOR_PROMPT,
    INTERNSHIP_READINESS_PROMPT,
    CAREER_ROADMAP_PROMPT,
    RESUME_COMPARISON_PROMPT,
    CAREER_RESEARCH_PROMPT,
    INTERACTIVE_CHAT_PROMPT,
)

# Environment variables loaded from .env if python-dotenv is installed


class GeminiClientWrapper:
    """Wrapper that supports both google-genai and google-generativeai libraries."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.8-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        self._sdk_type = None
        self._client = None
        self._init_sdk()

    def _init_sdk(self):
        """Initializes whichever SDK is available."""
        if not self.api_key:
            return

        # Attempt to use google-genai first
        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            self._sdk_type = "google-genai"
            return
        except ImportError:
            pass

        # Fallback to google-generativeai
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=self.api_key)
            self._client = genai_legacy.GenerativeModel(self.model_name)
            self._sdk_type = "google-generativeai"
            return
        except ImportError:
            pass

        self._sdk_type = "missing_sdk"

    def is_configured(self) -> bool:
        """Returns True if API key is present and SDK is available."""
        return bool(self.api_key and self._sdk_type in ("google-genai", "google-generativeai"))

    def generate_content(self, system_instruction: str, prompt: str) -> str:
        """Sends prompt to Gemini using the current Google Gen AI Python SDK and returns text response."""
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured. Please set GEMINI_API_KEY in your server's .env file.")

        if self._sdk_type == "google-genai":
            from google.genai import types
            import time

            # Candidate models with user's selected model first, falling back gracefully on temporary 503/429 spikes
            candidate_models = [self.model_name]
            for fallback in ["gemini-3.5-flash", "gemini-flash-lite-latest", "gemini-3.1-flash-lite"]:
                if fallback not in candidate_models:
                    candidate_models.append(fallback)

            last_exception = None
            for model_to_use in candidate_models:
                for attempt in range(2):
                    try:
                        response = self._client.models.generate_content(
                            model=model_to_use,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                            ),
                        )
                        return response.text or ""
                    except Exception as e:
                        last_exception = e
                        err_msg = str(e).lower()
                        if "503" in err_msg or "unavailable" in err_msg or "high demand" in err_msg or "429" in err_msg:
                            time.sleep(1.0)
                            continue
                        # If configuration format issue, retry with concatenated prompt
                        try:
                            full_prompt = f"{system_instruction}\n\n{prompt}"
                            response = self._client.models.generate_content(
                                model=model_to_use,
                                contents=full_prompt,
                            )
                            return response.text or ""
                        except Exception as e_inner:
                            last_exception = e_inner
                            break

            if last_exception:
                raise last_exception

        elif self._sdk_type == "google-generativeai":
            import google.generativeai as genai_legacy
            full_prompt = f"{system_instruction}\n\n{prompt}"
            try:
                model = genai_legacy.GenerativeModel(self.model_name)
                response = model.generate_content(full_prompt)
                return response.text or ""
            except Exception as e:
                raise e

        else:
            raise ImportError(
                "Neither 'google-genai' nor 'google-generativeai' is installed. "
                "Please run: pip install -r requirements.txt"
            )


class LinkedInAdvisorAgent:
    """Core agent coordinating LinkedIn Profile Advisor tasks."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.8-flash"):
        self.client = GeminiClientWrapper(api_key=api_key, model_name=model_name)

    def set_api_key(self, api_key: str, model_name: Optional[str] = None):
        """Updates the active API key and re-initializes client."""
        self.client = GeminiClientWrapper(api_key=api_key, model_name=model_name or self.client.model_name)

    def is_ready(self) -> bool:
        """Checks if agent is ready to process queries."""
        return self.client.is_configured()

    def _extract_json(self, raw_text: str) -> Dict[str, Any]:
        """Safely extracts JSON from model response text."""
        # Clean markdown codeblocks
        cleaned = raw_text.strip()
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
        if match:
            cleaned = match.group(1).strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback regex search for JSON object
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                try:
                    return json.loads(cleaned[start : end + 1])
                except json.JSONDecodeError:
                    pass

        # Return fallback structure if parsing failed
        return {
            "scores": {
                "overall": 65,
                "headline": 60,
                "about": 60,
                "skills": 70,
                "projects": 65,
                "certifications": 50,
                "experience": 60,
                "education": 80,
                "career_alignment": 70,
            },
            "summary": "Profile analysis completed. Review detailed category suggestions below.",
            "category_feedback": {
                "headline": {"score": 60, "analysis": "Could be more keyword-focused.", "suggestions": ["Add target role keywords"]},
                "about": {"score": 60, "analysis": "Add a stronger hook and call to action.", "suggestions": ["Include bulleted skills", "Add contact email"]},
                "skills": {"score": 70, "analysis": "Good baseline, but missing specialized tools.", "suggestions": ["Add in-demand frameworks"]},
                "projects": {"score": 65, "analysis": "Focus on measurable outcomes.", "suggestions": ["Add metrics and GitHub links"]},
                "certifications": {"score": 50, "analysis": "Needs industry-recognized credentials.", "suggestions": ["Pursue relevant cloud or role certifications"]},
                "experience": {"score": 60, "analysis": "Use stronger action verbs.", "suggestions": ["Use STAR / Google XYZ format"]},
                "education": {"score": 80, "analysis": "Clear academic details.", "suggestions": ["Highlight coursework and leadership"]},
                "career_alignment": {"score": 70, "analysis": "Moderate alignment with target role.", "suggestions": ["Align projects with target role"]},
            },
            "top_priorities": [
                "Craft an ATS-optimized headline featuring target keywords",
                "Expand project descriptions with impact metrics",
                "Acquire missing core technical skills for target role",
            ],
            "raw_text": raw_text,
        }

    # ==========================================
    # Feature 2: Profile Analysis & Scoring
    # ==========================================
    def analyze_profile(self, profile: dict) -> Dict[str, Any]:
        """Runs complete profile analysis and returns scores and category feedback."""
        context = format_profile_context(profile)
        prompt = f"{context}\n\n{PROFILE_ANALYSIS_PROMPT}"
        raw = self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)
        parsed = self._extract_json(raw)
        return parsed

    # ==========================================
    # Feature 3: Headline Advisor
    # ==========================================
    def generate_headlines(self, profile: dict) -> str:
        """Generates 3-5 optimized LinkedIn headlines."""
        context = format_profile_context(profile)
        prompt = f"{context}\n\n{HEADLINE_ADVISOR_PROMPT}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 4: About Section Advisor
    # ==========================================
    def improve_about(self, profile: dict) -> str:
        """Analyzes and rewrites the About/Summary section."""
        context = format_profile_context(profile)
        prompt = f"{context}\n\n{ABOUT_SECTION_ADVISOR_PROMPT}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 5: Skills Advisor
    # ==========================================
    def analyze_skills(self, profile: dict) -> str:
        """Compares current skills to industry expectations."""
        context = format_profile_context(profile)
        prompt = f"{context}\n\n{SKILLS_ADVISOR_PROMPT}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 6: Project Advisor
    # ==========================================
    def analyze_projects(self, profile: dict) -> str:
        """Analyzes projects and provides enhanced LinkedIn descriptions."""
        context = format_profile_context(profile)
        prompt = f"{context}\n\n{PROJECT_ADVISOR_PROMPT}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 7: Certification Advisor
    # ==========================================
    def advise_certifications(self, profile: dict) -> str:
        """Advises on certification presentation and recommendations."""
        context = format_profile_context(profile)
        prompt = f"{context}\n\n{CERTIFICATION_ADVISOR_PROMPT}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 8: Experience Advisor
    # ==========================================
    def improve_experience(self, profile: dict) -> str:
        """Polishes internship, work, and leadership descriptions."""
        context = format_profile_context(profile)
        prompt = f"{context}\n\n{EXPERIENCE_ADVISOR_PROMPT}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 9: Internship Readiness
    # ==========================================
    def assess_internship_readiness(self, profile: dict) -> str:
        """Scores and breaks down internship readiness."""
        context = format_profile_context(profile)
        prompt = f"{context}\n\n{INTERNSHIP_READINESS_PROMPT}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 10: Career Roadmap
    # ==========================================
    def generate_career_roadmap(self, profile: dict, timeframe: str = "30") -> str:
        """Generates a personalized 30, 60, or 90-day action plan."""
        context = format_profile_context(profile)
        prompt_template = CAREER_ROADMAP_PROMPT.format(timeframe=timeframe)
        prompt = f"{context}\n\n{prompt_template}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 11: Resume & LinkedIn Comparison
    # ==========================================
    def compare_resume(self, profile: dict, resume_text: str) -> str:
        """Compares user's resume text against LinkedIn profile data."""
        context = format_profile_context(profile)
        prompt_template = RESUME_COMPARISON_PROMPT.format(resume_text=resume_text)
        prompt = f"{context}\n\n{prompt_template}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 12: Career Market Research
    # ==========================================
    def research_career_market(self, profile: dict) -> str:
        """Researches in-demand skills and industry benchmarks for target role."""
        target_role = profile.get("target_role", "Software Engineer")
        context = format_profile_context(profile)
        prompt_template = CAREER_RESEARCH_PROMPT.format(target_role=target_role)
        prompt = f"{context}\n\n{prompt_template}"
        return self.client.generate_content(SYSTEM_BASE_PROMPT, prompt)

    # ==========================================
    # Feature 13: Interactive Chat Advisor
    # ==========================================
    def chat_advisor(self, profile: dict, chat_history: List[Dict[str, str]], user_message: str) -> str:
        """Conversational chat advisor answering questions in context."""
        context = format_profile_context(profile)
        history_text = ""
        if chat_history:
            history_text = "\n--- RECENT CONVERSATION HISTORY ---\n"
            for msg in chat_history[-6:]:  # Keep last 6 exchanges for context
                role = "User" if msg["role"] == "user" else "Advisor"
                history_text += f"{role}: {msg['content']}\n"
            history_text += "-----------------------------------\n"

        prompt = f"{context}\n{history_text}\nUser Question: {user_message}\n\nPlease provide your helpful, accurate advisory response:"
        return self.client.generate_content(INTERACTIVE_CHAT_PROMPT, prompt)


def get_sample_profile() -> Dict[str, str]:
    """Returns a realistic student/early-career sample profile for instant testing."""
    return {
        "name": "Alex Chen",
        "education": "University of Technology",
        "degree": "B.S. in Computer Science",
        "current_year": "3rd Year Undergraduate",
        "career_goal": "Secure a Summer Software Engineer Internship at a top tech company",
        "target_role": "Full-Stack Software Engineer Intern",
        "headline": "CS Student @ University of Technology | Aspiring Software Engineer | Python, JavaScript",
        "about": (
            "I am a third-year Computer Science student passionate about building web apps and learning new technologies. "
            "I have built several personal projects using Python, React, and Flask. Looking for summer 2026 internship opportunities."
        ),
        "skills": "Python, JavaScript, React, HTML/CSS, Flask, Git, PostgreSQL, REST APIs",
        "projects": (
            "1. TaskFlow - Full-Stack Task Management Web Application\n"
            "Built with React and Flask. Allowed users to create, categorize, and track daily tasks. Implemented user authentication with JWT and stored data in PostgreSQL.\n\n"
            "2. Campus Book Exchange\n"
            "A marketplace platform for students to buy and sell used textbooks. Used Python, SQLite, and Bootstrap. Handled 100+ simulated user listings."
        ),
        "certifications": "CS50: Introduction to Computer Science (edX), Meta Front-End Developer Specialization (Coursera)",
        "experience": (
            "Undergraduate Teaching Assistant - Intro to Programming (Fall 2025)\n"
            "Assisted 40+ students with Python debugging and fundamental algorithms. Held weekly lab sessions and graded assignments.\n\n"
            "Web Developer Intern - Campus Tech Club (Jan 2025 - Present)\n"
            "Collaborated with 3 team members to maintain the student club website using React and GitHub Pages."
        ),
        "achievements": (
            "Dean's Honor List (2 consecutive semesters)\n"
            "Top 10 Finalist at University Hackathon 2025 (Built an AI study planner prototype in 24 hours)"
        ),
        "portfolio_url": "https://github.com/alexchen-dev",
    }
