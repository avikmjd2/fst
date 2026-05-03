import re
# Extract all suffix tokens (xxx_s patterns) and inflection tags (+XXX)
suffixes = set()
inflections = set()
prefixes = set()
with open('test_data.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '\t' not in line:
            continue
        surface, annot = line.split('\t', 1)
        for alt in annot.split(','):
            alt = alt.strip()
            for token in alt.split():
                if token.endswith('_s'):
                    suffixes.add(token)
                elif token.startswith('+'):
                    inflections.add(token)
                elif token.endswith('_p') or token.endswith('_P'):
                    prefixes.add(token)

print("=== SUFFIXES ===")
for s in sorted(suffixes):
    print(s)
print("\n=== INFLECTIONS ===")
for i in sorted(inflections):
    print(i)
print("\n=== PREFIXES ===")
for p in sorted(prefixes):
    print(p)
