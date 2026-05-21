#!/bin/bash

MESSAGE=${1:-"commit goblin 😎🔥"}

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='⠋⠙⠸⠴⠦⠇'

    while ps a | awk '{print $1}' | grep -q "$pid"; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\r"
    done

    printf "    \r"
}

run_task() {
    local message=$1
    shift

    printf "😎 %s..." "$message"

    "$@" > /dev/null 2>&1 &
    local pid=$!

    spinner $pid
    wait $pid

    if [ $? -eq 0 ]; then
        echo " ✅"
    else
        echo " ❌"
        exit 1
    fi
}

run_task "Adding files..." git add -A
run_task "Committing..." git commit -m "$MESSAGE"
run_task "Pushiig..." git push

echo ""
echo "🔥 DONE GOBLIN 🔥"
