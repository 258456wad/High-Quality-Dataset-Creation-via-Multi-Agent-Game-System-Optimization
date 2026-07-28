# High-Quality Dataset Creation via Multi-Agent Game System Optimization

Persona-Driven Evolvable Instruction Synthesis: High-Quality Dataset Creation via Multi-Agent Game System Optimization.

This repository records the workflow for generating persona-driven synthetic datasets, filtering finance-domain outputs with a multi-agent game system, and preparing the generated data for downstream model testing.

## Repository Focus

The project contains an experimental pipeline for high-quality synthetic data creation. The core workflow is:

1. Generate candidate synthetic data from persona, instruction, and knowledge sources.
2. Use finance-oriented prompt templates to create professional domain examples.
3. Deduplicate, select, and classify the generated data.
4. Test the selected data in Qwen/LlamaFactory-based model training or evaluation environments.

## Requirements

Install the Python dependencies first:

```bash
pip install -r requirements.txt
```

Configure the DeepSeek API key through an environment variable instead of hard-coding it:

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="YOUR_DEEPSEEK_API_KEY"

# Linux / macOS
export DEEPSEEK_API_KEY="YOUR_DEEPSEEK_API_KEY"
```

If your network requires a proxy or VPN for model API access, enable it before running the synthesis commands.

## 1. Data Generation

### 1.1 Experimental Synthetic Dataset Generation

#### 1.1.1 Local Run

The newer code does not require manually running the demand-planning prompts below, but they are useful references for the planning agent input:

```text
I want to output 5 high-quality synthetic dataset entries that are persona-based and relatively professional.
I want to output 10 high-quality synthetic dataset entries that are persona-based and relatively professional.
I want to output 20 high-quality synthetic dataset entries that are persona-based and relatively professional.
I want to output 200 high-quality synthetic dataset entries that are persona-based and relatively professional.
I want to output 2,000 high-quality synthetic dataset entries that are persona-based and relatively professional.
I want to output 3,000 high-quality synthetic dataset entries that are persona-based and relatively professional.
I want to output 5,000 high-quality synthetic dataset entries that are persona-based and relatively professional.
Finance
I want to output high-quality synthetic dataset entries that are persona-based and relatively professional.
```

Run commands from the project root. For example:

```bash
python code/openai_synthesize.py --template math --sample_size 10 --output_path output_data/test_math.jsonl
```

Non-finance Chinese template example:

```bash
python code/openai_synthesize.py --template universal_gen_v2_cn --sample_size 200 --output_path output_data/universal_gen_v2_cn.jsonl
```

Finance Chinese template example:

```bash
python code/openai_synthesize.py --template finance_cn --sample_size 10 --output_path output_data/test_math.jsonl
```

The `_cn` suffix indicates a Chinese-language prompt template. The finance templates are used for finance-domain synthesis.

#### Stage 1: Generate Diverse Finance Data From the Main Persona Source

Use `persona.jsonl` as the target output file:

```bash
python code/openai_synthesize.py --template stock_analysis_cn --sample_size 100 --output_path output_data/persona.jsonl
```

#### Stage 2: Generate Question-Style Data From the Instruction Source

Use `instruction.jsonl` as the target output file:

```bash
python code/openai_synthesize.py --template trading_strategy_cn --sample_size 100 --output_path output_data/instruction.jsonl
```

#### Stage 3: Generate Article-Style Data From the Knowledge Source

Use `knowledge.jsonl` as the target output file:

```bash
python code/openai_synthesize.py --template stock_knowledge_cn --sample_size 50 --output_path output_data/knowledge.jsonl
```

See `demo_openai_synthesize.sh` for a compact command reference.

#### 1.1.2 Server Run

On the server, enter the project code directory first:

```bash
cd code
```

Run `manager.py` in the background:

```bash
nohup python -u manager.py > train.log 2>&1 &
```

View logs:

```bash
tail -f train.log
tail -n 1000 train.log
```

Check whether the process is still running:

```bash
ps -ef | grep manager.py
```

Stop the process if needed:

```bash
ps -ef | grep manager.py
kill -9 PROCESS_ID
```

#### 1.1.3 Server-Side Dataset Filtering

The filtering stage uses a strict six-category finance taxonomy:

```python
CATEGORIES = {
    "quant_trading": "Quantitative trading and asset management, such as quantitative strategies, asset allocation, robo-advisory, and factor investing",
    "fintech_infra": "Financial technology and infrastructure, such as financial large models, intelligent agents, financial knowledge graphs, and privacy computing",
    "financial_regulation": "Financial regulation, such as look-through supervision, insider-trading detection, front-running detection, anti-money laundering, and market-manipulation prevention",
    "laws_and_regulations": "Laws and regulations, such as securities law, financial compliance review, policy comparison, compliance Q&A accountability, and legal risk auditing",
    "risk_management": "Risk management and credit assessment, such as enterprise ratings, credit risk control, default-probability modeling, systemic risk, and stress testing",
    "digital_finance": "Digital transformation of traditional financial services, such as bank or brokerage intelligent customer service, IPO due-diligence assistance, and intelligent insurance underwriting or claims settlement"
}
```

Run the selector in the background:

```bash
cd code
mkdir -p ../output_data
nohup python -u dataset_select.py > ../output_data/dataset_select.log 2>&1 &
```

View selector logs:

```bash
tail -f ../output_data/dataset_select.log
tail -n 1000 ../output_data/dataset_select.log
```

Check or stop the selector process:

```bash
ps -ef | grep dataset_select.py
kill -9 PROCESS_ID
```

### 1.2 Generation-Only Baseline Without Deduplication

Run the generation-only baseline in the background:

```bash
cd ../baseline-no-dedup-generation
nohup python -u manager.py > train.log 2>&1 &
```

View logs:

```bash
tail -f train.log
tail -n 1000 train.log
```

Check or stop the process:

```bash
ps -ef | grep manager.py
kill -9 PROCESS_ID
```

### 1.3 Original Paper Simulation Baseline

This baseline reproduces a random-sampling style experiment and is not the current multi-agent game experiment.

Run a random-sampling test on the server:

```bash
cd ../control-random-sampling-personahub
python code/openai_synthesize.py --template instruction --sample_size 5000 --output_path output_data/test_instruction_5000.jsonl
```

Background run:

```bash
cd ../control-random-sampling-personahub

