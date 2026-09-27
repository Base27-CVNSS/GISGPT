#!/usr/bin/env python3
"""Reference text/tool SFT runner for VFM-SpatialLM.

This is deliberately model-agnostic. It trains language/tool-planning behavior
from JSONL examples; multimodal encoders are a separate research stage.
"""
from __future__ import annotations

import argparse
import json
from typing import Any


def render_example(row: dict[str, Any]) -> str:
    instruction = row.get("instruction", "")
    inp = json.dumps(row.get("input", {}), ensure_ascii=False, sort_keys=True)
    out = json.dumps(row.get("output", {}), ensure_ascii=False, sort_keys=True)
    return (
        "### Spatial instruction\n"
        + instruction
        + "\n### Structured input\n"
        + inp
        + "\n### Expected output\n"
        + out
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-length", type=int, default=2048)
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--lora", action="store_true")
    args = parser.parse_args()

    from datasets import load_dataset
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        DataCollatorForLanguageModeling,
        Trainer,
        TrainingArguments,
    )

    ds = load_dataset("json", data_files=args.data, split="train")
    tokenizer = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def tokenize(batch: dict[str, list[Any]]) -> dict[str, Any]:
        rows = [
            {key: batch[key][i] for key in batch}
            for i in range(len(batch["instruction"]))
        ]
        texts = [render_example(r) for r in rows]
        return tokenizer(
            texts,
            truncation=True,
            max_length=args.max_length,
            padding=False,
        )

    tokenized = ds.map(tokenize, batched=True, remove_columns=ds.column_names)
    model = AutoModelForCausalLM.from_pretrained(args.model)

    if args.lora:
        from peft import LoraConfig, get_peft_model

        model = get_peft_model(
            model,
            LoraConfig(
                task_type="CAUSAL_LM",
                r=16,
                lora_alpha=32,
                lora_dropout=0.05,
                target_modules="all-linear",
            ),
        )

    training_args = TrainingArguments(
        output_dir=args.output,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        logging_steps=10,
        save_strategy="epoch",
        bf16=True,
        report_to=[],
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )
    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
