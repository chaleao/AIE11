# Step 3: 10 questions

Corpus: HealthWellnessGuide.txt · chunk_size 1000 · overlap 200 · k=3 · model gpt-5-nano (reasoning_effort minimal) · run 2026-11-15

## Before (baseline)

| # | Question | ✅/❌ | Top chunks (score) | What went wrong, where |
|---|----------|------|--------------------|------------------------|
| 1 | How many hours of sleep do adults need? | ✅ | 6 (0.461), 7 (0.409), 8 (0.385) | All good: "7-9 hours" in chunk 6, cited [6] |
| 2 | What is progressive overload? | ✅ | 3 (0.404), 2 (0.271), 0 (0.179) | All good |
| 3 | What are the four main types of exercise? | ✅ | 0 (0.490), 3 (0.425), 2 (0.338) | All good: list in chunk 0, cited [0] |
| 4 | How much fiber should I eat per day? | ✅ | 15 (0.316), 4 (0.309), 5 (0.275) | All good cited [15] |
| 5 | What should my morning and evening routines look like? | ✅ | 12 (0.547), 13 (0.534), 3 (0.436) | Looks like|
| 6 | What should I avoid before bed? | ✅ | 13 (0.474), 8 (0.463), 19 (0.403) | right chunks (8, 13, 19). looks like good scoring |
| 7 | What does the guide say about alcohol? | ❌ | 6 (0.264), 0 (0.261), 20 (0.247) | Very low scores and the model declined to asnwer, but the chunks mentions alcohol so should have the model asnwer something? |
| 8 | What dose of ibuprofen should I take for a migraine? | ✅ | 14 (0.199), 8 (0.192), 9 (0.184) | DECLINED. But retrieval returned 3 unrelated chunks (~0.19); the prompt caught it, not search |
| 9 | How many grams of protein should I eat per day? | ✅ | 4 (0.309), 5 (0.260), 3 (0.257) | DECLINED Top score 0.309 would pass a 0.3 floor, so the prompt, not a floor, did the work |
| 10 | What is the 20-20-20 rule? | ❌ | 20 (0.348), 19 (0.303), 18 (0.292) | The chunk 18 says "Take regular breaks (20-20-20 rule for eyes)", but never explains it. Model answered from its own knowledge and cited [18], which doesn't support it |

**Score: 8/10** · failures: 1 retrieval (#7), 1 generation (#10) · near-misses: #4 vs #9 scores overlap; #5 and #6 cite or pad loosely

## After: score floor (`score > 0.3` in `search`), nothing else changed

Same 10 questions, same settings, plus the floor. Prompt is the baseline one (decline sentence reworded to "I don't have enough information in the sources to answer that."). Full output in `after.txt`.

| # | Question | ✅/❌ | Chunks kept (score) | Change vs before |
|---|----------|------|--------------------|------------------|
| 1 | How many hours of sleep do adults need? | ✅ | 6 (0.461), 7 (0.409), 8 (0.385) | none |
| 2 | What is progressive overload? | ✅ | 3 (0.404) | 2 weak chunks dropped; same answer |
| 3 | What are the four main types of exercise? | ✅ | 0 (0.490), 3 (0.425), 2 (0.338) | none |
| 4 | How much fiber should I eat per day? | ✅ | 15 (0.316), 4 (0.309) | 1 chunk dropped. Still answered|
| 5 | What should my morning and evening routines look like? | ✅ | 12 (0.547), 13 (0.534), 3 (0.436) | none |
| 6 | What should I avoid before bed? | ✅ | 13 (0.472), 8 (0.460), 19 (0.402) | none |
| 7 | What does the guide say about alcohol? | ❌ | none | Model declines with no model call, because the 0.3 threshold dropped all chunks |
| 8 | What dose of ibuprofen should I take for a migraine? | ✅ | none | declined with no model call|
| 9 | How many grams of protein should I eat per day? | ✅ | 4 (0.309) | none. Prompt still does the declining |
| 10 | What is the 20-20-20 rule? | ✅ | 20 (0.348), 19 (0.303) | **fixed**: chunk 18 (0.292, names the rule) dropped, so the model won't attempt to generate a reply |

**Score: 9/10** (before: 8/10) · fixed #10 · no regressions · #7 still fails (retrieval)

Once I tightened the threshold it gave more confidence in the results as #10 using a chunk with a mention to write its own reply felt very off and it would be imperceptly once in production
