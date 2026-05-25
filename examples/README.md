# Examples

This folder contains real, runnable ICM workspaces used by the test suite and as reference.

## `content-creator-demo/`

A scaffolded pipeline workspace (research → script → production) with one populated research output. Use it to:

- See what a working ICM workspace looks like.
- Run the helper scripts against real data:

  ```
  python ../scripts/icm_detect.py content-creator-demo
  python ../scripts/icm_audit.py content-creator-demo
  python ../scripts/icm_remap.py content-creator-demo
  python ../scripts/icm_debloat.py content-creator-demo
  ```

- Provides the test suite fixture (`tests/test_scripts.py` checks this workspace).

Note: the AGENTS.md and CONTEXT.md files still carry their EXAMPLE marker. They are not meant to be edited as if they were a real production project — they are a fixture.
