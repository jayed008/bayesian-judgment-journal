# Bayesian Judgment Journal

[简体中文](README.zh-CN.md)

A Codex skill for recording verifiable judgments and updating their probabilities as new evidence arrives. The journal keeps the original estimate, the rationale for each update, and the eventual outcome so you can review what you knew at the time and why your judgment changed.

## Install and use

With access to the repository and GitHub SSH configured, install the skill in your Codex user-level directory.

```bash
mkdir -p ~/.agents/skills
git clone git@github.com:jayed008/bayesian-judgment-journal.git \
  ~/.agents/skills/bayesian-judgment-journal
```

Select **Bayesian Judgment Journal** in the Codex skill picker or enter `$bayesian-judgment-journal` in an interface that supports `$` mentions. Workspaces using the same skill installation share the default journal. To use a different journal, specify its directory in your request. [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)

## Example project launch judgment

The proposition, dates, and probabilities below are hypothetical. Substitute your own values to start a journal.

**1. Create a judgment.** State the proposition, its conditions, the deadline, and the source you will use to verify the outcome.

If you omit the prior, the skill asks for your initial probability. If you skip the question or supply no number, it starts at **50%** and labels it the default prior.

```text
Use $bayesian-judgment-journal to record this judgment.
Project A will launch within its current scope before 18:00 Beijing time on March 31, 2027, as verified by the signing time of the launch acceptance form.
My initial estimate is 80%, based on the current schedule and delivery outcomes for similar projects.
```

**2. Forecast a related event before its outcome is known.** Define how to verify the event, then estimate how likely it is under each possible outcome of the original judgment.

```text
Record a prospective event forecast for the launch judgment.
Event E is a delay in the integration testing milestone, as verified by the March 10, 2027 milestone record as of 18:00 Beijing time.
I estimate a 20% chance of a delay if the original proposition holds and a 60% chance if it does not.
These are my estimates of how integration delays relate to the launch schedule. Use them for this forecast.
```

**3. Report what happened and request an update.** State what you observed, when you learned it, and where the information came from.

```text
The March 10 milestone record showed at 18:00 Beijing time that integration testing had not finished on schedule. I saw the record that evening.
Incorporate the delay into the original judgment. Show the probabilities before and after the update and where the record will be saved.
```

Under these assumptions, the prospective probability of an integration delay was **28%**. Once the delay is observed, its likelihood ratio is **1/3** and the proposed posterior is **57.1%**, down from **80%**. The skill shows the proposal in the conversation and asks you to confirm it. Select **Confirm write** to save the evidence and official posterior. The proposal and confirmation option stay in the conversation while the update awaits confirmation. If your interface lacks a button, use the text command shown below the proposal.

Once saved, you can look up the current estimate and outstanding evidence by judgment ID. After acceptance, you can resolve the judgment under its original criteria and compare the last prospective forecast with the actual result.

## How the update works

Let $H$ be the original proposition, $E$ the outcome you actually observed, and $D$ the evidence already incorporated. Start with $p=P(H\mid D)$ and estimate $a=P(E\mid H,D)$ and $b=P(E\mid\neg H,D)$. Both estimates describe the same outcome $E$.

$$
\mathrm{LR}=\frac{a}{b},\qquad
P(E\mid D)=pa+(1-p)b,\qquad
P(H\mid D,E)=\frac{pa}{pa+(1-p)b}.
$$

The likelihood ratio measures how well the outcome distinguishes the two possibilities. A ratio above 1 supports the proposition, a ratio below 1 weakens it, and a ratio of 1 leaves the probability unchanged. Equivalently, multiply the odds $p/(1-p)$ by the likelihood ratio and convert back to probability. If a binary event is verified not to have occurred by its deadline, use $1-a$ and $1-b$ for that outcome.

### Evidence and history

- **Count new information once.** A forwarded report adds no evidence on its own. For related events, estimate what each adds given the evidence already included, or evaluate them jointly. Mark evidence as pending when there is too little basis to assess it.
- **Recalculate from the affected step.** If integration testing finished on time and the milestone record was incomplete, append a correction and reassess the affected updates. Keep the earlier update history and confirm the revised estimate before writing.
- **Preserve the original prior and prospective forecasts.** A direct change in confidence is recorded as a subjective reassessment with its rationale and the evidence it already reflects. Resolve judgments under their original criteria. Use timestamped prospective forecasts to assess long-term performance with the Brier score.

## Journal files

The default journal is the `records/` directory next to the installed `SKILL.md`, created on the first write. With the installation above, it is `~/.agents/skills/bayesian-judgment-journal/records/`. The journal uses plain Markdown.

```text
records/
  journal.md          Journal metadata and judgment index
  judgments/          Priors, evidence assessments, and update histories
  events/             Event definitions, forecasts, observations, and revisions
```

See the [skill instructions](SKILL.md), [journal structure and storage](references/journal.md), [probability updates and corrections](references/updating.md), and [forecast review and examples](references/review.md).

## License

[MIT License](LICENSE).
