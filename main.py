from temporal_eval.scoring import Scoring

scoring = Scoring("tests/sam.json")

results = scoring.evaluate("Qwen/Qwen3-0.6B", False, 16)