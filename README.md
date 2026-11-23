# temp readme documenting steps i took


### initializing the project
1. install python (specifically here its 3.11) 
2. check if its installed
```python
python --version
conda --version
```
3. create conda venv
```bash
conda create -n cs886 python=3.11 pip
```
4. **do this before every run** - activate venv
```bash
conda activate cs886
```
5. install libraries
```bash
python -m pip install -r requirements.txt
```
5. setup run.sbatch to run code
- specifically the memory, gpu, and other choices are file dependent
```bash
sbatch run.sbatch
```
### code documentation/steps
1. quickstart.py
- https://huggingface.co/Qwen/Qwen3-0.6B#quickstart
2. i then made inference.py and main.py, just creating a class to define which model we want and a runner function to make it easier to laod multiple models
3. then i created a simple testing scenario and files, scoring.py scores the outputs from inference.py, and evaluate just combines that into a single function of running and scoring so we can just say evaluater.evaluate("model_name") and get results
4. i create sample "sam_predictions" where sam has preferences that span random time periods and we see if the model holds that up correctly