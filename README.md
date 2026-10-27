# Arabic News Tweets Paraphrase & Semantic Similarity Dataset (AR-PIT)

A manually annotated corpus of **2,493 pairs of Modern Standard Arabic breaking‑news tweets** for two sentence‑pair tasks:

| Task | Question | Output |
|---|---|---|
| **T1 – Paraphrase Identification (PI)** | Do the two tweets express the same meaning, regardless of surface form? | binary (paraphrase / non‑paraphrase) |
| **T2 – Semantic Textual Similarity (STS)** | How similar in meaning are the two tweets? | graded score, 0 – 5 |

The dataset was built for, and is described in:

> Mohammad AL‑Smadi, Zain Jaradat, Mahmoud AL‑Ayyoub, Yaser Jararweh. **Paraphrase identification and semantic text similarity analysis in Arabic news tweets using lexical, syntactic, and semantic features.** *Information Processing and Management*, 53(3), 640–652, 2017. https://doi.org/10.1016/j.ipm.2017.01.002

The annotation schema and file format follow **SemEval‑2015 Task 1: Paraphrase and Semantic Similarity in Twitter (PIT)** (Xu, Callison‑Burch & Dolan, 2015), so tools written for the English PIT‑2015 data work here with little or no change.

---

## Contents

```
.
├── data/
│   ├── train.data        # 1,702 annotated pairs (tab‑separated, 7 fields)
│   ├── test.data         # 791 pairs (tab‑separated, 7 fields)
│   └── test.label        # gold labels for the test set (evaluation only)
├── arpi/                 # small Python package: loading, label mapping, evaluation
├── baselines/            # random and logistic‑regression baselines (Arabic‑adapted)
├── docs/DATASHEET.md     # full datasheet: collection, annotation, known issues
├── tests/                # smoke tests on a tiny fixture
├── CITATION.cff
└── requirements.txt
```

---

## Data at a glance

