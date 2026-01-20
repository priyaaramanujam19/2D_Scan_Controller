#!/bin/bash

echo "Starting scan automation..."

# 1. Activate Python virtual environment (adjust path if needed)
if [ -f "myvenv/bin/activate" ]; then
    source myvenv/bin/activate
else
    echo "Virtual environment not found, using system Python"
fi

# 2. Run the scan controller
echo "Running scan_controller.py..."
python3 scan_controller.py

sleep 30  # Optional, depends on your scan duration

# 3. Check if scan.log exists
LOG_FILE="output/scan.log"
if [ ! -f "$LOG_FILE" ]; then
  echo "ERROR: $LOG_FILE not found!"
  exit 1
fi

# Ensure directories exist
mkdir -p archived_logs
mkdir -p automation_reports

# 4. Rename log with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
NEW_LOG="archived_logs/scan_${TIMESTAMP}.log"
mv "$LOG_FILE" "$NEW_LOG"
echo "Log renamed to $NEW_LOG"

# 5. Analyze log
ERROR_COUNT=$(grep -c "ERROR" "$NEW_LOG")
WARNING_COUNT=$(grep -c "WARNING" "$NEW_LOG")

# 6. Generate summary report
REPORT="automation_reports/scan_report_${TIMESTAMP}.txt"

{
echo "Scan Test Report"
echo "----------------"
echo "Log file: $NEW_LOG"
echo "Errors: $ERROR_COUNT"
echo "Warnings: $WARNING_COUNT"
echo "Generated on: $(date)"
} > "$REPORT"

echo "Report generated: $REPORT"

# 7. Final status
if [ "$ERROR_COUNT" -gt 0 ]; then
  echo "Scan completed with ERRORS"
else
  echo "Scan completed successfully"
fi
