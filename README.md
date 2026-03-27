# OpenClaw Workspace

Personal AI assistant workspace configuration and documentation for OpenClaw.

## Overview

This repository contains the setup, configuration, and documentation for running OpenClaw AI assistant with Ollama cloud models (specifically Kimi K2.5).

## Key Files

| File | Description |
|------|-------------|
| [`Skills.md`](Skills.md) | Current capabilities and integrations |
| [`USAGE_TRACKER.md`](USAGE_TRACKER.md) | Ollama Free Tier usage monitoring |
| [`MODEL_GUIDE.md`](MODEL_GUIDE.md) | Kimi/Ollama/OpenClaw architecture guide |
| [`QUICKSTART.md`](QUICKSTART.md) | Quick start and restart procedures |
| [`check-usage.sh`](check-usage.sh) | Script to check current usage status |

## Quick Start

```bash
# Start OpenClaw with Kimi
openclaw chat --model ollama/kimi-k2.5:cloud

# Check status
openclaw status

# Check usage limits
./check-usage.sh
```

## Architecture

```
You → OpenClaw → Ollama → Kimi K2.5
```

- **OpenClaw**: Orchestrator (tools, sessions, memory)
- **Ollama**: Model runner (API access)
- **Kimi K2.5**: AI model (generates responses)

See [MODEL_GUIDE.md](MODEL_GUIDE.md) for detailed explanation.

## Current Status

- ✅ Usage Tracker: Active (30-min polling)
- ✅ Notion Integration: Connected
- ✅ GitHub Integration: Configured
- ❌ iMessage: Removed (switched to alternative)

## Links

- [GitHub Repository](https://github.com/vikasvmohite1776/openclaw-workspace)
- [Notion Page](https://www.notion.so/)

---

*Last updated: March 27, 2026*
