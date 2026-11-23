import json
from .inference import Runner
from .mc_grading import MC_Grading

class Scoring:
    def __init__(self, dataset):
        with open(dataset, "r") as f:
            self.data = json.load(f)
            self.grader = MC_Grading()

    def evaluate(self, model, thinking=False, max_new_tokens=16):
        runner = Runner(model)
        outputs = []
        results = []
        for d in self.data:
            output = runner.run(d["prompt"], thinking, max_new_tokens)
            outputs.append(output)
            results.append(self.grader.grade_mcq(output[0]["content"], d["raw_answer"]))
        print(outputs)
        print(results)

        return results

        
