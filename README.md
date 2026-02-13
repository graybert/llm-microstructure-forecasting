# LLM Microstructure Forecasting

3-arms prediction pipeline for forecasting prediction market outcomes using market microstructure data.

## Pipelines

### 1. Technical Pipeline (`pipeline_3arms_technical_final.ipynb`)

**Input:**
- `data/markets_microstructure_v2_v3_merged.csv` (1,844 markets with microstructure features)

**Output:**
- `data/output/predictions_3arms_technical.csv`

**What it does:**
- Queries Groq LLM (llama-3.1-8b-instant) for probability predictions
- Three arms:
  - **Baseline**: Title + mid_yes prior only
  - **Volume**: Baseline + volume/liquidity metrics
  - **Full Technical**: Volume + all technical indicators (returns, volatility, spreads, etc.)
- Async processing with concurrency=8, includes retry logic
- No web search, pure market microstructure signals

**Status:** Ran but hit Groq rate limits (30 RPM). ~60% successful predictions before errors.

---

### 2. Web Search Pipeline (`pipeline_3arms_with_web_search.ipynb`)

**Input:**
- `data/markets_microstructure_v2_v3_merged.csv` (1,844 markets)

**Output:**
- `data/tavily_cache.jsonl` (Stage A: web search cache)
- `data/output/predictions_3arms_with_web.csv.tmp` (Stage B: predictions)

**What it does:**

**Stage A - Web Search (100% complete ✅):**
- Tavily API searches for each market's question
- Caches 4 search results per market to `tavily_cache.jsonl`
- Rate limited to 100 RPM
- All 1,844 markets successfully cached

**Stage B - LLM Inference (failed ❌):**
- Same 3 arms as technical pipeline, but prompts include web search context
- Queries Groq LLM with web results appended to prompts
- Hit rate limits immediately: <1% successful predictions

**Status:** Stage A complete, Stage B failed due to rate limits.

---

## Rate Limit Issue

Both pipelines hit **Groq API rate limits**:
- 30 requests per minute (RPM)
- 6,000 tokens per minute (TPM)

With 5,532 total calls needed (1,844 markets × 3 arms), this causes severe throttling.

**Solutions:**
1. **Batch with delays**: Process 25 markets at a time, wait 3 minutes between batches (~8-10 hours, free)
2. **Switch to OpenAI**: Use gpt-4o-mini with 500 RPM limit (~$0.88, 45 minutes)
3. **Switch to Anthropic**: Use Claude Haiku (~$1.50, 60 minutes)

See `analyze_pipeline_outputs.ipynb` for detailed analysis.

---

## Files

**Pipelines:**
- `pipeline_3arms_technical_final.ipynb` - Technical features only
- `pipeline_3arms_with_web_search.ipynb` - Technical + web search

**Data:**
- `data/markets_microstructure_v2_v3_merged.csv` - Input dataset (1,844 markets, 26 features)
- `data/tavily_cache.jsonl` - Web search results cache (3 MB, 1,844 records)
- `data/output/predictions_3arms_with_web.csv.tmp` - Partial predictions (mostly errors)

**Analysis:**
- `analyze_pipeline_outputs.ipynb` - Notebook to analyze usable predictions and errors

**Other:**
- `test_api_quick.py` - Groq API connection test
- `requirements.txt` - Python dependencies
