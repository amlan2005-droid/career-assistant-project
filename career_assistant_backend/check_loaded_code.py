"""
Check if the updated resume_parser is being used
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services import resume_parser
import inspect

# Check the source code of extract_features
source = inspect.getsource(resume_parser.extract_features)

print("Current extract_features function:")
print("=" * 60)

# Check if it has the comprehensive skill patterns
if "SKILL_PATTERNS" in source or "50+" in source or "comprehensive" in source.lower():
    print("✅ NEW CODE IS LOADED - Has comprehensive skill extraction")
else:
    print("❌ OLD CODE IS LOADED - Still using basic regex")

# Show first few lines
lines = source.split('\n')[:15]
for line in lines:
    print(line)

# Check if SKILL_PATTERNS exists
if hasattr(resume_parser, 'SKILL_PATTERNS'):
    print("\n✅ SKILL_PATTERNS variable exists")
    print(f"Pattern length: {len(resume_parser.SKILL_PATTERNS)} characters")
else:
    print("\n❌ SKILL_PATTERNS variable NOT FOUND - old code is running")
