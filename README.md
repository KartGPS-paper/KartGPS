# KartGPS
Code of paper: KartGPS: Knowledge Base Update with Temporal Graph Pattern-based Semantic Rules

### Main Requirements:
Python>=3.6
numpy >= 1.21.4
joblib = 1.2.0
pandas = 1.3.4
rdflib = 7.0.0

### KG Data:
entity2id.json, relation2id.json, ts2id.json define the mapping of entities, relations, and timestamps to their corresponding IDs

### Usage
In main.py:

--dataset, -d: str. Dataset name.

--rule_lengths, -l: int. Length(s) of rules that will be learned, e.g., 1 2 3.
