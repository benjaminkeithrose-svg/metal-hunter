# Working on Metal Hunter

## How Ben wants changes made
1. **Propose first.** For anything beyond a trivial fix, come back with a proposal (options, mockups or a short plan) before touching the code.
2. **Ask before building.** End the proposal with a yes/no question box (AskUserQuestion), plus any other questions you need answered. Only build after Ben clicks yes.
3. **Build on a branch.** Never commit straight to `main`. Push the work to a feature branch and open a pull request.
4. **Ask before merging.** When the branch is ready, ask with a yes/no question box: "Do you want me to merge it?" Merge the pull request only after Ben clicks yes.

Ben's yes to the question box is the approval. Don't ask him to repeat it in chat.

## Exception: scheduled data refreshes
The scheduled refresh tasks (Mon and Thu news check, monthly full band sweep) may commit and push straight to `main` without a pull request or merge question, but only when:
- the commit changes nothing except `data/events.json`, `data/bands.json` and `docs/INSTRUCTIONS.md`;
- `python3 scripts/validate.py` passes (JSON parses, tours and shows are complete, no checked band slips back to `unchecked`);
- the commit message starts with `Data refresh:`.
If a run finds something that needs a code or design change, or the checks fail, push nothing to `main`: open a pull request instead and say why. Everything else still follows steps 1 to 4 above. (Ben approved this on 22 Oct 2026.)

