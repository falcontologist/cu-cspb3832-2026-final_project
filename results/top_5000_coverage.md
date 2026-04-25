# Top-5,000 Frequent English Verb Coverage

How well does the v2.0 lexicon ([data/situation_shapes_workbook.csv](../data/situation_shapes_workbook.csv)) cover the top 5,000 most-frequent English verbs?

## Method

The verb pool is built with a hybrid POS filter so the ranking is not capped by any single corpus. A lemma enters the pool if any one of these sources confirms it as a verb:

1. **VerbNet 3.4 membership.** Authoritative — VerbNet only lists verbs.
2. **WordNet primary-POS rule.** verb synsets are at least 30% of all synsets for the lemma. Catches verbs like `do`, `keep`, `help`, `become` that Brown's strict threshold drops; rejects `up`, `still`, `right` whose verb senses are minor.
3. **Brown corpus** verb-tagged hits >= 3 (loosened from the previous threshold of 10).

Lemmas are ranked by `wordfreq` Zipf frequency (a meta-corpus combining Wikipedia, OpenSubtitles, Twitter, news, books). NFKC normalization is applied throughout.

**Workbook size:** 4,189 unique verbs.

**Verb pool built (raw):** 6,057 lemmas
**Top-5,000 pool used for coverage:** 5,000 lemmas

## Coverage at cutoffs

| Top-N most frequent | Covered by workbook | Coverage |
|---:|---:|---:|
| 50 | 39 | 78.0% |
| 100 | 83 | 83.0% |
| 250 | 207 | 82.8% |
| 500 | 398 | 79.6% |
| 1,000 | 782 | 78.2% |
| 2,500 | 1,803 | 72.1% |
| 5,000 | 3,214 | 64.3% |

## Gap to 80% coverage at top-5,000

- **Current coverage:** 3,214 / 5,000 = **64.3%**
- **Target (80%):** 4,000 / 5,000
- **Verbs to add:** 786 (15.7% of the pool)

Adding the **786 highest-frequency missing verbs** below would lift coverage to the 80% threshold. They are sorted by frequency-rank in the pool (most frequent first).

## Prioritized verbs to add (top of the gap)

