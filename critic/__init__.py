"""
critic package – LLM evaluation pipeline for AutoBehavior.

The critic queries an LLM with a trajectory summary and a prompt template to
produce a qualitative score and textual feedback.  This feedback drives the
next round of policy generation without a differentiable loss function.
"""
