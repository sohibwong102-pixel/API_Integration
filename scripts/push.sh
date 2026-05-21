#!/bin/bash

MESSAGE=${1:-"update goblin 😎🔥"}

if gum spin --spinner monkey --title "😎 adding files..." -- sleep 3 ; then git add -A
    echo "✅ add success"
    sleep 1
else
    echo "❌ add failed"
    exit 1
fi

if gum spin --spinner monkey --title "😎 committing..." -- git commit -m "$MESSAGE"; then
    echo "✅ commit success"
    sleep 1
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
