"""
AutoBehavior – main entry point.

Loads the configuration, resolves the environment and critic, then runs the
generate → simulate → critique training loop for the configured number of
iterations.

Usage
-----
    python main.py                     # uses config/default.yaml
    python main.py --task ant          # override task
    python main.py --config my.yaml    # use a custom base config
    python main.py --iterations 5      # run for 5 iterations
"""

from __future__ import annotations

import argparse
import logging

from utils.config_loader import load_config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AutoBehavior training loop")
    parser.add_argument("--config", default=None, help="Path to base YAML config file")
    parser.add_argument("--task", default=None, help="Task name (overrides config task.name)")
    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help="Number of generate→simulate→critique iterations",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Load and merge configuration
    cfg = load_config(config_path=args.config, task=args.task)

    # CLI overrides
    if args.iterations is not None:
        cfg.setdefault("training", {})["iterations"] = args.iterations

    task_name = cfg.get("task", {}).get("name", "unknown")
    iterations = cfg.get("training", {}).get("iterations", 10)
    llm_model = cfg.get("llm", {}).get("model", "unknown")

    logger.info("AutoBehavior starting")
    logger.info("  task       : %s", task_name)
    logger.info("  llm model  : %s", llm_model)
    logger.info("  iterations : %d", iterations)
    logger.info("  log dir    : %s", cfg.get("training", {}).get("log_directory", "logs/"))

    # TODO: instantiate the environment, policy generator, and critic from
    # the config and run the training loop here.
    logger.info("Configuration loaded successfully. Training loop not yet implemented.")


if __name__ == "__main__":
    main()
