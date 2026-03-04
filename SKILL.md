---
name: TauricResearch-Skill
description: "This skill should be used when the user asks to analyze a stock, perform fundamental or technical trading analysis, run the Tauric framework, debate a stock's potential, or generate a trading decision. It executes the TauricResearch LangGraph trading pipeline."
metadata:
  {
    "openclaw":
      {
        "emoji": "📈"
      }
  }
---

# TauricResearch-Skill

This skill provides access to the **TauricResearch TradingAgents** framework, a multi-agent system that simulates a real-world trading firm. It employs a team of LLM analysts (Fundamentals, News, Sentiment, Technical) and a debate engine (Bull vs. Bear) to arrive at high-conviction trading decisions.

## When to use this skill

Activate this skill when the user requests:
- "Analyze [TICKER] using Tauric"
- "Run a fundamental analysis on AAPL"
- "Should I buy or sell NVDA?"
- "Start a trading debate on MSFT"
- "What is the market sentiment for TSLA?"

## How to execute

This skill relies on a Python pipeline located in this directory.

To run an analysis for a specific ticker (e.g., AAPL), execute the following command:

```bash
cd ~/.openclaw/skills/TauricResearch-Skill && python cli/main.py --ticker AAPL
```

### Supported Arguments
- `--ticker`: The stock symbol to analyze (e.g., NVDA, MSFT).
- `--rounds`: (Optional) The number of debate rounds between the Bull and Bear agents (default: 2).

## Pipeline Execution Details
When executed, the system will output logs to the console as it performs the following steps:
1. **Data Collection**: Gathers stock data, fundamentals, technical indicators, and breaking news using LangGraph Tools.
2. **Analysis**: Specialized agents (Flash, Macro, Pulse) generate individual reports.
3. **Debate**: The Bull and Bear agents debate the merits and risks of the trade based on the reports.
4. **Decision**: A final Trader/Risk node evaluates the debate and determines the optimal action (BUY/SELL/HOLD).

You should present the final output and decision summary to the user in a clear, formatted message.
