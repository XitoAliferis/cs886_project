from temporal_eval.inference import Runner

runner = Runner("Qwen/Qwen3-0.6B")

inputs = [
    "testing does this work?",
    "what's 9+10?"
]
runner.run(inputs)