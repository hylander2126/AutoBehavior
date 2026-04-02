"""
Base policy interface for AutoBehavior.

Every LLM-generated policy module must expose a class called ``Policy`` that
subclasses ``BasePolicy`` and implements the ``act`` method.  The training
loop loads policies by importing the generated module and calling::

    from policies.<generated_module> import Policy
    policy = Policy(config)
    action = policy.act(observation)
"""

from __future__ import annotations

import abc
from typing import Any


class BasePolicy(abc.ABC):
    """Abstract base class for a controller policy.

    Parameters
    ----------
    config:
        The merged configuration dictionary produced by
        :func:`utils.config_loader.load_config`.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    @abc.abstractmethod
    def act(self, observation: Any) -> Any:
        """Compute and return an action for the given *observation*.

        Parameters
        ----------
        observation:
            Current environment observation (numpy array or similar).

        Returns
        -------
        action
            The action to apply to the environment.
        """

    def reset(self) -> None:
        """Optional hook called at the start of every episode."""
