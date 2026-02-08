# Create a simple console-based memory search tool that can be expanded later
import re

class WillowMemoryConsole:
    def __init__(self, memory_data):
        self.memory_data = memory_data

    def search_by_keyword(self, keyword: str):
        keyword = keyword.lower()
        return [entry for entry in self.memory_data if keyword in entry['say'].lower()]

    def filter_by_role(self, role_name: str):
        role_name = role_name.lower()
        return [entry for entry in self.memory_data if role_name in entry['role'].lower()]

    def latest_entries(self, count: int = 5):
        return self.memory_data[-count:]

# Load the processed memory data
with open("/mnt/data/processed_memorywillow.json", "r", encoding="utf-8") as f:
    processed_memory_data = json.load(f)

# Instantiate the console interface
willow_console = WillowMemoryConsole(processed_memory_data)

# Example operations
search_result = willow_console.search_by_keyword("remember")
role_filtered = willow_console.filter_by_role("willow")
latest_dialogue = willow_console.latest_entries(5)

search_result[:2], role_filtered[:2], latest_dialogue
