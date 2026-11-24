# Journal structure and storage

## Choose a journal

Prefer a journal path supplied by the user. Use `records/` next to the loaded `SKILL.md` by default. Workspaces using the same installation share this default location. Create the journal on the first write request and tell the user when the default location was created.

Discussions, conceptual explanations, and fictional demonstrations do not create a real journal. In later conversations, read the existing files from the selected journal location first.

The journal uses Markdown files that can be read and edited directly without an additional database or service.

```text
records/
  journal.md                Journal ID, time zone, version, and rebuildable judgment index
  judgments/J-<id>.md        Proposition, prior, evidence assessments, and update history
  events/E-<id>.md           Event definition, forecast versions, observed results, and revisions
```

IDs are unique and stable within a journal. Prefer short UUIDs and check for collisions. A display title may change while the ID stays fixed. Include the journal ID in references that cross journals.

## Judgment records

Include these sections in each judgment file. Mark unknown fields as pending and keep fictional example values out of real records.

### Original judgment

| Field | Contents |
| --- | --- |
| identity | judgment_id, creation time, original wording, title, and aliases |
| proposition | Subject, proposition H, applicable conditions, and time window or deadline |
| resolution | Criteria, verification source, time and time zone, and handling for inconclusive outcomes |
| initial_prior | Initial probability, rationale, source, estimator, and confirmation status |
| relationships | Related judgment IDs, relationships, and reasons |

Keep vague judgments in `draft`. A formal forecast needs a clear proposition, time window, and resolution criteria. Lifecycle statuses are `draft / active / resolved / inconclusive / retired`. Track pending evidence and recalculation separately from the lifecycle status.

### Initial probability

When a prior is missing, ask the user in their language what initial probability they assign to the judgment and say they can skip it to use the 50% default. If the request also incorporates new evidence, ask for the estimate before that evidence. Give the user a chance to answer when interaction is available. Record any valid value they supply, including 0% or 100%. Ask for clarification if the value is invalid or ambiguous.

If the user skips or provides no number after being asked, use 50%, label the source `default`, record that the user supplied no initial probability and the skill default was used, and mention that in the response. When creating a judgment on its own, save already established details if helpful and keep the prior `null` while waiting. Once established, use the prior to start the first valid model before handling unincorporated evidence. When completing an older record, append the prior and preserve the history of its earlier absence. If the user later explicitly corrects the prior, append a revision using the model version rules.

### Model versions (append-only)

Record `model_version`, creation time, starting probability, rationale, estimator, reason for the version, superseded version, and the evidence IDs and versions already reflected in its starting probability.

- The first model starts at the original prior.
- When correcting the original prior, reprocess the evidence using the corrected prior in a new model version. Keep the original prior and update history.
- A subjective reassessment creates a new starting estimate. Record which evidence it already reflects and update only on additional information. Ask whether it includes a particular item if unclear so the item is counted at most once.
- Keep the proposition when only the model version changes. Create a new judgment for a material change in the proposition.

### Event assessments and update history (append-only)

| Field | Contents |
| --- | --- |
| assessment_id / revision | Unique assessment ID, revision, and prior version |
| event_ref | Event ID, observation version, and the specific outcome E used |
| judged_at / model_version | Assessment time and associated model version |
| evidence_context | Historical evidence IDs and versions making up the conditioning set D |
| likelihood_h / likelihood_not_h | P(E\|H,D) and P(E\|¬H,D), each a value, range, or null |
| likelihood_basis | Source, estimator, reason, and confirmation status for each estimate |
| likelihood_ratio | Value, scenario result, zero, positive infinity, or pending. Identify a calculated value or a direct user estimate |
| direction | Supports, weakens, neutral, or pending. Apply no extra weight for credibility |
| dependence | Basis for independence, or duplicate and related events, shared sources, and joint evidence groups |
| application | applied / pending / duplicate / excluded / superseded, with the reason |
| probability_before / after | Probability before and after the update. Use null for after when no update was applied |
| correction | Reason, superseded item, and affected assessment IDs |

Apply a given observation version at most once in an active model. List members of a joint evidence group and apply either the group or its members. A version that only corrects an event supersedes the old observation without adding evidence. A genuinely new observation can be appended after checking dependence.

### Current view (rebuildable)

Show the active model, applied evidence, current probability, the cutoff time for the calculation, outstanding evidence, and the `valid / pending_recalculation` status.

If earlier evidence has been invalidated and its reassessment is incomplete, flag the old posterior as no longer valid. Show at most the last probability supported by the part of the update chain that still holds, and explain that it excludes some current information. Keep the old model's final probability as history.

### Resolution and review (append-only)

Record the resolution time, actual result, verification source, final prospective forecast and its time, forecast versions, lessons learned, and future improvements. Append a revision if the result is disputed and preserve the original resolution.

