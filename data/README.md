# data/

Place the dataset files here:

| File | Pairs | Contents |
|---|---:|---|
| `train.data` | 1,702 | 7 tab-separated fields, labels in field 5 |
| `test.data`  | 791 | 7 tab-separated fields |
| `test.label` | 791 | gold labels, one per line, same order as `test.data` |

Format and label mapping are documented in the top-level README.
After adding the files, check the counts:

```bash
python -c "from arpi import load_pairs; from collections import Counter; \
[print(f, len(d), Counter(p.pi_label for p in d)) for f in ('data/train.data','data/test.data') for d in [load_pairs(f)]]"
```

Expected for train: 526 paraphrase, 1,027 non-paraphrase, 149 debatable.
