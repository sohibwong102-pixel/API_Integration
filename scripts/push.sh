#!/bin/bash

MESSAGE=${1:-"update goblin 😎🔥"}

sleep 2

if gum spin --spinner monkey --title "😎 adding files..." -- git add -A; then
    echo "✅ add success"
    sleep 3
else
    echo "❌ add failed"
    exit 1
fi

if gum spin --spinner monkey --title "😎 committing..." -- git commit -m "$MESSAGE"; then
    echo "✅ commit success"
    sleep 3
else
    echo "❌ commit failed"
    exit 1
fi

if gum spin --spinner monkey --title "😎 pushing..." -- git push; then
    echo "✅ push success"
    sleep 3
else
    echo "❌ push failed"
    exit 1
fi

echo ""
echo "🔥 DONE GOBLIN 🔥"
