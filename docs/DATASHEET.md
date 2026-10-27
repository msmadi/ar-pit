# Datasheet: Arabic News Tweets PI & STS Dataset (AR-PIT)

Structured after *Datasheets for Datasets* (Gebru et al., 2021). Sources: AL‑Smadi et al. (2017), *Information Processing and Management* 53(3), and the dataset chapter of the accompanying thesis.

## 1. Motivation

**Why was the dataset created?** In 2016 there was little or no public data for paraphrase identification (PI) or semantic textual similarity (STS) in Arabic short texts. News outlets on Twitter repeatedly post about the same events in different words, which makes them a natural source of paraphrase pairs and a realistic test bed for duplicate‑news detection and first‑story detection.

**Who created it?** Mohammad AL‑Smadi, Zain Jaradat, Mahmoud AL‑Ayyoub and Yaser Jararweh, Computer Science Department, Jordan University of Science and Technology.

## 2. Composition

**What are the instances?** Pairs of Arabic tweets, each pair annotated with an STS degree (0–5) from which a binary paraphrase label is derived.

**How many?** 2,493 pairs: 1,702 train, 791 test (≈70/30). 3,404 unique sentences in train and 1,582 in test.

**Language and register.** Modern Standard Arabic as written by professional news desks. Tweets contain hashtags (often multi‑word, joined with `_`), outlet tags such as `#العربية_عاجل`, the prefix `عاجل |` ("Breaking |"), digits attached to words, and occasional missing spaces around `#`.

**Topics.** Breaking news, predominantly politics, war and conflict in the Middle East (Syria, Yemen, Iraq, Egypt, Iran, the Gulf), with some sport and other news.

**Label distribution.** See the README. About 58% of pairs are scored 0 (different topics); roughly 31% are paraphrases. This is intentionally less positive‑heavy than MSRP, whose high positive rate has been noted to bias results (Das & Smith, 2009).

**Is there a recommended split?** Yes; use the provided temporal split. Train was collected over three months and test over the following month, so test events are largely unseen.

**Is any information missing?** Tweet IDs, timestamps, the source account of each tweet, and per‑annotator judgements are not included.

**Does the data contain sensitive content?** Yes. As conflict news, many tweets report killings, bombings and casualties, and name public figures, armed groups and locations. No private individuals' personal data was intentionally collected.

## 3. Collection process

- Crawled with the Twitter Streaming API from @AJABreaking (Al Jazeera) and @alarabiya_brk (Al Arabiya). Two outlets were chosen so that most events would be reported at least twice.
- About 8,000 tweets collected (about 4,000 per account).
- Retweets and URLs were removed; only the tweet body was kept.
- Candidate pairs were formed from tweets on the same event posted by different accounts, plus unrelated pairs; 2,493 pairs were selected for annotation.

## 4. Annotation

**Schema.** SemEval‑2015 Task 1 (PIT) for PI, and the 0–5 STS guidelines of Agirre et al. (2012) for similarity:

| Score | Guideline |
|---:|---|
| 5 | Completely equivalent |
| 4 | Mostly equivalent; unimportant details differ |
| 3 | Roughly equivalent; important information differs or is missing |
| 2 | Not equivalent but share some details |
| 1 | Not equivalent but same topic |
| 0 | Different topics |

**Worked examples from the guidelines** (English glosses):

| Score | Sentence 1 | Sentence 2 |
|---:|---|---|
| 5 | Rouhani: ready to sit with any country at any table to discuss peace in Syria | Iranian President Rouhani: Iran will sit at any table with any country to discuss peace in Syria |
| 4 | Jubeir: Obama assured the Custodian of the Two Holy Mosques that the agreement prevents Iran from developing a nuclear weapon | Jubeir: Obama affirmed the agreement with Iran will not allow it to possess a nuclear weapon |
| 3 | Egypt: one policeman killed, 25 wounded in blast targeting troop carrier in Beheira | Two Egyptian police killed, more than 20 wounded in bombing targeting a police bus in Beheira |
| 2 | Three soldiers killed in bombing of police station in Istanbul | 7 wounded in bomb attack on a security centre in Sultanbeyli, Istanbul |
| 1 | Hollande: responsibility for refugees and migrants falls on everyone | Austrian interior minister: Vienna will not use force to stop refugees arriving from Hungary |
| 0 | Russian Foreign Ministry: we never hid our supply of military equipment to the Assad regime | Jubeir: we inspect all flights and ships to Yemen to ensure no military support reaches the Houthis |

**Annotators.** Native Arabic speakers: graduate student(s) and two senior researchers. <!-- TODO: reconcile — the paper states three annotators (1 graduate student + 2 senior researchers); the thesis chapter states five (3 graduate students + 2 senior researchers). -->

**Procedure.** Iterative: graduate annotation → review by senior researchers → feedback → revision, over several cycles. Because labels were revised through adjudication, a conventional inter‑annotator agreement statistic could not be computed. The authors note that agreeing on a single Likert degree was difficult in borderline cases.

## 5. Preprocessing

The `Sent_*_tag` columns hold a normalized version of each tweet. Preprocessing described in the paper:

- removal of non‑Arabic words, hyperlinks, hashtag symbols, diacritics, punctuation and symbols (`? ' ! @ $ # —`);
- removal of the outlet source tag (e.g. `#العربية_عاجل`);
- letter normalization of alef variants (أ إ آ → ا) and further character normalizations described in §3.2.1 of the paper;
- tokenization with NLTK `wordpunct_tokenize`;
- stemming with AraNLP / the NLTK ISRI root stemmer (used for features, not stored).

Stop words were deliberately **not** removed, since they carry meaning relevant to paraphrase (Eyecioglu & Keller, 2015).

## 6. Labels and derived classes

| Score (= positive votes of 5) | Vote form | PI class |
|---|---|---|
| 3, 4, 5 | (3,2) (4,1) (5,0) | paraphrase |
| 2 | (2,3) | debatable |
| 0, 1 | (1,4) (0,5) | non‑paraphrase |

This mapping reproduces the published split statistics exactly (e.g. train: 13.2 + 9.7 + 7.9 = 30.8% ≈ 526 paraphrases; score 2 = 8.8% ≈ 149 debatable).


