# LangSmith Integration Guide

This app can integrate with **LangSmith** (smith.langchain.com) to track, monitor, and debug all LLM calls and chains in real-time.

## What is LangSmith?

LangSmith provides:
- 📊 **Real-time tracing** - See every LLM call, database query, and chain execution
- 🐛 **Debugging** - Identify bottlenecks and errors instantly
- 📈 **Analytics** - Track latency, token usage, and costs
- 💾 **Replay** - Test and replay specific conversations
- 🎯 **Monitoring** - Alert on failures or performance issues

## Setup Instructions

### 1. Create a LangSmith Account
- Go to [smith.langchain.com](https://smith.langchain.com)
- Sign up (free tier available)
- Create an API key in your account settings

### 2. Get Your LangSmith API Key
1. Log in to LangSmith
2. Click your profile icon → Settings
3. Copy your API key

### 3. Add LangSmith to .env
Edit your `.env` file and add:

```env
LANGCHAIN_TRACING_V2=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=akarsh-db-chat
```

Optional: Set `LANGSMITH_PROJECT` to organize traces by project.

### 4. Install/Update Dependencies
```bash
pip install -r requirements.txt
```

### 5. Restart Your App
```bash
./run.sh
```

## Monitoring Your App

Once enabled, visit [smith.langchain.com](https://smith.langchain.com) and you'll see:

### Real-time Traces
For each message in the chat, you'll see:
- **Input**: Your natural language question
- **SQL Chain**: Generated SQL query
- **Database Query**: Execution and results
- **Response Chain**: LLM-generated natural language answer
- **Latency**: Total time for each step
- **Tokens**: LLM token usage and costs

### Example Flow
```
User Message: "Which artists have the most tracks?"
  ↓
SQL Generation Chain
  ├─ Prompt with schema
  ├─ LLM call (Groq)
  └─ Generated: SELECT ArtistId, COUNT(*) as count FROM Track GROUP BY ArtistId...
  ↓
Database Execution
  └─ Result: 3 rows returned
  ↓
Response Chain
  ├─ Prompt with query result
  ├─ LLM call (Groq)
  └─ Response: "The top 3 artists are..."
```

All visible in LangSmith dashboard with timing breakdowns!

## Features You Can Monitor

### 1. Token Usage & Costs
- See exactly how many tokens each call used
- Track daily/monthly usage
- Monitor cost trends

### 2. Latency Analysis
- Identify slow queries
- Compare SQL generation time vs database time vs response generation time
- Optimize bottlenecks

### 3. Error Tracking
- See failed SQL queries
- Track API errors
- Debug exceptions

### 4. Conversation History
- Browse all past conversations
- Replay specific interactions
- Test new prompts without live changes

## Disable Tracing (Optional)

If you want to turn off tracing:
1. Set `LANGCHAIN_TRACING_V2=false` in `.env`
2. Or remove it entirely
3. Restart the app

Tracing is disabled by default - you must opt-in by setting `LANGCHAIN_TRACING_V2=true`.

## Privacy & Security

- LangSmith traces are sent securely to their servers
- Only traces (prompts, outputs, latencies) are sent - NOT your database contents
- You can always disable tracing
- Free tier has retention limits; paid plans offer longer history

## Troubleshooting

**Traces not appearing?**
- Verify `LANGCHAIN_TRACING_V2=true` in `.env`
- Verify `LANGSMITH_API_KEY` is correct
- Restart the app
- Check LangSmith dashboard for project name

**High latency?**
- Check if database queries are slow
- Monitor LLM response times
- Optimize SQL generation prompts

---

For more info, visit [LangSmith Documentation](https://docs.smith.langchain.com/)
