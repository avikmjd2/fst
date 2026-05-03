"""Extract stems from test_data.txt and write stems.txt"""
import re, os

stems = {}
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, 'test_data.txt')) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '\t' not in line:
            continue
        _, annot = line.split('\t', 1)
        for alt in annot.split(','):
            for token in alt.strip().split():
                m = re.match(r'^([a-zA-Z_-]+)_(V|N|A|O|Q|P|B)$', token)
                if m:
                    w, p = m.group(1).lower(), m.group(2)
                    if w not in stems:
                        stems[w] = p

with open(os.path.join(script_dir, 'stems.txt'), 'w') as f:
    for s in sorted(stems):
        f.write(f'{s}\t{stems[s]}\n')
print(f'Wrote {len(stems)} stems')