| Pool rank | Verb | Zipf freq | Evidence |
|---:|---|---:|---|
| 4 | do | 6.35 | verbnet+brown+wn-primary |
| 7 | people | 6.25 | brown+wn-primary |
| 15 | well | 6.03 | brown |
| 21 | still | 5.92 | verbnet |
| 26 | man | 5.82 | brown |
| 35 | help | 5.75 | verbnet+brown+wn-primary |
| 40 | school | 5.71 | brown+wn-primary |
| 41 | end | 5.68 | verbnet+brown |
| 44 | team | 5.67 | verbnet+brown+wn-primary |
| 45 | keep | 5.66 | verbnet+brown+wn-primary |
| 48 | free | 5.63 | verbnet+brown+wn-primary |
| 68 | include | 5.21 | verbnet+brown+wn-primary |
| 69 | power | 5.52 | brown |
| 80 | service | 5.49 | brown |
| 95 | guy | 5.40 | wn-primary |
| 99 | single | 5.41 | brown |
| 100 | become | 5.40 | verbnet+brown+wn-primary |
| 101 | control | 5.40 | verbnet+brown+wn-primary |
| 103 | fuck | 5.39 | brown+wn-primary |
| 108 | matter | 5.38 | verbnet+brown |
| 136 | further | 5.31 | verbnet+brown |
| 141 | gonna | 5.29 | brown |
| 142 | market | 5.29 | brown+wn-primary |
| 143 | near | 5.29 | brown |
| 146 | front | 5.28 | brown |
| 147 | kid | 4.99 | brown |
| 148 | list | 5.28 | brown+wn-primary |
| 154 | program | 5.27 | brown |
| 159 | process | 5.26 | brown+wn-primary |
| 161 | word | 5.26 | brown |
| 162 | action | 5.25 | verbnet |
| 167 | field | 5.24 | brown |
| 170 | seem | 5.08 | verbnet+brown+wn-primary |
| 178 | space | 5.23 | brown |
| 179 | summer | 5.23 | verbnet+wn-primary |
| 186 | sex | 5.22 | wn-primary |
| 188 | account | 5.21 | brown |
| 190 | parent | 4.57 | wn-primary |
| 200 | share | 5.20 | brown+wn-primary |
| 201 | center | 5.19 | verbnet+brown |
| 231 | evidence | 5.14 | verbnet+brown+wn-primary |
| 242 | felt | 5.13 | brown+wn-primary |
| 247 | size | 5.13 | brown+wn-primary |
| 251 | key | 5.12 | brown |
| 255 | trade | 5.12 | verbnet+brown+wn-primary |
| 263 | complete | 5.10 | verbnet+brown+wn-primary |
| 268 | title | 5.10 | brown |
| 274 | release | 5.09 | verbnet+brown+wn-primary |
| 280 | increase | 5.08 | verbnet+brown |
| 287 | begin | 4.84 | verbnet+brown+wn-primary |
| 288 | career | 5.07 | wn-primary |
| 289 | december | 5.07 | verbnet |
| 290 | figure | 5.07 | verbnet+brown |
| 294 | forget | 5.06 | brown+wn-primary |
| 296 | okay | 5.06 | verbnet |
| 303 | risk | 5.05 | verbnet+brown+wn-primary |
| 307 | district | 5.04 | wn-primary |
| 309 | minister | 5.04 | brown+wn-primary |
| 312 | wall | 5.04 | brown |
| 313 | wanna | 5.04 | brown |
| 315 | culture | 5.03 | brown |
| 316 | fan | 4.92 | brown+wn-primary |
| 323 | effect | 5.02 | brown |
| 324 | except | 5.02 | wn-primary |
| 325 | limit | 4.70 | verbnet+brown+wn-primary |
| 340 | campaign | 5.00 | brown+wn-primary |
| 345 | focus | 5.00 | verbnet+brown+wn-primary |
| 346 | husband | 5.00 | wn-primary |
| 349 | message | 5.00 | wn-primary |
| 354 | contact | 4.99 | brown |
| 366 | subject | 4.96 | brown |
| 373 | gotta | 4.95 | brown |
| 376 | bar | 4.94 | verbnet+brown |
| 380 | feature | 4.82 | brown |
| 381 | finish | 4.91 | verbnet+brown+wn-primary |
| 385 | sport | 4.73 | brown |
| 388 | master | 4.93 | brown |
| 391 | trump | 4.93 | wn-primary |
| 392 | weekend | 4.93 | verbnet+wn-primary |
| 397 | compare | 4.45 | verbnet+brown+wn-primary |
| 399 | impact | 4.92 | wn-primary |
| 400 | lack | 4.92 | brown+wn-primary |
| 424 | associate | 4.39 | verbnet+brown+wn-primary |
| 431 | winter | 4.89 | verbnet+brown+wn-primary |
| 434 | challenge | 4.88 | brown+wn-primary |
| 437 | rat | 4.17 | brown+wn-primary |
| 439 | avoid | 4.87 | verbnet+brown+wn-primary |
| 445 | weather | 4.87 | wn-primary |
| 446 | google | 4.86 | wn-primary |
| 449 | locate | 3.94 | brown+wn-primary |
| 453 | attempt | 4.85 | verbnet+brown+wn-primary |
| 455 | exchange | 4.85 | verbnet+brown+wn-primary |
| 456 | fell | 4.85 | brown+wn-primary |
| 462 | traffic | 4.85 | wn-primary |
| 464 | benefit | 4.82 | verbnet+brown+wn-primary |
| 470 | structure | 4.84 | brown |
| 477 | mouth | 4.83 | brown |
| 484 | surface | 4.83 | wn-primary |
| 487 | wed | 3.66 | verbnet+brown+wn-primary |
| 489 | budget | 4.82 | brown+wn-primary |
| 491 | fail | 4.61 | verbnet+brown+wn-primary |
| 493 | fund | 4.82 | wn-primary |
| 508 | chairman | 4.80 | wn-primary |
| 509 | engineer | 4.50 | brown+wn-primary |
| 511 | institute | 4.80 | verbnet+brown+wn-primary |
| 522 | prevent | 4.79 | verbnet+brown+wn-primary |
| 524 | spirit | 4.79 | brown |
| 534 | garden | 4.77 | brown |
| 536 | labor | 4.77 | verbnet+brown+wn-primary |
| 543 | map | 4.76 | brown+wn-primary |
| 548 | aid | 4.75 | verbnet+brown+wn-primary |
| 555 | frank | 4.75 | wn-primary |
| 557 | operate | 4.50 | verbnet+brown+wn-primary |
| 570 | wine | 4.74 | wn-primary |
| 572 | blog | 4.73 | wn-primary |
| 576 | reduce | 4.73 | verbnet+brown+wn-primary |
| 583 | introduce | 4.37 | verbnet+brown+wn-primary |
| 587 | plane | 4.72 | wn-primary |
| 590 | sky | 4.72 | wn-primary |
| 593 | zone | 4.72 | brown+wn-primary |
| 596 | joint | 4.71 | wn-primary |
| 602 | steel | 4.71 | wn-primary |
| 615 | profit | 4.70 | verbnet+brown+wn-primary |
| 616 | proof | 4.70 | wn-primary |
| 618 | suit | 4.70 | brown+wn-primary |
| 622 | ray | 4.69 | wn-primary |
| 629 | download | 4.68 | wn-primary |
| 630 | email | 4.68 | wn-primary |
| 643 | factor | 4.67 | wn-primary |
| 644 | fee | 4.51 | brown+wn-primary |
| 649 | mistake | 4.67 | brown+wn-primary |
| 652 | route | 4.67 | wn-primary |
| 653 | schedule | 4.67 | brown+wn-primary |
| 659 | holiday | 4.66 | verbnet+wn-primary |
| 667 | sub | 4.66 | wn-primary |
| 671 | equal | 4.65 | brown+wn-primary |
| 672 | fake | 4.65 | verbnet+brown+wn-primary |
| 673 | finance | 4.65 | brown+wn-primary |
| 674 | identity | 4.65 | verbnet |
| 680 | task | 4.65 | wn-primary |
| 683 | arrest | 4.55 | verbnet+brown+wn-primary |
| 684 | conflict | 4.64 | brown |
| 693 | phase | 4.64 | wn-primary |
| 707 | shirt | 4.63 | wn-primary |
| 741 | deserve | 4.59 | brown+wn-primary |
| 743 | instance | 4.59 | wn-primary |
| 744 | motion | 4.59 | brown |
| 754 | dedicate | 3.51 | verbnet+brown+wn-primary |
| 756 | flag | 4.58 | brown+wn-primary |
| 765 | sentence | 4.58 | brown |
| 767 | achieve | 4.57 | verbnet+brown+wn-primary |
| 768 | afford | 4.57 | brown+wn-primary |
| 771 | bunch | 4.57 | brown+wn-primary |
| 773 | cheese | 4.57 | wn-primary |
| 774 | diet | 4.57 | wn-primary |
| 775 | fruit | 4.57 | wn-primary |
| 776 | index | 4.57 | brown+wn-primary |
| 777 | mess | 4.57 | brown |
| 780 | scheme | 4.57 | verbnet+brown |
| 782 | tank | 4.57 | wn-primary |
| 783 | tend | 4.57 | verbnet+brown+wn-primary |
| 789 | depend | 4.20 | verbnet+brown+wn-primary |
| 791 | golf | 4.56 | wn-primary |
| 795 | pattern | 4.56 | brown |
| 796 | premier | 4.56 | wn-primary |
| 797 | promote | 4.56 | verbnet+brown+wn-primary |
| 799 | ban | 4.55 | verbnet+brown+wn-primary |
| 801 | concert | 4.55 | wn-primary |
| 806 | joy | 4.55 | wn-primary |
| 807 | mate | 4.55 | verbnet+brown |
| 810 | retail | 4.55 | brown+wn-primary |
| 818 | quit | 4.54 | verbnet+brown+wn-primary |
| 824 | contest | 4.53 | brown+wn-primary |
| 833 | attach | 3.75 | verbnet+brown+wn-primary |
| 834 | blind | 4.52 | brown+wn-primary |
| 836 | debut | 4.52 | brown+wn-primary |
| 839 | license | 4.52 | verbnet+brown |
| 849 | defeat | 4.51 | brown+wn-primary |
| 850 | entitle | 2.71 | brown+wn-primary |
| 854 | injure | 3.27 | brown+wn-primary |
| 857 | oppose | 3.94 | verbnet+brown+wn-primary |
| 864 | egg | 4.46 | wn-primary |
| 865 | finger | 4.48 | brown+wn-primary |
| 867 | graduate | 4.50 | brown+wn-primary |
| 877 | colour | 4.49 | wn-primary |
| 881 | pride | 4.49 | brown |
| 886 | ignore | 4.48 | verbnet+brown+wn-primary |
| 889 | rape | 4.48 | brown+wn-primary |
| 897 | complicate | 3.26 | brown+wn-primary |
| 901 | format | 4.47 | verbnet+wn-primary |
| 902 | gap | 4.47 | brown |
| 903 | gate | 4.47 | wn-primary |
| 905 | mirror | 4.47 | brown+wn-primary |
| 909 | accuse | 3.71 | verbnet+brown+wn-primary |
| 910 | adventure | 4.46 | wn-primary |
| 914 | contrast | 4.46 | verbnet+brown |
| 915 | founder | 4.46 | wn-primary |
| 916 | gear | 4.46 | verbnet+brown |
| 918 | package | 4.46 | verbnet+brown |
| 925 | fort | 4.45 | brown+wn-primary |

