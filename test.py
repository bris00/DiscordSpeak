from datasets import load_dataset
from collections import defaultdict

ds = load_dataset("codeparrot/github-code", streaming=True, split="train")

syms = defaultdict(lambda: 0)

for n, file in enumerate(ds):
    for c in file['code']:
        if not c.isalpha() and ord(c) < 128 and not c.isspace() and c.isprintable():
            syms[c] += 1

    if n % 10000:
    #if True:
        view = [(v, k) for k, v in syms.items()]
        
        print("\n".join([f"{i+1}: {k}" for i, (v, k) in enumerate(sorted(view, reverse=True)[:100])]))