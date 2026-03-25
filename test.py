from claude_service import ClaudeService

with open("test-bread.jpeg", "rb") as photo:
    claude = ClaudeService()
    result = claude.analyze_bread(photo, "This is my bread")
    print(result)