import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("AIzaSyA7MFbFDvn35OHFjTMpRstq2bPCxlrhksI"))

def explain_portfolio(data: dict) -> str:
    asset_labels = {
        "stocks":       "Stocks (Equity)",
        "mutual_funds": "Mutual Funds",
        "crypto":       "Cryptocurrency",
        "bonds":        "Bonds",
        "gold":         "Gold",
    }

    asset  = asset_labels.get(data.get("asset_type", "stocks"), "Stocks")
    amount = data.get("initial", 0)
    years  = data.get("years", 10)
    avg    = data.get("avg", 0)
    best   = data.get("best", 0)
    worst  = data.get("worst", 0)
    loss   = data.get("loss_prob", 0)
    gain   = data.get("total_gain", 0)

    prompt = f"""
You are a friendly financial advisor explaining investment simulation results to a young first-time investor in India.

Simulation details:
- Asset: {asset}
- Initial Investment: Rs.{amount:,.0f}
- Time Horizon: {years} years
- Average Outcome: Rs.{avg:,.0f}
- Best Case (95th percentile): Rs.{best:,.0f}
- Worst Case (5th percentile): Rs.{worst:,.0f}
- Loss Probability: {loss}%
- Total Expected Gain: {gain}%

Write a 3-4 sentence plain-language explanation of these results.
- Be direct and honest about the risk
- Use simple words, no jargon
- Mention whether this is a good investment for a beginner
- End with one actionable tip
- Do NOT use bullet points, just flowing paragraphs
- Keep it under 80 words
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return f"Unable to generate AI explanation. {loss}% chance of loss with {gain}% expected gain over {years} years."