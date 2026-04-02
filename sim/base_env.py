"""
Base environment abstraction for MuJoCo task environments.

Subclass ``BaseEnv`` for every new task and implement the three abstract
methods.  The AutoBehavior training loop interacts exclusively through this
interface, so swapping tasks is a matter of changing the ``task.name`` key
in the YAML config.
"""

from __future__ import annotations

import abc
from typing import Any


class BaseEnv(abc.ABC):
    """Abstract base class for a MuJoCo simulation environment.

    Parameters
    ----------
    config:
        The merged configuration dictionary produced by
        :func:`utils.config_loader.load_config`.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.task_cfg = config.get("task", {})
        self.max_steps: int = self.task_cfg.get("max_steps", 500)
        self.dt: float = self.task_cfg.get("dt", 0.02)
        self._step_count: int = 0

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abc.abstractmethod
    def reset(self) -> Any:
        """Reset the environment to an initial state.

        Returns
        -------
        observation
            The initial observation after the reset.
        """

    @abc.abstractmethod
    def step(self, action: Any) -> tuple[Any, float, bool, dict]:
        """Advance the simulation by one step.

        Parameters
        ----------
        action:
            The action produced by the current policy.

        Returns
        -------
        observation:
            Observation after applying *action*.
        reward:
            Scalar reward signal (may be unused in the LLM-critic loop).
        done:
            ``True`` if the episode has ended.
        info:
            Auxiliary diagnostic information.
        """

    @abc.abstractmethod
    def close(self) -> None:
        """Release any resources held by the environment."""

    # ------------------------------------------------------------------
    # Helpers shared by all environments
    # ------------------------------------------------------------------

    def _check_done(self) -> bool:
        """Return ``True`` if the episode has exceeded ``max_steps``."""
        return self._step_count >= self.max_steps
