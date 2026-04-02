Phase 1 — Demo Recording & Replay
Build a minimal task in MuJoCo (a push-to-goal with your IRB120 is the obvious first candidate since you already have mujoco_irb120). Record a human demo — this means logging the full state trace: joint positions, end-effector pose, object pose, contact wrenches, timestamps. Store it as a structured format (HDF5 or just numpy archives). Write a replay visualizer so you can sanity-check demos. This is your "ground truth specification."
Phase 2 — LLM Policy Generation (The "First Stab")
This is where you'd call Claude or GPT-4 via API. The prompt template is critical — it needs to include: the task description, the sim environment spec (object geometry, start/goal pose, robot kinematics), and a policy interface contract (e.g., "write a function get_action(obs) -> action where obs is [joint_pos, ee_pose, object_pose, ft_reading] and action is [desired_joint_velocities]"). The LLM writes Python code. You sandbox it and run it in MuJoCo. Save the resulting trajectory in the same format as the demo.
Phase 3 — The Critic (Soft Loss Function)
This is the research core. Build a critic pipeline that takes two trajectory logs (demo vs. attempt) and produces a structured evaluation. The critic has two layers:

Automatic metrics: compute them in code — pose error at terminal time, trajectory DTW distance, max contact force, smoothness (jerk), task success binary, time-to-completion ratio.
LLM qualitative critique: feed the metrics + a subsampled state trace (or even rendered frames) to the LLM and ask it to diagnose what went wrong and suggest specific changes.

The output is a structured "critique document" — both the numbers and the natural-language analysis — that gets fed back into the next generation step.
Phase 4 — The Iteration Loop
Wire phases 2 and 3 into a loop. Each iteration: run policy → collect trajectory → critic evaluates → LLM rewrites policy → repeat. Key engineering decisions here: do you give the LLM its previous code + the critique (so it edits incrementally), or do you regenerate from scratch each time? Incremental is almost certainly better — it prevents catastrophic forgetting of things that were working. Keep a full history of all iterations (code + trajectory + critique) so you can analyze convergence.
Phase 5 — Evaluation & Analysis
Define what "success" means: does the metric converge? Does it converge faster than a human manually tuning the same controller? Does the qualitative loss catch things the quantitative metrics miss? Plot iteration-vs-performance curves. Compare against a baseline of pure quantitative optimization (e.g., CMA-ES over the same parameterized controller).
Phase 6 — Generalize
If push-to-goal works, try it on tipping. Then try a task where the LLM needs to discover the right interaction mode (slide vs. tip) — that's where the qualitative reasoning should really shine over scalar losses. This is where it connects back to your thesis.

The riskiest part is Phase 3 — whether the LLM critique is specific enough to drive convergence rather than going in circles. I'd prototype that piece first, even before the full loop: take a demo trajectory and a deliberately bad trajectory, and see if the LLM can produce a critique that a human would agree with and find actionable. If that works, the rest is plumbing.
