# Probability updates and corrections

## Quantities and formulas

H is the original proposition. ¬H is its complete complement under the same scope. D is the evidence already incorporated. Evaluate ¬H across its full scope, including ordinary ways the proposition could fail.

- `p = P(H|D)` is the probability before updating.
- `a = P(E|H,D)` is the probability of observing E if H holds, given D.
- `b = P(E|¬H,D)` is the probability of observing the same E if H does not hold, given D.
- `LR = a / b` is the conditional likelihood ratio for this evidence.
- `q = p × a + (1 − p) × b` is the event probability under the model.
- `p_new = p × a / q` is the posterior after observing E.

The equivalent odds update is `O_new = O_old × LR`, where `O = p/(1−p)`. Apply LR to the odds and convert back to a probability.

LR > 1 supports H, LR < 1 weakens H, and LR = 1 leaves the probability unchanged. Values close to 1 usually have little effect and still belong in the record. Avoid arbitrary thresholds for what counts as evidence.

Only a q recorded before the observation qualifies as a prospective forecast. Mark q reconstructed from old inputs after the observation as a retrospective calculation and exclude it from prospective scoring.

## Inputs and uncertainty

- Use probabilities in [0,1], convert percentages explicitly, and require LR to be nonnegative. Reject invalid inputs such as negative values, out-of-range probabilities, and NaN.
- Record where the inputs came from and whether they account for D. Treat assistant suggestions as scenarios until the user adopts them for an official update.
- If the user supplies only LR, it can be recorded as a direct estimate. When the user explicitly adopts it and the evidence conditions are clear, use `p_new = p×LR/(1−p+p×LR)`. Keep a, b, and q unknown.
- P(E) alone does not determine LR. A posterior supplied by the user alone is a subjective reassessment. Record it without inventing a likelihood.
- When only ranges are available, evaluate plausible parameter combinations and report a sensitivity range instead of silently taking the midpoint. Label it a scenario range. Statistical confidence or credible intervals carry different meanings. Bayesian integration requires a parameter distribution.
- Use reliability, source quality, and domain experience to explain the inputs or build an explicit model. Avoid arbitrary credibility multipliers on LR.
- Record observations of expressions, gaze, or movements separately from psychological interpretations. A story alone provides no calibration for assigning strong evidence to an averted gaze. Record it as pending or show a hypothetical scenario.

## Direction of the observation

When a prospectively forecast event E does not occur, the evidence is ¬E. With the same conditioning information and a complete binary partition:

- `P(¬E|H,D) = 1 − a`
- `P(¬E|¬H,D) = 1 − b`
- `LR_absent = (1 − a)/(1 − b)`, generally different from `1/LR`

Apply ¬E only once the original observation deadline has passed and the criteria confirm non-occurrence. A lack of news can serve as evidence only when the model explicitly defines “no news by this time” as the observation. For partial occurrence or multiple outcomes, use the conditional probabilities of the category actually observed. Mark it pending if the category is undefined.

## Sequential events and duplicate evidence

Use a and b conditional on D for each update. Use likelihood ratios without explicit conditioning on the evidence history only when conditional independence is reasonable under both H and ¬H.

1. Mark reposts from the same source, repeated reports, and observation versions already applied as `duplicate`. Count them once.
2. For observations with a shared cause or from the same process, record the dependence and estimate the marginal contribution as a likelihood ratio conditional on the observations already known.
3. If a complete joint model is available, group related events and apply the joint likelihood ratio in place of the individual ratios.
4. If the incremental or joint ratio cannot reasonably be estimated, mark the assessment as pending. Avoid assuming independence or applying arbitrary discounts.

Calculate separate judgments independently by default. Use the same judgment and `1−p` for an exact complement. For mutually exclusive and exhaustive hypotheses, require priors and likelihoods for the same evidence across all hypotheses, then normalize together. Only normalize across hypotheses when the joint specification is complete.

## Zero, one, and impossible evidence

- When a = b = 0, the observation is impossible under the model and LR is undefined. Halt the update and check the event or model. A neutral LR of 1 does not apply.
- When q = 0, the posterior is undefined. Preserve the observation and flag the model conflict. Avoid division by zero and unannounced smoothing.
- When b = 0 and a > 0, LR is positive infinity. When a = 0 and b > 0, LR = 0. Record the justification for the boundary value and clarify whether the user means a mathematical zero if the language is colloquial.
- When p is 0 or 1, a finite likelihood ratio generally cannot move it. Preserve the exact prior. If the user corrects an absolute judgment, append a prior revision.
- Direct LR = ∞ with p = 0, or LR = 0 with p = 1, produces an impossible-evidence conflict. The posterior is undefined.
- A modeled posterior of 0 or 1 does not resolve the real outcome. Follow the original criteria and verification source to resolve the judgment.

## Revisions and recalculation

1. Distinguish new information, corrections to observations, changes to conditional probabilities, prior corrections, and subjective reassessments. Record the reason and both versions.
2. Find all judgments, models, and later assessments that reference the old observation or estimate. Preserve the original update chain and mark it as superseded.
3. Recalculate from the last valid probability before the earliest affected step. For a prior correction, start from the revised prior. Replace the corrected evidence instead of adding it as a new independent observation.
4. Reassess later likelihood ratios when their evidence context D has changed. Removing the old ratio alone can leave dependent estimates invalid. Keep unaffected assessments when the reason is clear.
5. If the inputs are complete, preview the new update chain and current view in the conversation. Follow [Confirm an official probability update](journal.md#confirm-an-official-probability-update) before writing. If inputs are missing, explain the pending recalculation and show the last still-valid probability and unresolved items in the conversation.
6. When a remedial action changes the proposition's conditions, create a related judgment. Keep the original and continue, resolve, or mark it `retired` under its original criteria. Preserve the old forecast and its conditions.

## Numerical examples

The inputs below are hypothetical and serve only as examples.

| Scenario | p | a | b | Result |
| --- | ---: | ---: | ---: | --- |
| Delay weakens an on-time completion judgment | 0.8 | 0.2 | 0.6 | LR = 1/3, q = 0.28, posterior ≈ 0.571429 |
| Same model with no delay | 0.8 | 0.8 | 0.4 | LR = 2, q = 0.72, posterior ≈ 0.888889 |
| Equally likely under both conditions | 0.6 | 0.5 | 0.5 | LR = 1, posterior = 0.6 |
| A failed pilot weakens a judgment about meeting the final target | 0.8 | 0.35 | 0.75 | LR ≈ 0.466667, q = 0.43, posterior ≈ 0.651163 |
| Impossible under both conditions | 0.6 | 0 | 0 | LR and posterior undefined. Review the model |

If the first delay report is forwarded, the posterior stays at about 0.571429. Multiplying the odds by 1/3 a second time would incorrectly yield about 0.307692.
