#!/bin/bash
# Clean up data files (with confirmation)

echo "========================================"
echo "Data Cleanup Utility"
echo "========================================"
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Count files
json_count=$(find data/json -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
fif_count=$(find data/fif -name "*.fif" 2>/dev/null | wc -l | tr -d ' ')
plot_count=$(find data/plots -name "*.png" -o -name "*.json" 2>/dev/null | wc -l | tr -d ' ')

echo "Current data files:"
echo "  JSON files:  $json_count"
echo "  FIF files:   $fif_count"
echo "  Plot files:  $plot_count"
echo ""

# Show file sizes
if [ -d "data" ]; then
    echo "Directory sizes:"
    du -sh data/json data/fif data/plots 2>/dev/null || true
    echo ""
fi

# Cleanup options
echo "Cleanup options:"
echo "  1) Delete all JSON files"
echo "  2) Delete all FIF files"
echo "  3) Delete all plots"
echo "  4) Delete ALL data files"
echo "  5) Keep everything (cancel)"
echo ""
read -p "Select option (1-5): " choice

case $choice in
    1)
        echo "🗑️  Deleting JSON files..."
        rm -f data/json/*.json
        echo "✓ JSON files deleted"
        ;;
    2)
        echo "🗑️  Deleting FIF files..."
        rm -f data/fif/*.fif
        echo "✓ FIF files deleted"
        ;;
    3)
        echo "🗑️  Deleting plots..."
        rm -f data/plots/*.png data/plots/*.pdf data/plots/*_statistics.json
        echo "✓ Plot files deleted"
        ;;
    4)
        read -p "⚠️  Delete ALL data files? This cannot be undone! (yes/N): " confirm
        if [ "$confirm" = "yes" ]; then
            echo "🗑️  Deleting all data files..."
            rm -rf data/json/* data/fif/* data/plots/*
            echo "✓ All data files deleted"
        else
            echo "Cancelled."
        fi
        ;;
    5)
        echo "Cancelled. No files deleted."
        ;;
    *)
        echo "Invalid option. Cancelled."
        ;;
esac

echo ""
echo "Done."

