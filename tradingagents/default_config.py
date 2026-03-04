import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings — Use OpenClaw CLI as the provider.
    # 'deep_think_llm' and 'quick_think_llm' map to OpenClaw agent IDs.
    # Override via env: TRADINGAGENTS_LLM_PROVIDER, TRADINGAGENTS_DEEP_LLM, TRADINGAGENTS_QUICK_LLM
    "llm_provider": os.getenv("TRADINGAGENTS_LLM_PROVIDER", "openclaw"),
    "deep_think_llm": os.getenv("TRADINGAGENTS_DEEP_LLM", "main"),
    "quick_think_llm": os.getenv("TRADINGAGENTS_QUICK_LLM", "main"),
    # Backend URL not required for OpenClaw CLI (handled internally by the gateway).
    # Set to None unless using a direct OpenAI/Anthropic provider.
    "backend_url": os.getenv("TRADINGAGENTS_BACKEND_URL", None),
    # Provider-specific thinking configuration
    "google_thinking_level": None,      # "high", "minimal", etc.
    "openai_reasoning_effort": None,    # "medium", "high", "low"
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Data vendor configuration
    # Category-level configuration (default for all tools in category)
    "data_vendors": {
        "core_stock_apis": "yfinance",       # Options: alpha_vantage, yfinance
        "technical_indicators": "yfinance",  # Options: alpha_vantage, yfinance
        "fundamental_data": "yfinance",      # Options: alpha_vantage, yfinance
        "news_data": "yfinance",             # Options: alpha_vantage, yfinance
    },
    # Tool-level configuration (takes precedence over category-level)
    "tool_vendors": {
        # Example: "get_stock_data": "alpha_vantage",  # Override category default
    },
}
