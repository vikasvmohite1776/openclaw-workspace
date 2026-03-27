#!/bin/bash
# Quick usage check for Ollama Free Tier

echo "🦀 OpenClaw Usage Tracker"
echo "========================"

# Check if we can get status
if command -v openclaw &> /dev/null; then
    openclaw status 2>/dev/null | head -20
else
    echo "⚠️  openclaw CLI not found in PATH"
fi

echo ""
echo "📊 Manual Tracker: ~/.openclaw/workspace/USAGE_TRACKER.md"
echo "⏰ 5-hour window resets every 5 hours of active use"
echo "💡 Tip: Long sessions with large models = faster limit hit"
