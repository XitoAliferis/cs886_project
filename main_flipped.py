from temporal_eval.scoring import Scoring
from generators.generate_tests import Generators

seed = 42 
generator = Generators("tests/dataset_flipped.json")
data = generator.generateData(amount = 10000, short_distribution = 0.5, followup_applies_distribution = 0.5, start = 2000, end = 2026, flip_options=True, seed = 42)


Scoring("tests/dataset_flipped.json").evaluate("Qwen/Qwen3-0.6B", thinking=False, max_new_tokens=16)