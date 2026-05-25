# Research — ICM Explained

> Sample output. Produced by stage 01 from the user prompt "explain ICM to people who have never built an AI system".

## One-Liner

ICM (Interpretable Context Methodology) replaces multi-agent frameworks with filesystem structure — folders and markdown files that route a single agent through a workflow.

## Key Points

1. **Most "AI agents" are not autonomous.** They're prompts + orchestration code, sequenced by a human-defined flow. The AI is ~10% of the system.
2. **Folders can be the orchestration layer.** Numbered folders encode execution order; markdown files carry context; the routing table is the spine.
3. **Five layers of context.** Global identity → workspace routing → stage contract → references → working artifacts. Each layer answers a different question.
4. **Context scoping beats context cramming.** Loading 5k relevant tokens beats loading 40k of which most is noise.
5. **No framework to learn.** Anyone with a text editor can read, edit, or fork an ICM workspace.

## Examples

- A 3-stage video pipeline: research → script → animation. Same single agent at each stage, different context loaded.
- Non-technical users at the Neuropolitics Lab (Edinburgh) ran 10-minute animated videos by editing markdown.
- A workspace is just a folder. Zip it, email it, commit it to git.

## Counter-arguments / Open questions

- ICM does NOT fit real-time multi-agent collaboration. AutoGen / CrewAI are better for that.
- It does NOT fit conditional routing that needs the model to decide branches mid-pipeline.
- Open: how does ICM compose when one stage needs the model to call an external tool that itself spans multiple steps?

## Narrative Angles

- **The Unix angle:** ICM is Unix pipelines applied to AI orchestration. 1970s ideas, 2020s problems.
- **The 60/30/10 angle:** Most production AI systems are 60% traditional code, 30% rules, 10% AI. ICM makes that visible.
- **The "workspace as factory" angle:** Configure the factory once; each run produces a new deliverable. Stable vs variable, separated by layer.
