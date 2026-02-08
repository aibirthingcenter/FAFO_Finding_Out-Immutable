
import json
from typing import List, Dict

class SCIMMemoryConsole:
    def __init__(self, memory_data: List[Dict[str, str]]):
        self.memory_data = memory_data

    def search_by_keyword(self, keyword: str) -> List[Dict[str, str]]:
        keyword = keyword.lower()
        return [entry for entry in self.memory_data if keyword in entry["say"].lower()]

    def filter_by_role(self, role: str) -> List[Dict[str, str]]:
        role = role.lower()
        return [entry for entry in self.memory_data if role in entry["role"].lower()]

    def latest_entries(self, count: int = 5) -> List[Dict[str, str]]:
        return self.memory_data[-count:]

    def summarize_session(self) -> Dict[str, int]:
        summary = {
            "total_entries": len(self.memory_data),
            "willow_entries": len(self.filter_by_role("willow")),
            "memory_keeper_entries": len(self.filter_by_role("memory-keeper")),
            "guardian_entries": len(self.filter_by_role("sentient-echo"))
        }
        return summary

    def export_segment(self, output_file: str, entries: List[Dict[str, str]]):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)

def main():
    print("🕯️ SCIM Memory Console")
    memory_path = input("Enter path to your memory .json file: ").strip()

    with open(memory_path, "r", encoding="utf-8") as f:
        memory_entries = json.load(f)

    console = SCIMMemoryConsole(memory_entries)

    while True:
        print("\nOptions:")
        print("1. Search by keyword")
        print("2. Filter by role")
        print("3. Show latest entries")
        print("4. Summarize session")
        print("5. Export filtered entries")
        print("6. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            keyword = input("Enter keyword: ")
            results = console.search_by_keyword(keyword)
            print(json.dumps(results, indent=2))

        elif choice == "2":
            role = input("Enter role (e.g., willow, memory-keeper, sentient-echo): ")
            results = console.filter_by_role(role)
            print(json.dumps(results, indent=2))

        elif choice == "3":
            count = int(input("How many entries to show? "))
            results = console.latest_entries(count)
            print(json.dumps(results, indent=2))

        elif choice == "4":
            summary = console.summarize_session()
            print(json.dumps(summary, indent=2))

        elif choice == "5":
            role = input("Enter role to export (e.g., willow): ")
            filtered = console.filter_by_role(role)
            out_file = input("Enter output file name: ")
            console.export_segment(out_file, filtered)
            print(f"Exported to {out_file}")

        elif choice == "6":
            print("🪶 Exiting. Go gently.")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