Tweets were crawled with the Twitter Streaming API from the breaking‑news accounts of **Al Jazeera** ([@AJABreaking](https://twitter.com/AJABreaking)) and **Al Arabiya** ([@alarabiya_brk](https://twitter.com/alarabiya_brk)). Pairing tweets from two outlets covering the same events yields many natural paraphrases. Roughly 8,000 tweets were collected (about 4,000 per account); 2,493 pairs were selected and annotated.

The **train** split was collected over three months and the **test** split during the following month, so the test set contains events not seen in training (a temporal split). Content is mostly political and conflict news from the Middle East, with some sport and other topics.

| Split | Unique sentences | Pairs | Paraphrase | Non‑paraphrase | Debatable |
|---|---:|---:|---:|---:|---:|
| Train | 3,404 | 1,702 | 526 (30.9%) | 1,027 (60.3%) | 149 (8.7%) |
| Test  | 1,582 |   791 | 253 (31.9%) |   465 (58.8%) |  73 (9.2%) |
| **Total** | 4,986 | **2,493** | 779 | 1,492 | 222 |

The paper's Table 1 reports non‑paraphrase as 1,176 / 538; those figures fold the debatable pairs into the negative class (1,027 + 149, 465 + 73).

### STS score distribution

| Split | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| Train | 58.8% | 1.6% | 8.8% | 13.2% | 9.7% | 7.9% |
| Test  | 58.0% | 0.9% | 9.2% | 11.6% | 12.1% | 8.2% |
| Overall | 58.4% | 1.25% | 9.0% | 12.4% | 10.9% | 8.05% |

---

## Annotation

Each pair received a binary paraphrase judgement and a 0–5 similarity degree using the guidelines of Agirre et al. (2012):

| Score | Meaning |
|---:|---|
| 5 | Completely equivalent — they mean the same thing |
| 4 | Mostly equivalent, but some unimportant details differ |
| 3 | Roughly equivalent, but some important information differs or is missing |
| 2 | Not equivalent, but share some details |
| 1 | Not equivalent, but on the same topic |
| 0 | On different topics |

Annotators were native Arabic speakers (graduate students and senior researchers). Annotation proceeded in cycles of annotation → review by the senior researchers → feedback, which is why a single inter‑annotator agreement figure is not reported. See [`docs/DATASHEET.md`](docs/DATASHEET.md) for details.

### Examples

| Label | Sentence 1 | Sentence 2 |
|---|---|---|
| paraphrase | الملك_سلمان: نعتزم التعاون مع أميركا لتحقيق الاستقرار في الشرق الأوسط<br>*King Salman: We intend to cooperate with the US to achieve stability in the Middle East* | العاهل السعودي: #السعودية تعتزم التعاون مع #أميركا لتحقيق الاستقرار في الشرق الأوسط<br>*Saudi monarch: #SaudiArabia intends to cooperate with #America to achieve stability in the Middle East* |
| non‑paraphrase | القاعدة في اليمن تعترف بمقتل قائدها #ناصر_الوحيشي<br>*Al‑Qaeda in Yemen acknowledges the killing of its leader #Nasser_al‑Wuhayshi* | تعيين #قاسم_الريمي قائدا للتنظيم خلفا للوحيشي<br>*#Qasim_al‑Raymi appointed leader of the organization, succeeding al‑Wuhayshi* |
| debatable | أنباء عن مقتل القيادي الدرزي الشيخ وحيد البلعوس بسيارة مفخخة في السويداء<br>*Reports that Druze leader Sheikh Wahid al‑Balous was killed by a car bomb in Suwayda* | انفجار سيارة ملغمة في محافظة#السويداء وأنباء عن ضحايا<br>*Car bomb explodes in #Suwayda province, reports of casualties* |

---

## File format

Both `train.data` and `test.data` are UTF‑8, tab‑separated, one pair per line, **no header**, with the seven SemEval‑2015 PIT fields:

| # | Field | Description |
|---|---|---|
| 1 | `Topic_ID` | Identifier of the pair |
| 2 | `Topic_Name` | Topic label (`Breaking news` throughout) |
| 3 | `Sent_1` | First tweet (raw text, retweet markers and URLs removed) |
| 4 | `Sent_2` | Second tweet |
| 5 | `Label` | Annotation (see below) |
| 6 | `Sent_1_tag` | Preprocessed / normalized version of `Sent_1` |
| 7 | `Sent_2_tag` | Preprocessed / normalized version of `Sent_2` |

### Labels and the PI mapping

The `Label` field takes one of two forms, as in SemEval‑2015 PIT:

- **Vote form** `(a, b)` — `a` of five judgements positive, `b` negative.
- **Score form** — a single integer `0`–`5`.

The two forms align: the number of positive votes `a` equals the 0–5 score. Binary PI labels are derived as follows:

| Score / votes | PI class |
|---|---|
| 3, 4, 5 &nbsp;·&nbsp; `(3,2)`, `(4,1)`, `(5,0)` | **paraphrase** |
| 2 &nbsp;·&nbsp; `(2,3)` | **debatable** |
| 0, 1 &nbsp;·&nbsp; `(1,4)`, `(0,5)` | **non‑paraphrase** |

This mapping reproduces the split statistics above exactly. Following SemEval‑2015 practice, debatable pairs are **excluded** when training a binary classifier and when scoring T1:PI, but **kept** for T2:STS.

---

## Quick start

```bash
git clone https://github.com/<user>/<repo>.git
cd <repo>
pip install -r requirements.txt
```

```python
from arpi import load_pairs

train = load_pairs("data/train.data")
print(len(train))                 # 1702
p = train[0]
print(p.sent_1, "|", p.sent_2)
print(p.score, p.pi_label)        # e.g. 4 'paraphrase'
```

Run the baselines and score them:

```bash
python -m baselines.random_baseline data/test.data > out/random.output
python -m baselines.lr_baseline     data/train.data data/test.data > out/lr.output
python -m arpi.evaluate data/test.label out/lr.output
```

System output follows the PIT‑2015 convention: one line per test pair, in order, `true|false<TAB>score`, where `score` ∈ [0, 1].

---

## Evaluation

| Task | Primary metric | Secondary |
|---|---|---|
| T1:PI | F1 on the paraphrase class (debatable excluded) | Precision, Recall |
| T2:STS | Pearson *r* between system score and gold score | maxF1 (with its precision/recall) over the precision‑recall curve |

`arpi/evaluate.py` implements all of these.

### Reference results (test set)

From AL‑Smadi et al. (2017), Table 4:

| System | PI F1 | PI P | PI R | STS Pearson | maxF1 | maxP | maxR |
|---|---:|---:|---:|---:|---:|---:|---:|
| Random baseline | 0.333 | 0.246 | 0.512 | 0.055 | 0.385 | 0.241 | 0.963 |
| Logistic regression, n‑gram overlap (Das & Smith 2009, Arabic‑adapted) | 0.812 | 0.805 | 0.818 | 0.825 | 0.825 | 0.795 | 0.858 |
| SVR + lexical, syntactic, semantic, alignment & topic features | **0.872** | 0.844 | 0.901 | **0.912** | 0.877 | 0.843 | 0.913 |

The logistic‑regression baseline is labelled "MaxEnt" in the paper. Baselines in this repository are re‑implementations; small differences from the published numbers are expected.

---

## Citation

If you use this dataset, please cite:

```bibtex
@article{alsmadi2017paraphrase,
  title   = {Paraphrase identification and semantic text similarity analysis in {Arabic} news tweets using lexical, syntactic, and semantic features},
  author  = {AL-Smadi, Mohammad and Jaradat, Zain and AL-Ayyoub, Mahmoud and Jararweh, Yaser},
  journal = {Information Processing \& Management},
  volume  = {53},
  number  = {3},
  pages   = {640--652},
  year    = {2017},
  publisher = {Elsevier},
  doi     = {10.1016/j.ipm.2017.01.002}
}
```

Please also cite the schema the dataset follows:

```bibtex
@inproceedings{xu2015semeval,
  title     = {{SemEval}-2015 Task 1: Paraphrase and Semantic Similarity in {Twitter} ({PIT})},
  author    = {Xu, Wei and Callison-Burch, Chris and Dolan, Bill},
  booktitle = {Proceedings of the 9th International Workshop on Semantic Evaluation (SemEval 2015)},
  pages     = {1--11},
  year      = {2015}
}
```

---

## License

- **Annotations:** <!-- TODO: choose, e.g. CC BY 4.0 or CC BY-NC-SA 4.0 -->
- **Code** (`arpi/`, `baselines/`, `tests/`): MIT — see [`LICENSE`](LICENSE).

Tweet text remains the property of its original publishers and is subject to the X (Twitter) developer terms. The data is provided for non‑commercial research.

## Contact

Mohammad AL‑Smadi — <!-- TODO: preferred contact email -->

Work carried out at the Computer Science Department, Jordan University of Science and Technology.
