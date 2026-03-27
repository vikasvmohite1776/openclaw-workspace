# Skills.md - Available Capabilities

## Core Skills
- **Web Search**: Via web_search/web_fetch tools (Gemini with Google Search)
- **Notion**: Read/write pages and databases
- **Session Spawning**: Can spawn isolated sub-agents for complex tasks
- **Cron/Scheduling**: Automated periodic tasks
- **GitHub**: Repositories, issues, PRs (vikasvmohite1776) ✅ Token configured
- **Usage Tracker**: Ollama Free Tier monitoring with automated warnings

## Workflow Triggers
- Context limit reached → Summarize → Write to Context.md → Spawn fresh session → Resume

## Usage Notes
- Web search: `web_search` tool (Gemini configured)
- Notion: API configured, key at `~/.config/notion/api_key`
- Session spawn: `sessions_spawn` with runtime="subagent"
- GitHub: Need personal access token (classic or fine-grained)
- Usage Tracker: Check `USAGE_TRACKER.md` or run `check-usage.sh`

## Ollama Free Tier Limits
- **5-hour session window** - Resets every 5 hours of active use
- **Weekly limit** - 7 days
- **1 concurrent model** max
- **Warnings**: Automated alerts at 80% (4 hours) and 100% (5 hours)
- **Upgrade**: Pro ($20/mo) = 50x more usage

## Status
- **iMessage**: ❌ Removed (switched to alternative messenger)
- **Usage Tracker**: ✅ Active with 30-min polling
