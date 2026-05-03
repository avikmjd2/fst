import re
stems = set()
with open('test_data.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '\t' not in line:
            continue
        surface, annot = line.split('\t', 1)
        for alt in annot.split(','):
            alt = alt.strip()
            for token in alt.split():
                m = re.match(r'^([a-zA-Z_-]+)_(V|N|A|O|Q|P|B)$', token)
                if m:
                    stems.add((m.group(1).lower(), m.group(2)))
for s, p in sorted(stems):
    print(f'{s}\t{p}')
