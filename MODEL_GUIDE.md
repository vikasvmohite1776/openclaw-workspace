# Model Launch Guide - Kimi with OpenClaw

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        YOU (User)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    OPENCLAW (Orchestrator)                  │
│         • Your AI assistant interface                       │
│         • Manages sessions, tools, and workflows             │
│         • Routes requests to appropriate models              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     OLLAMA (Model Runner)                     │
│         • Downloads and runs AI models locally or cloud      │
│         • Provides API for model inference                   │
│         • Manages model weights and execution                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   KIMI K2.5 (The AI Model)                  │
│         • Large language model by Moonshot AI                │
│         • Actually generates responses                       │
│         • Runs via Ollama Cloud service                    │
└─────────────────────────────────────────────────────────────┘
```

## What Each Component Does

### 1. **Kimi K2.5** 🧠
- **What:** A large language model (like GPT-4, Claude, etc.)
- **Who made it:** Moonshot AI (Chinese AI company)
- **What it does:** Actually thinks and generates text
- **Analogy:** It's the *brain* that does the thinking

### 2. **Ollama** 🖥️
- **What:** A tool that runs AI models
- **What it does:** 
  - Downloads models to your computer
  - Provides an API to talk to models
  - Offers cloud-hosted models (like kimi-k2.5:cloud)
- **Analogy:** It's the *interpreter* that translates between you and the brain

### 3. **OpenClaw** 🤖
- **What:** Your personal AI assistant framework
- **What it does:
  - Manages conversations and sessions
  - Provides tools (web search, file editing, etc.)
  - Routes tasks to appropriate models
  - Handles memory, skills, and workflows
- **Analogy:** It's the *assistant* that organizes everything

## Why You Need All Three

| Component | Role | Without It |
|-----------|------|------------|
| **Kimi** | Intelligence | No AI to think/respond |
| **Ollama** | Model Access | No way to run the AI model |
| **OpenClaw** | Orchestration | No tools, memory, or session management |

**Think of it like a restaurant:**
- **Kimi** = The chef (creates the food)
- **Ollama** = The kitchen equipment (cooks the food)
- **OpenClaw** = The waiter + restaurant manager (takes orders, brings food, remembers preferences)

## Correct Commands

### ❌ Incorrect Command
```bash
ollama launch openclaw --model kimi-k2.5:cloud
```
This doesn't work because:
- `ollama` doesn't have a "launch openclaw" command
- The syntax is wrong

### ✅ Correct Commands

**Check current model:**
```bash
openclaw status
```

**Start OpenClaw with a specific model:**
```bash
openclaw chat --model ollama/kimi-k2.5:cloud
```

**Or set default model in config:**
```bash
# Edit ~/.openclaw/config.yaml
default_model: ollama/kimi-k2.5:cloud
```

**Available Ollama Models:**
```bash
ollama list                    # Local models
ollama pull llama3.2          # Download a model
ollama run llama3.2           # Run model directly
```

**Switch models mid-session:**
```bash
/status model=<model-name>     # In chat
```

## Model Format Explained

```
ollama/kimi-k2.5:cloud
└───┬───┘ └──┬──┘ └──┬──┘
    │        │       │
 Provider  Model   Variant
  (Ollama) (Kimi)  (Cloud-hosted)
```

**Other examples:**
- `ollama/llama3.2:latest` - Meta's Llama model (local)
- `ollama/qwen2.5:14b` - Alibaba's Qwen model (local, 14B params)
- `ollama/deepseek-coder:latest` - DeepSeek code model

## Quick Reference

| Task | Command |
|------|---------|
| Start OpenClaw | `openclaw` or `openclaw chat` |
| Check status | `openclaw status` |
| List Ollama models | `ollama list` |
| Pull new model | `ollama pull <model>` |
| Run model directly | `ollama run <model>` |
| View model info | `ollama show <model>` |

## Troubleshooting

**"Model not found" error:**
```bash
ollama pull kimi-k2.5:cloud    # Download if available locally
# OR use cloud version which doesn't require download
```

**Rate limit errors:**
- See USAGE_TRACKER.md for Ollama Cloud limits
- Consider upgrading to Ollama Pro ($20/mo)

**Slow responses:**
- Large models = slower but smarter
- Cloud models depend on Ollama's infrastructure
- Local models depend on your hardware
