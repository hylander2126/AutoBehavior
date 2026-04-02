"""
Base LLM critic for AutoBehavior.

Subclass ``BaseCritic`` to implement provider-specific API calls (OpenAI,
Anthropic, etc.).  The training loop calls ``critique`` once per episode and
passes the returned score and feedback to the policy generator.
"""

from __future__ import annotations

import abc
import string
from pathlib import Path
from typing import Any

import yaml


class BaseCritic(abc.ABC):
    """Abstract base class for an LLM-based trajectory critic.

    Parameters
    ----------
    config:
        The merged configuration dictionary produced by
        :func:`utils.config_loader.load_config`.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.critic_cfg = config.get("critic", {})
        self.llm_cfg = config.get("llm", {})

        # Load the prompt template
        prompt_file = self.critic_cfg.get("prompt_file", "critic/prompts/default_prompt.yaml")
        self._prompt_template = self._load_prompt(Path(prompt_file))

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abc.abstractmethod
    def _call_llm(self, prompt: str) -> str:
        """Send *prompt* to the LLM and return the raw text response.

        Implement this method for each LLM provider (OpenAI, Anthropic, …).
        """

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def critique(self, trajectory: dict[str, Any]) -> dict[str, Any]:
        """Evaluate a trajectory and return a score with textual feedback.

        Parameters
        ----------
        trajectory:
            Dictionary with at minimum the keys ``observations``, ``actions``,
            and ``task_name``.  Additional keys (e.g. ``total_reward``,
            ``episode_length``) are passed through to the prompt template.

        Returns
        -------
        dict
            A dictionary with at minimum a ``score`` key (float in [0, 1])
            and a ``feedback`` key (str).
        """
        prompt = self._build_prompt(trajectory)
        raw_response = self._call_llm(prompt)
        return self._parse_response(raw_response)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_prompt(path: Path) -> dict[str, Any]:
        """Load a YAML prompt template from *path*."""
        if not path.exists():
            raise FileNotFoundError(f"Critic prompt file not found: {path}")
        with path.open() as f:
            return yaml.safe_load(f) or {}

    def _build_prompt(self, trajectory: dict[str, Any]) -> str:
        """Fill the prompt template with trajectory data."""
        template_str: str = self._prompt_template.get("template", "")
        # Use safe_substitute so missing keys are left as-is instead of raising
        return string.Template(template_str).safe_substitute(trajectory)

    def _parse_response(self, raw: str) -> dict[str, Any]:
        """Parse the LLM response into a structured result dict.

        The default implementation looks for a YAML block in the response.
        Override this method for provider-specific parsing.
        """
        try:
            parsed = yaml.safe_load(raw)
            if isinstance(parsed, dict):
                return parsed
        except yaml.YAMLError:
            pass
        # Fallback: return the raw text as feedback with an unknown score
        return {"score": None, "feedback": raw}
