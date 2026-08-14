# RAG Evaluation Results

## 1. Evaluation Dataset

The RAG system was evaluated using 10 questions based on the
Internship Rule Book.

- Answerable questions: 9
- Unanswerable questions: 1

The evaluation included factual, multi-part, detailed,
and unanswerable questions.

---

## 2. Retrieval Evaluation

The baseline retrieval configuration used:

- Chunk size: [VALUE]
- Chunk overlap: [VALUE]
- Retrieval k: 4

Baseline retrieval hit rate:

[VALUE]%

---

## 3. Retrieval Count Experiment

The retrieval count was evaluated using:

- k = 2
- k = 4
- k = 6

| k | Retrieval Hit Rate |
|---|---:|
| 2 | [VALUE]% |
| 4 | [VALUE]% |
| 6 | [VALUE]% |

---

## 4. Chunking Experiment

Three chunk configurations were evaluated.

| Configuration | Chunk Size | Overlap | Number of Chunks | Hit Rate |
|---|---:|---:|---:|---:|
| A | 300 | 30 | [VALUE] | [VALUE]% |
| B | 500 | 50 | [VALUE] | [VALUE]% |
| C | 800 | 100 | [VALUE] | [VALUE]% |

---

## 5. Answer Quality Evaluation

The generated answers were evaluated for:

- Correctness
- Groundedness
- Source availability

Answer accuracy:

[VALUE]%

Grounded response rate:

[VALUE]%

---

## 6. Unanswerable Question

An intentionally unanswerable question was included:

"What is the monthly salary provided to interns?"

The document does not provide salary information.

System response:

[DESCRIBE ACTUAL RESULT]

This test was used to assess whether the system avoided
generating unsupported information.

---

## 7. Final Configuration

Based on the evaluation results, the selected configuration is:

- Chunk size: [VALUE]
- Chunk overlap: [VALUE]
- Retrieval k: [VALUE]

This configuration was selected based on retrieval performance,
answer quality, and the amount of retrieved context.

---

## 8. Conclusion

The evaluation demonstrates the behavior of the RAG pipeline
under different retrieval and chunking configurations.
The experiments were used to select a final configuration
for the integrated application.