_(Showing top 200 of 786 verbs to add. Full list in `data/top_5000_verbs.csv` — filter `in_workbook=no` and take the top 786 by rank.)_

## Top 50 missing verbs (highest frequency, absent from workbook)

These are the highest-frequency verbs in the top-5,000 pool that are not in the workbook. They are the most-leveraged additions per row, even if you decide to stop short of the 80% target.

| Pool rank | Verb | Zipf freq | Evidence |
|---:|---|---:|---|
| 4 | do | 6.35 | verbnet+brown+wn-primary |
| 7 | people | 6.25 | brown+wn-primary |
| 15 | well | 6.03 | brown |
| 21 | still | 5.92 | verbnet |
| 26 | man | 5.82 | brown |
| 35 | help | 5.75 | verbnet+brown+wn-primary |
| 40 | school | 5.71 | brown+wn-primary |
| 41 | end | 5.68 | verbnet+brown |
| 44 | team | 5.67 | verbnet+brown+wn-primary |
| 45 | keep | 5.66 | verbnet+brown+wn-primary |
| 48 | free | 5.63 | verbnet+brown+wn-primary |
| 68 | include | 5.21 | verbnet+brown+wn-primary |
| 69 | power | 5.52 | brown |
| 80 | service | 5.49 | brown |
| 95 | guy | 5.40 | wn-primary |
| 99 | single | 5.41 | brown |
| 100 | become | 5.40 | verbnet+brown+wn-primary |
| 101 | control | 5.40 | verbnet+brown+wn-primary |
| 103 | fuck | 5.39 | brown+wn-primary |
| 108 | matter | 5.38 | verbnet+brown |
| 136 | further | 5.31 | verbnet+brown |
| 141 | gonna | 5.29 | brown |
| 142 | market | 5.29 | brown+wn-primary |
| 143 | near | 5.29 | brown |
| 146 | front | 5.28 | brown |
| 147 | kid | 4.99 | brown |
| 148 | list | 5.28 | brown+wn-primary |
| 154 | program | 5.27 | brown |
| 159 | process | 5.26 | brown+wn-primary |
| 161 | word | 5.26 | brown |
| 162 | action | 5.25 | verbnet |
| 167 | field | 5.24 | brown |
| 170 | seem | 5.08 | verbnet+brown+wn-primary |
| 178 | space | 5.23 | brown |
| 179 | summer | 5.23 | verbnet+wn-primary |
| 186 | sex | 5.22 | wn-primary |
| 188 | account | 5.21 | brown |
| 190 | parent | 4.57 | wn-primary |
| 200 | share | 5.20 | brown+wn-primary |
| 201 | center | 5.19 | verbnet+brown |
| 231 | evidence | 5.14 | verbnet+brown+wn-primary |
| 242 | felt | 5.13 | brown+wn-primary |
| 247 | size | 5.13 | brown+wn-primary |
| 251 | key | 5.12 | brown |
| 255 | trade | 5.12 | verbnet+brown+wn-primary |
| 263 | complete | 5.10 | verbnet+brown+wn-primary |
| 268 | title | 5.10 | brown |
| 274 | release | 5.09 | verbnet+brown+wn-primary |
| 280 | increase | 5.08 | verbnet+brown |
| 287 | begin | 4.84 | verbnet+brown+wn-primary |
