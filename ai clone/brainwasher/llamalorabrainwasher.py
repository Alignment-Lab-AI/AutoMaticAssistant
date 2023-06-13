import os
import sys
from typing import List

import fire
import torch
import transformers
from datasets import load_dataset

from peft import (
    LoraConfig,
    get_peft_model,
    get_peft_model_state_dict,
    prepare_model_for_int8_training,
    set_peft_model_state_dict,
)
from transformers import LlamaForCausalLM, LlamaTokenizer

from utils.prompter import Prompter

def print_training_params(params: dict):
    print(
        f"Training Alpaca-LoRA model with params:\n"
        + "\n".join([f"{k}: {v}" for k, v in params.items()])
    )

def load_model_and_config(base_model: str, device_map: str):
    model = LlamaForCausalLM.from_pretrained(
        base_model,
        load_in_8bit=True,
        torch_dtype=torch.float16,
        device_map=device_map,
    )
    config = LoraConfig(
        r=lora_r,
        lora_alpha=lora_alpha,
        target_modules=lora_target_modules,
        lora_dropout=lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, config)
    return model

def load_data(data_path: str):
    if data_path.endswith(".json") or data_path.endswith(".jsonl"):
        data = load_dataset("json", data_files=data_path)
    else:
        data = load_dataset(data_path)
    return data

def train(
    base_model: str = "",
    data_path: str = "yahma/alpaca-cleaned",
    output_dir: str = "./lora-alpaca",
    batch_size: int = 128,
    micro_batch_size: int = 4,
    num_epochs: int = 3,
    learning_rate: float = 3e-4,
    cutoff_len: int = 256,
    val_set_size: int = 2000,
    lora_r: int = 8,
    lora_alpha: int = 16,
    lora_dropout: float = 0.05,
    lora_target_modules: List[str] = [
        "q_proj",
        "v_proj",
    ],
    train_on_inputs: bool = True,
    add_eos_token: bool = False,
    group_by_length: bool = False,
    wandb_project: str = "",
    wandb_run_name: str = "",
    wandb_watch: str = "",
    wandb_log_model: str = "",
    resume_from_checkpoint: str = None,
    prompt_template_name: str = "alpaca",
):
    # assert base_model and then print all the params
    assert base_model, "Please specify a --base_model, e.g. --base_model='huggyllama/llama-7b'"
    print_training_params(locals())

    gradient_accumulation_steps = batch_size // micro_batch_size
    prompter = Prompter(prompt_template_name)

    device_map = "auto"
    world_size = int(os.environ.get("WORLD_SIZE", 1))
    ddp = world_size != 1
    if ddp:
        device_map = {"": int(os.environ.get("LOCAL_RANK") or 0)}
        gradient_accumulation_steps = gradient_accumulation_steps // world_size

    # Check if parameter passed or if set within environ
    use_wandb = len(wandb_project) > 0 or (
        "WANDB_PROJECT" in os.environ and len(os.environ["WANDB_PROJECT"]) > 0
    )
    if len(wandb_project) > 0:
        os.environ["WANDB_PROJECT"] = wandb_project
    if len(wandb_watch) > 0:
        os.environ["WANDB_WATCH"] = wandb_watch
    if len(wandb_log_model) > 0:
        os.environ["WANDB_LOG_MODEL"] = wandb_log_model

    model = load_model_and_config(base_model, device_map)

def setup_tokenizer(base_model: str, add_eos_token: bool):
    tokenizer = LlamaTokenizer.from_pretrained(base_model)
    tokenizer.pad_token_id = 0  # we want this to be different from the eos token
    tokenizer.padding_side = "left"  # Allow batched inference
    return tokenizer


def tokenize_prompt(prompter: Prompter, data_point: dict, cutoff_len: int, train_on_inputs: bool, add_eos_token: bool):
    def internal_tokenize(prompt, add_eos_token=True):
        result = tokenizer(
            prompt,
            truncation=True,
            max_length=cutoff_len,
            padding=False,
            return_tensors=None,
        )
        if (
            result["input_ids"][-1] != tokenizer.eos_token_id
            and len(result["input_ids"]) < cutoff_len
            and add_eos_token
        ):
            result["input_ids"].append(tokenizer.eos_token_id)
            result["attention_mask"].append(1)

        result["labels"] = result["input_ids"].copy()

        return result

    full_prompt = prompter.generate_prompt(
        data_point["instruction"],
        data_point["input"],
        data_point["output"],
    )
    tokenized_full_prompt = internal_tokenize(full_prompt)
    if not train_on_inputs:
        user_prompt = prompter.generate_prompt(
            data_point["instruction"], data_point["input"]
        )
        tokenized_user_prompt = internal_tokenize(user_prompt, add_eos_token=add_eos_token)
        user_prompt_len = len(tokenized_user_prompt["input_ids"])

        if add_eos_token:
            user_prompt_len -= 1

        tokenized_full_prompt["labels"] = [-100] * user_prompt_len + tokenized_full_prompt["labels"][user_prompt_len:]
    return tokenized_full_prompt

if __name__ == "__main__":
    fire.Fire(train)