nohup python -u code/openai_synthesize.py \
  --template instruction \
  --sample_size 5000 \
  --output_path output_data/test_instruction_5000.jsonl \
  > run_synthesize_instruction_5000.log 2>&1 &

ps -ef | grep openai_synthesize.py
tail -f run_synthesize_instruction_5000.log
```

## 2. Testing the Data in Models

### 2.1 Local Testing

The local testing setup uses Qwen3-0.6B, Qwen3-1.7B, and Qwen3-8B models.

Example local model directory:

```text
../AAA_Python_model
```

After generating new data, copy or register the updated `output_data` files in the model workspace. Also update the corresponding `file_name` entry in:

```text
../AAA_Python_model/LlamaFactory-main/data/dataset_info.json
```

Start LlamaFactory:

```bash
cd ../AAA_Python_model/LlamaFactory-main
llamafactory-cli webui
```

If the command is not available, install the package in editable mode from the LlamaFactory directory:

```bash
pip install -e .
```

Example local model path:

```text
../AAA_Python_model/Qwen3-0.6b
```

Adjust the model path in LlamaFactory and run the experiment directly.

### 2.2 Server Testing

Example server conda environment:

```text
../conda_envs/qwen3_factory
```

Example dataset path:

```text
../AAA_Python_model/output_data/select_output_test_manager.jsonl
```

Activate the environment:

```bash
conda activate ../conda_envs/qwen3_factory
```

Optionally verify that the Python executable points to the expected conda environment:

```bash
which python
```

Enter the LlamaFactory directory:

```bash
cd ../AAA_Python_model/LlamaFactory-main
```

Start the web UI with one of the following commands:

```bash
llamafactory-cli webui
llamafactory-cli webui --host 0.0.0.0 --port 7860
python -m llamafactory.cli webui
CUDA_VISIBLE_DEVICES=0 llamafactory-cli webui --trust_remote_code True
CUDA_VISIBLE_DEVICES=0,1,2,3 llamafactory-cli webui --trust_remote_code True
```

Example server model paths:

```text
../AAA_Python_model/Qwen3-0.6b
../AAA_Python_model/Qwen3-1.7b
../AAA_Python_model/Qwen3-8b
../AAA_Python_model/Qwen3-14b
../AAA_Python_model/Qwen3-32b
```

## Notes

- Do not commit real API keys. Use `DEEPSEEK_API_KEY` or another environment variable.
- Large model weights such as `bge-large-zh-v1.5/pytorch_model.bin` should be downloaded separately or managed with Git LFS instead of being committed directly to the repository.
- Generated JSONL files can be large. Commit representative samples when possible, and keep full production datasets in dedicated storage when they exceed normal GitHub repository limits.
