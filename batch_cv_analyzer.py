import os
import json
from agents.cv_analyzer import analyze_cv

# Path to your CV folder
cv_folder = "data/resume_samples"

# Output file
output_file = "cv_analysis.json"

# Collect results
results = []

# Loop through all PDF resumes
for filename in os.listdir(cv_folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(cv_folder, filename)
        print(f"🔍 Analyzing: {filename}")
        try:
            analysis = analyze_cv(file_path)
            results.append({
                "file_name": filename,
                "analysis": analysis.content if hasattr(analysis, 'content') else str(analysis)
            })
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

# Save results to JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Analysis complete. Results saved to: {output_file}")
