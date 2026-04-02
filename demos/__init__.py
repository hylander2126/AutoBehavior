"""
demos package – recorded reference trajectories.

Reference trajectories are saved as ``.npz`` or ``.json`` files inside this
directory.  Each file contains the observations, actions, and any metadata
captured during a demonstration episode.

Expected ``.npz`` schema
------------------------
observations : np.ndarray, shape (T, obs_dim)
    Sequence of observations for the episode.
actions : np.ndarray, shape (T, act_dim)
    Corresponding sequence of actions.
metadata : dict  (stored as a pickled object array)
    Arbitrary task/environment metadata (e.g. ``task_name``, ``dt``).
"""