## Event records

### Event definition

Record the event ID, creation time, original wording, title, subject, description, verification criteria, forecast deadline, actual occurrence time, time learned, source, and associated judgment IDs. Keep entry time distinct from both occurrence time and prospective forecast time.

### Forecast versions (append-only)

Record forecast ID, recording time, P(E), rationale, forecaster, expected resolution time, and status (`prospective / retrospective_claim / scenario`). Append later adjustments and preserve earlier probabilities.

The user may supply P(E) directly, or it may be derived from a judgment model. For a derived probability, cite the judgment ID, model version, p, a, b, and formula used at the time. Label probabilities derived from different models individually and leave them separate. If a direct user forecast differs from a model-derived forecast, keep both.

### Observation versions (append-only)

Record the version, occurrence time, time learned, entry time, outcome, source, whether the outcome is confirmed, any version it supersedes, and the reason for the correction. Describe the result as occurred, did not occur, partially occurred, unknown, or another applicable category. Preserve partial occurrence as a category rather than coding it as a binary outcome of 0.5.

### Action versions (append as needed)

Record remedial actions, start times, goals, expected effects before implementation, actual results, and whether they change the proposition's conditions. An action can provide new information. Require a basis before increasing the judgment probability and distinguish implementing an action from observing its effect.

## Sync to Notion

In local Markdown, use paths relative to the current file for links to journal records and preserve valid anchors for observation versions. Generate upload copies from the local originals and replace those links with stable Notion URLs for the target records. Keep existing external source links.

1. Find readable Notion record pages in the existing destination by journal and record ID. Update existing pages in place. Create missing pages and obtain their URLs before adding cross-references. Use record page URLs for cross-references because re-uploading Markdown attachments changes their file block IDs.
2. Resolve each relative journal link in the upload copy and check the target record ID. Point attachment links to the record page and preserve the observation version number in the link text. Create any missing target page before syncing files that reference it.
3. Sync files into the existing Notion folder using the original directory structure. Preserve other content when replacing an attachment of the same name. Read back and verify the index, links on record pages and attachments, and both directions of judgment–event references.

## Confirm an official probability update

Before incorporating evidence, recalculating a probability, or making a subjective reassessment the official current estimate, read the journal and prepare the entire write proposal in the conversation. Include the judgment ID, previous and proposed probabilities, evidence and sources, conditional probabilities and likelihood ratio when applicable, and the records that would be created or changed. Identify the proposal with its `operation_id`. List any assistant estimates the proposal needs and explain that confirming the proposal also adopts those estimates.

1. Label the proposal “Awaiting confirmation. Nothing saved yet.” Provide a **Confirm write** button in the user's language through an interactive prompt that can stay in the conversation. When `request_user_input_async` is available, use it with the proposal ID in the question and the localized **Confirm write** as an option. Keep the prompt available while waiting. If the user returns to the proposal after the button expires, offer it again. If the interface cannot retain a button, provide a localized written reply command below the proposal, such as `Confirm write <operation_id>` in English. Honor a localized command previously shown for the same proposal.
2. Proceed only after the user explicitly confirms this proposal. A preselected button, confirmation of the input parameters alone, a timeout, or silence do not count. If the user defers, pause and leave the proposal and confirmation option in the conversation. If the user cancels, invalidate the proposal. Treat the entire operation as read-only until confirmation, including events, judgments, indexes, and drafts under `records/` or the user-selected journal. Only confirmed proposals can be synced to Notion.
3. After confirmation, reread the journal and check the operation ID and the model and evidence versions. If the operation already exists, verify it under its original ID. If the proposed writes or their basis have changed, show an updated proposal and ask for confirmation again. Once verified, write and read back under the rules below. Tell the user that the recorded probability is the one they confirmed.

Standalone observations, prospective forecasts, prior initialization, and read-only queries follow their own workflows. When they are part of an official probability update, they wait with the rest of its proposal.

## Reliable writes

1. Read the latest files and note their versions before writing. If another session has made changes, reread and merge without overwriting its additions.
2. Append facts, forecasts, assessments, and revisions while retaining old sections. The index and current view can be regenerated.
3. Use the same `operation_id` across all files in one operation. Save the event first, then affected judgments, then refresh the index. Check that ID before retrying to avoid duplicate records or updates.
4. When replacing an entire file, prefer a temporary file and atomic replacement or another available safe-write method. If a write partially fails, say which files succeeded and resume using the operation ID. Report completion only after the entire update succeeds.
5. Read back to verify the IDs, reference versions, likelihood ratios, and current view against what was written. Report the record as saved only after verification.

Use the available file tools to follow these conventions when no journal script is available. There is no need to generate a new program for each record.
