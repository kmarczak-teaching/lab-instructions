import os

name = os.getenv("MY_NAME", "Unknown User")
print(f"Hello, {name}! This message was generated in GitHub Actions.")
