import os
from google import genai
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("AIzaSyA7MFbFDvn35OHFjTMpRstq2bPCxlrhksI"))

# ── TO SWITCH TO GROQ LATER ─────────────────────────────────────────────────
# from groq import Groq
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# ────────────────────────────────────────────────────────────────────────────

def analyze_portfolio(holdings: list) -> dict:
    """
    Takes a list of holdings and returns AI-generated portfolio analysis.

    holdings format:
    [
        {"asset": "stocks", "amount": 50000},
        {"asset": "gold",   "amount": 20000},
    ]
    """
    total = sum(h.get("amount", 0) for h in holdings)

    # Build holdings summary
    holdings_text = ""
    for h in holdings:
        asset  = h.get("asset", "Unknown")
        amount = h.get("amount", 0)
        pct    = (amount / total * 100) if total > 0 else 0
        holdings_text += f"- {asset}: Rs.{amount:,.0f} ({pct:.1f}%)\n"

    prompt = f"""
You are a senior financial advisor analyzing a young Indian investor's portfolio.

Their current portfolio (Total: Rs.{total:,.0f}):
{holdings_text}

Give a structured analysis in this exact format:

RISK PROFILE: [Conservative / Moderate / Aggressive]

OVERVIEW:
2-3 sentences summarizing the portfolio composition and overall risk level.

STRENGTHS:
2 specific strengths of this portfolio allocation.

CONCERNS:
2 specific concerns or risks with this allocation.

RECOMMENDATION:
2-3 sentences on how to improve or rebalance. Be specific with percentages.

Keep the entire response under 200 words. Use simple language. No bullet points inside sections, just flowing text.
"""

    try:
        text = ""
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
                text = response.text.strip()
                break
            except Exception as e:
                if '503' in str(e) and attempt < 2:
                    time.sleep(2)
                    continue
                raise e

        # Parse sections
        def extract(label, text):
            try:
                start = text.index(label) + len(label)
                # Find next section
                next_labels = ["OVERVIEW:", "STRENGTHS:", "CONCERNS:", "RECOMMENDATION:"]
                end = len(text)
                for nl in next_labels:
                    if nl in text[start:]:
                        end = min(end, text.index(nl, start))
                return text[start:end].strip()
            except:
                return ""

        risk_profile = extract("RISK PROFILE:", text)
        overview     = extract("OVERVIEW:", text)
        strengths    = extract("STRENGTHS:", text)
        concerns     = extract("CONCERNS:", text)
        recommendation = extract("RECOMMENDATION:", text)

        return {
            "success":        True,
            "total":          total,
            "risk_profile":   risk_profile,
            "overview":       overview,
            "strengths":      strengths,
            "concerns":       concerns,
            "recommendation": recommendation,
            "raw":            text,
        }

    except Exception as e:
        print("Profiler error:", e)
        return {
            "success":        False,
            "total":          total,
            "risk_profile":   "Unable to analyze",
            "overview":       f"Portfolio analysis unavailable at this time. Total portfolio value: Rs.{total:,.0f}.",
            "strengths":      "",
            "concerns":       "",
            "recommendation": "Please try again later.",
            "raw":            str(e),
        }