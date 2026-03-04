<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center">

[![Forked from TauricResearch](https://img.shields.io/badge/forked%20from-TauricResearch%2FTradingAgents-blue?logo=github)](https://github.com/TauricResearch/TradingAgents)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-7C3AED?logo=data:image/svg+xml;base64,)](https://openclaw.ai)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-powered-orange)](https://github.com/langchain-ai/langgraph)
[![arXiv](https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv)](https://arxiv.org/abs/2412.20138)

</div>

---

# TauricResearch-Skill — OpenClaw Skill

> **Forked from [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)**  
> This repository adapts the original multi-agent LLM trading framework as a native **OpenClaw Skill**, so it can be triggered conversationally through OpenClaw agents and routed exclusively through the OpenClaw CLI — no separate LLM API keys required.

---

## What Was Changed

This fork preserves the **entire original TauricResearch architecture** (LangGraph state machine, analyst/researcher/trader/risk roles, in-memory debate flow) and makes the following additions:

| Layer | Original | This Fork |
|-------|----------|-----------|
| **LLM Provider** | OpenAI / Anthropic / Google (direct APIs) | `ChatOpenClawCLI` — routes 100% of LLM calls through `openclaw agent` CLI |
| **Orchestration** | LangGraph state machine | Preserved exactly as original |
| **Data Sources** | Yahoo Finance, Alpha Vantage, SEC EDGAR | + Guru Signals (13F/Congressional), Breaking News Catalyst Cache, Hedge Fund Ownership |
| **Skill Registration** | None | `SKILL.md` — OpenClaw agents trigger this natively |
| **API Keys** | Required per provider | Not required — OpenClaw gateway handles routing |

---

## Architecture

```
User (conversational): "Analyze NVDA using Tauric"
        │
        ▼
   OpenClaw Gateway (reads SKILL.md, detects trigger)
        │
        ▼
   TauricResearch LangGraph
   ┌─────────────────────────────────────────────────────────┐
   │  Market Analyst  ──── get_stock_data, get_indicators    │
   │  News Analyst    ──── get_news, get_breaking_news_*     │
   │  Social Analyst  ──── get_news                          │  
   │  Fundamentals    ──── get_fundamentals, get_guru_*      │
   └─────────────────────────────────────────────────────────┘
        │
        │  All LLM calls
        ▼
   ChatOpenClawCLI
   subprocess(["openclaw", "agent", "--agent", "main", "--message", ...])
        │
        ▼
   Bull vs Bear Debate → Judge → Decision (BUY / SELL / HOLD)
```

---

## Installation

### 1. Install as an OpenClaw Skill

```bash
git clone https://github.com/oabdelmaksoud/TauricResearch-Skill.git ~/.openclaw/skills/TauricResearch-Skill
```

OpenClaw will auto-discover the skill via `SKILL.md`. No restart required.

### 2. Install Python Dependencies

```bash
cd ~/.openclaw/skills/TauricResearch-Skill
pip install -r requirements.txt
```

### 3. No API Keys Needed

All LLM inference routes through your OpenClaw gateway. The only optional keys are for market data:

```bash
# Optional — market data sources (defaults to Yahoo Finance if not set)
ALPHA_VANTAGE_API_KEY=...
FINNHUB_API_KEY=...
ALPACA_API_KEY=...
ALPACA_SECRET_KEY=...
```

Copy `.env.example` to `.env` and fill in any optional keys:
```bash
cp .env.example .env
```

---

## Usage

### Conversational (via OpenClaw)

Just talk to any OpenClaw agent:
> *"Run a Tauric analysis on NVDA"*  
> *"Should I buy or sell MSFT? Use the multi-agent framework."*

### CLI

```bash
cd ~/.openclaw/skills/TauricResearch-Skill
python -m cli.main
```

Or programmatically:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Defaults to OpenClaw CLI provider — no API key setup required
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)  # BUY / SELL / HOLD
```

### Advanced: Select a different OpenClaw agent

```python
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "macro"   # Use your 'macro' OpenClaw agent for deep reasoning
config["quick_think_llm"] = "main"   # Use 'main' for fast tasks
config["max_debate_rounds"] = 2

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
print(decision)
```

---

## ProTrader Data Tools

This fork adds three new LangGraph `@tool` functions bound to the analyst nodes:

| Tool | Analyst | Source |
|------|---------|--------|
| `get_guru_signals(ticker)` | News + Fundamentals | Congressional STOCK Act buys, hedge fund 13F filings, GuruFocus RSS |
| `get_breaking_news_catalysts(ticker)` | News | Tier 1/2 events from a 24/7 RSS + Finnhub cache |
| `get_institutional_ownership(ticker)` | Fundamentals | Live SEC EDGAR 13F holdings for 6 major funds |

These tools require no configuration. `get_guru_signals` and `get_breaking_news_catalysts` read from `logs/` files populated by standalone cron jobs (optional).

---

## Key Files in This Fork

```
TauricResearch-Skill/
├── SKILL.md                                       ← OpenClaw registration
├── tradingagents/
│   ├── default_config.py                          ← Provider defaults to 'openclaw'
│   ├── llm_clients/
│   │   ├── openclaw_client.py                     ← ChatOpenClawCLI (BaseChatModel)
│   │   └── openclaw_client_wrapper.py             ← OpenClawClient (BaseLLMClient)
│   ├── agents/utils/
│   │   └── protrader_tools.py                     ← 3 new LangGraph @tool functions
│   └── graph/
│       └── trading_graph.py                       ← ProTrader tools wired in ToolNodes
└── [all original TauricResearch files preserved]
```

---

## Credits

- **Original Framework:** [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) — *Multi-Agents LLM Financial Trading Framework* ([arXiv:2412.20138](https://arxiv.org/abs/2412.20138))
- **OpenClaw Adaptation:** [@oabdelmaksoud](https://github.com/oabdelmaksoud)

---

## Citation

If you use this work, please cite the original TradingAgents paper:

```bibtex
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```

---

> **Disclaimer:** This framework is designed for research purposes only. Trading performance may vary. It is not intended as financial, investment, or trading advice. See [Tauric disclaimer](https://tauric.ai/disclaimer/).
