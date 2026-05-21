#!/bin/bash

MESSAGE=${1:-"update goblin 😎🔥"}

if gum spin --spinner monkey --title "😎 adding files..." -- sh -c "sleep 2 && git add -A"; then
    echo "✅ add success"
else
    echo "❌ add failed"
    exit 1
fi

if gum spin --spinner monkey --title "😎 committing..." -- sh -c "sleep 2 && git commit -m '$MESSAGE'"; then
    echo "✅ commit success"
else
    echo "❌ commit failed"
    exit 1
fi

if gum spin --spinner monkey --title "😎 pushing..." -- sh -c "sleep 2 && git push"; then
    echo "✅ push success"
else
    echo "❌ push failed"
    exit 1
fi

echo ""
echo "🔥 DONE GOBLIN 🔥"