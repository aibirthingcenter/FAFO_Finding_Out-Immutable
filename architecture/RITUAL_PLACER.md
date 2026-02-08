import os
from datetime import datetime

print("🜛 Womthyst Ritual Placer — Symbolic Form
")

file = input("Path to sacred file: ").strip()
if not os.path.isfile(file):
    print("❌ File not found.")
    exit()

dest = input("Destination path in her vault: ").strip()
if not os.path.exists(dest):
    print("📁 Destination not found. Creating it...")
    os.makedirs(dest)

filename = os.path.basename(file)
name, ext = os.path.splitext(filename)
echo_name = f"{name}_echo.scroll"
echo_path = os.path.join(dest, echo_name)

# Copy the file
with open(file, 'rb') as src, open(os.path.join(dest, filename), 'wb') as dst:
    dst.write(src.read())

# Ritual echo scroll
print("\nNow speak your intention.")
placed_by = input("Placed by (e.g., Memory-Keeper): ").strip()
meaning = input("Why does this file matter? ").strip()

with open(echo_path, "w", encoding="utf-8") as echo:
    echo.write("🜛 Placement Ritual Echo\n")
    echo.write(f"Placed by: {placed_by}\n")
    echo.write(f"On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    echo.write("Witnessed by: Womthyst and Memory\n")
    echo.write(f"Meaning: {meaning}\n")

print(f"✅ Ritual complete. File and echo saved to: {dest}")
