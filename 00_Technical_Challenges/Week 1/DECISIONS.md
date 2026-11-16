# Decisions

One row one decision. This week is the first one. By Week 5 this file will explain what decisions you made during this bootcamp.

## Retrieval, week 1

**What I changed**

* Changed model from the gpt-4.1-mini to gpt-5-nano with minimal effort. 
* Decided to use XML tags to augment the user question as well as added extra instructions in my system prompt around it
* Added a score threshold of 0.3 in `search`, so chunks below it are dropped before they reach the model.

**Why**

* It targeted question #10 ("What is the 20-20-20 rule?"). The guide only names the rule in chunk 18 and never explains it, but the model answered from its own knowledge and cited [18].
* With the threshold, chunk 18 (0.292) is dropped and the app declines. Score went from 8/10 to 9/10 with no regressions (before/after in QUESTIONS.md).
* I first tried a prompt rule instead. It still answered from its own knowledge 3 out of 3 times.

**What would change my mind**

* I would raise the score threshold if users start seeing confident answers based on poor chunks, as 0.3 and 0.5 are fairly loose thresholds meant for broader retrieval.

