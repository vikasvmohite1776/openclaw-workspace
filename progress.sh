#!/bin/bash
# Progress bar wrapper for long-running commands
# Usage: progress "Description" command [args...]

progress() {
    local desc="$1"
    shift
    local cmd="$@"
    
    echo "🚀 $desc"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Use pv (pipe viewer) if available, otherwise simulate progress
    if command -v pv &> /dev/null; then
        # For commands that produce output
        eval "$cmd" | pv -l -s $(eval "$cmd 2>&1 | wc -l" 2>/dev/null || echo 100) > /dev/null 2>&1 || eval "$cmd"
    else
        # Simulate progress with spinner
        eval "$cmd" &
        local pid=$!
        local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
        local i=0
        
        while kill -0 $pid 2>/dev/null; do
            i=$(( (i+1) % 10 ))
            printf "\r%s Working..." "${spin:$i:1}"
            sleep 0.1
        done
        wait $pid
        local exit_code=$?
        
        if [ $exit_code -eq 0 ]; then
            printf "\r✅ Done!                        \n"
        else
            printf "\r❌ Failed (exit %d)              \n" $exit_code
        fi
        return $exit_code
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check for pv and install if needed
check_pv() {
    if ! command -v pv &> /dev/null; then
        echo "📦 Installing pv (progress viewer)..."
        if command -v brew &> /dev/null; then
            brew install pv
        elif command -v apt-get &> /dev/null; then
            sudo apt-get install -y pv
        else
            echo "⚠️  Please install 'pv' manually for progress bars"
        fi
    fi
}

# Export functions
export -f progress
check_pv
