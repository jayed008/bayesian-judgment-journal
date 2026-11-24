# Forecast review and examples

## Resolve a judgment

Use the deadline, criteria, and verification source recorded when the judgment was created. Mark the judgment resolved once it is clear whether the proposition held. Mark partial fulfillment, missing information, or unresolved disputes as `inconclusive` unless the original criteria resolve them.

List each of these items separately.

- The initial forecast and its rationale at the time.
- The last forecast recorded before the outcome became known, along with key intermediate updates.
- The actual result, when it occurred and became known, and the verification source.
- Estimates or observations that warrant correction and ways to improve future forecasts.

Use only forecasts made before the outcome became known for prospective scoring. A later recalculation can show what a different model would have predicted at the time. Preserve the historical scores.

## Review questions

Use the evidence to answer these questions. A forecast can miss even when the reasoning was sound.

1. Was the prior well founded? Were relevant base rates overlooked or experiences from another subject applied without justification?
2. Was information available at the time missed? Use only information that could actually have been obtained then.
3. Did the two conditional estimates overstate or understate how well the evidence discriminated between outcomes?
4. Were related observations counted twice, unknown results treated as non-occurrences, or actions treated as successful before their effects were observed?
5. Did the proposition or deadline change? How many forecasts remain unresolved or unverifiable?
6. What concrete change would improve future forecasts? Record suggestions and preserve past priors and unrelated judgments.

An event forecast at 70% can fail to occur. Assess calibration across a set of timestamped, verifiable prospective forecasts.

## Assess long-term performance

When asked about performance, first define the forecasts to score and the selection rule. Score judgment forecasts and event forecasts separately. Use the first eligible prospective forecast per target by default. The last prospective forecast can be reported separately. Use one forecast per target in each analysis.

- For binary outcomes, the Brier score is `mean((p − y)^2)`, where y is 0 or 1. Lower is better. Report the sample size, period, and selection rule. Small samples are insufficient for stable calibration conclusions.
- Group similar probabilities and compare their mean forecast probability with their observed frequency. Note dependence among closely related events or targets when interpreting the sample size.
- Exclude retrospective claims, demonstrations, unknown outcomes, and outcomes that fail the original verification criteria from prospective scoring. Report how many were excluded and why. Include both successes and failures that meet the selection rule.
- If several judgment models predict an event, score them separately or designate a primary forecast in advance. Use a designation made before the outcome was known.
- A subjective reassessment recorded before the outcome became known can be scored for that time point. Keep its source label.

## Interaction examples

These examples illustrate behavior. Treat them as fictional data.

### Same judgment or different judgment

The existing judgment gives Project A a 60% chance of launching by March 31, 2027, on its current budget, as verified by the launch acceptance form.

- “I now give A a 40% chance of launching on its original budget by the end of March.” Match the original judgment and capture the subjective reassessment and rationale. Reuse the existing judgment and leave LR unspecified.
- “How likely is A to become profitable by the end of June?” Create a related judgment about the new proposition and clarify what counts as profitable.
- “A can launch by the end of March, but it needs more funding.” Create a new judgment for the changed conditions and keep the original budget judgment.

### One event linked to two judgments

“A client delayed payment” may relate to “The project has enough cash for six months” and “The client will renew.” Store the event facts once. Estimate P(E|H,D), P(E|¬H,D), and LR separately for each judgment. Use the renewal judgment's own LR to update it.

### Insufficient information

The user says, “The founder looked away briefly when talking about competitors. I have a bad feeling about it.”

Record the observed change in gaze and the user's interpretation, then look for related judgments. Mark the observation as pending assessment if there is no basis for estimating the likelihoods. Leave the probability and the person's mental state undetermined by this observation. An 80% to 65% change from an example does not apply automatically.

### Correction

The user initially reports that a client did not pay, then verifies that the client paid on time and the system had not logged the payment.

Preview the observation revision, cite the old version, and explain the correction. Find every judgment that used “did not pay” and reassess each from its earliest affected step. Preserve the original record and apply only the corrected observation. Reassess later likelihood ratios that depended on the original result. If they cannot be reassessed yet, say that recalculation is pending. After recalculating, ask for confirmation before saving the revision and official probability together.

### Look up the current probability

The user asks, “How confident are we now in that original project judgment?”

Identify the proposition the user means. Look it up directly if the match is clear, or ask which judgment they mean. Report the original prior, current valid probability, main factors behind any changes, the estimate's cutoff time, and outstanding evidence. Keep the original prior intact.
