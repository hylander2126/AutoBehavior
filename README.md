# AutoBehavior
Qualitatively train robotic systems for imitation learning. Use an LLM as both policy generator and critic in a simulation loop, replacing traditional differentiable loss functions with qualitative/semantic feedback. Inspired by Karpathy's autoresearch, but applied to robot behavior synthesis.

## Repository Structure

```
AutoBehavior/
├── config/                  # YAML configuration files
│   ├── default.yaml         # Default config (task, LLM, critic, training settings)
│   └── tasks/               # Per-task overrides
│       ├── cartpole.yaml
│       └── ant.yaml
├── sim/                     # MuJoCo task environments
│   ├── __init__.py
│   └── base_env.py          # Abstract BaseEnv – subclass for each new task
├── policies/                # LLM-generated controller code (populated at runtime)
│   ├── __init__.py
│   └── base_policy.py       # Abstract BasePolicy – every generated module must implement this
├── demos/                   # Recorded reference trajectories (.npz / .json)
│   └── __init__.py
├── critic/                  # LLM evaluation pipeline
│   ├── __init__.py
│   ├── base_critic.py       # Abstract BaseCritic – subclass for each LLM provider
│   └── prompts/             # Critic prompt templates (YAML)
│       ├── default_prompt.yaml
│       ├── cartpole_prompt.yaml
│       └── ant_prompt.yaml
├── logs/                    # Per-iteration trajectory logs (git-ignored at runtime)
├── utils/                   # Shared utilities
│   ├── __init__.py
│   └── config_loader.py     # YAML config loader with deep-merge support
├── main.py                  # Training loop entry point
└── requirements.txt
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with the default config (CartPole task)
python main.py

# Run with a different task
python main.py --task ant

# Override the number of iterations
python main.py --task cartpole --iterations 20

# Use a custom base config file
python main.py --config path/to/my_config.yaml
```

## Configuration System

All settings live in YAML files under `config/`.  The loader (`utils/config_loader.py`) applies a **deep-merge** strategy:

1. `config/default.yaml` is loaded first as the base.
2. If a matching `config/tasks/<task_name>.yaml` exists, its keys are merged on top – task-level values override defaults, everything else is inherited.

**Swappable knobs (no code changes required):**

| What to change | Config key |
|---|---|
| Task / environment | `task.name` |
| LLM model | `llm.model` |
| LLM temperature | `llm.temperature` |
| Critic prompt | `critic.prompt_file` |
| Training iterations | `training.iterations` |
| Demo directory | `demos.directory` |
| Log directory | `training.log_directory` |

## Extending

### Adding a new task
1. Create `config/tasks/<task_name>.yaml` with task-specific overrides.
2. Subclass `sim.base_env.BaseEnv` and implement `reset`, `step`, and `close`.
3. Add a matching critic prompt at `critic/prompts/<task_name>_prompt.yaml`.

### Adding a new LLM provider
Subclass `critic.base_critic.BaseCritic` and implement `_call_llm`.  Point to it via the config or training loop.
