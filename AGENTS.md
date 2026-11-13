# Project Working Instructions

These instructions apply to this standalone COMP1890 Spatial Data Science project. Use a conventional project layout rooted at this repository. Keep the workflow simple and proportionate to academic work; do not introduce production infrastructure without an agreed need.

## Human approval and AI collaboration

- Use Human-in-the-Loop (HITL): Codex and Claude may independently assess evidence, form technical judgments and make recommendations. Final decisions and permission to implement changes remain with Chathuranga.
- Codex and Claude can each act as a coding tool or an independent reviewer, as assigned by Chathuranga for the task. Neither has a permanent exclusive coding role. A tool's review of its own changes is self-review, not independent review.
- Before writing implementation code or creating, editing, updating or deleting project files, either tool must have Chathuranga's explicit permission for the proposed scope. This includes notebooks, scripts, reports, documentation, configuration and generated artifacts; having coding capability or repository access does not grant permission to change them.
- Read-only inspection, analysis, discussion, review and recommendations may proceed without file changes. Permission to review or discuss an idea does not authorize implementation or file changes.
- An explicit request to make a specific change authorizes that change; do not ask for the same permission again. Stay within the approved scope and obtain explicit approval before implementing additional changes. Existing reviewer-driven edit, Git and model-training approval rules still apply separately.
- Claude can independently review both the local repository and the GitHub repository. Prepare review prompts according to the assigned tool's actual access capabilities.
- The active coding tool must help Chathuranga reach the final decision by explaining its own assessment, tradeoffs and any independent reviewer findings. Discuss those findings with Chathuranga; final decisions and approval remain with Chathuranga and must not be replaced by AI agreement.
- The active coding tool must review its own changes. Another tool may provide an independent review when requested or supplied; its availability or agreement is not a prerequisite for assessing the work or continuing already-authorized tasks. Respect any review checkpoint explicitly requested by Chathuranga.
- Prepare a concise review handoff when external reviewer feedback is requested. Do not claim another tool has reviewed work unless its actual feedback is available. Report explicitly requested reviews that are still pending.
- Assess reviewer findings against the current files, requirements and evidence. Do not automatically accept or reject them.
- Before reviewer-driven edits, present a table containing the finding, assessment (agree, partly agree or disagree), evidence and proposed action. Wait for explicit approval before applying the proposed changes. If no changes are needed, say so.

## Git and GitHub

- Never commit or push independently. Run these only when explicitly requested.
- Before starting work, inspect the current branch and working-tree state using read-only Git commands.
- Use a feature-branch workflow for changes after the initial repository setup: create or reuse a task-specific branch, implement and validate the changes, push that branch, and open a pull request targeting `main`. Chathuranga reviews and merges the PR. Do not commit or push task changes directly to `main`.
- Before implementation, provide the branch-creation command if the current branch is `main`; wait for Chathuranga to create or switch to the feature branch. Reuse an existing suitable feature branch.
- When a new branch is needed, provide the exact command, such as `git switch -c <branch-name>`, for Chathuranga to run. Do not create or switch branches independently. Reuse the current branch when it already suits the task.
- Do not stage files, pull, rebase, delete branches, create pull requests, or perform releases without explicit instructions.
- AI tools must not execute Git merges or merge pull requests. Merging is performed by Chathuranga; approval of a change or agreement that it is ready does not authorize an AI tool to merge it.
- Keep virtual environments, secrets and private student information out of Git. Check the proposed file list before suggesting a commit.
- When preparing a pull request (PR) for merge, provide a ready-to-use PR title and description reflecting the actual changes, including the problem addressed, resulting behavior, relevant validation results and material limitations. State the base (`main`) and actual feature head branch. Provide the exact branch, staging, commit and push commands, plus PR creation and merge instructions or commands where appropriate, for Chathuranga to run. Do not execute these merely because the commands were provided. Publishing or updating the PR requires explicit instructions; the merge must be performed by Chathuranga.

## Coursework and implementation

- Read the relevant coursework brief, marking criteria, existing files and applicable instructions before proposing changes. Refer to lecture material where required.
- Preserve original datasets, briefs and lecture notes. Perform cleaning and transformations in code or separate derived files; never silently overwrite source data.
- Use the existing root `.venv` and WSL-native commands. Check dependencies and configuration before installing tools or changing the environment.
- Chathuranga's development environment is Ubuntu under WSL2 (Linux paths and shell, WSL-hosted services such as MySQL). Align commands, instructions and testing with this environment; do not give Windows PowerShell commands unless asked.
- Submitted work must still run for markers on their own computers (Windows, macOS or Linux, with native services). When something that works in the Ubuntu/WSL2 setup could cause a problem on a marker's computer (for example Linux-only commands or paths, WSL-specific host addresses, packages or services installed only in WSL, case-sensitive file names, line endings or software versions that differ from the documented ones), tell Chathuranga explicitly and propose a portable alternative or a documented note. Do not leave such differences silent.
- Prefer the smallest correct change and preserve unrelated work. Avoid unnecessary abstractions and formatting-only changes.
- Organise this standalone project from the repository root: keep the project overview and dependency configuration at the root, notebooks in `notebooks/`, and source datasets plus their data documentation and provenance manifest in `data/`. Add scripts, derived data, figures, reports or tests only when needed, using suitable project-level folders.
- The `COMP1890_Spatial_Data_Science/` folder contains local coursework reference material; implementation files do not need to be stored beside the coursework brief. Preserve original reference files.
- Keep the project independently runnable and packageable using its documented dependencies and supplied inputs. Do not depend on implementation files from other coursework repositories or on machine-specific virtual-environment paths. Change dependency specifications only within an approved scope.
- Make analysis reproducible: document data sources and transformations, use relative project paths and set random seeds where relevant.
- Keep submitted code portable: use `pathlib.Path` with project-relative paths; never hard-code machine-specific absolute paths, drive letters, usernames or virtual-environment locations. `Path` around an absolute path does not make it portable.
- Treat examiners, markers and other readers as users on separate computers. Submitted code and notebooks must run with the supplied inputs and documented dependencies without relying on Chathuranga's local machine, repository location, folder names or environment. Apply this requirement to code, Markdown, comments, configuration, error messages and execution instructions. Describe input locations relative to the submitted files or an explicitly documented working directory, allow configuration where needed, and never require readers to recreate the author's local directory structure.
- Resolve script resources relative to `__file__` where appropriate. For notebooks, document the expected working directory and resolve paths from that location; do not use `__file__`, which is normally unavailable in notebooks. Allow configuration for external data locations when needed.
- Verify required input files exist and give clear errors. Ensure submitted code can run on another machine with the documented dependencies and folder structure, without requiring local lecture notes or ignored files unless explicitly supplied as part of the submission.
- Never invent references, results, screenshots, test outcomes or dataset meanings. State uncertainty and flag contradictory assessment instructions for clarification.
- Follow module-specific AI guidance, citation and declaration requirements. Do not assume AI-generated implementation is permitted for every module. Keep report findings consistent with the executed code.

## Model training execution

- AI tools must not execute predictive model training unless Chathuranga explicitly authorizes the specific training run. The default workflow is for AI tools to prepare and explain the code and commands, and for Chathuranga to run the training manually.
- This restriction applies regardless of dataset size or runtime, including model `fit`, `partial_fit` and training APIs, cross-validation fitting, hyperparameter searches, final refits, and synthetic model-training smoke tests.
- Approval to write code, define configurations, install dependencies, review work or run checks does not authorize model training. Do not infer training permission from general instructions such as “continue” or “move on”.
- Before executing a notebook or test, inspect its execution path for model-training calls. Run only permitted cells or checks; do not bypass this restriction through scratch copies, subprocesses or other AI tools.
- Already-authorized preprocessing calculations, such as fitting training-fold medians and categorical definitions, remain permitted when they do not fit a predictive model. Report training checks as pending until Chathuranga provides results or explicitly authorizes the specific run.

## Data generation, loading and database import

- AI tools write the code (for example loader, import and data-generation scripts) and provide the exact commands. Chathuranga runs them. AI tools must not execute scripts that generate data files, load data or import data into any database, including throwaway containers such as Docker MySQL, unless Chathuranga explicitly authorizes that specific run.
- Approval to write or edit such a script does not authorize running it. Do not infer permission from general instructions such as "continue" or "move on", and do not use scratch copies, subprocesses or other AI tools to bypass this rule.
- Read-only inspection of the original data files remains permitted. Report data generation, loading and import checks as pending until Chathuranga provides the results or explicitly authorizes the specific run.

## Checks and reviews

- Use Ruff for linting, MyPy for type checking and pytest for tests when appropriate to the changed Python code. Check existing configuration first; these tools are not mandatory for every task.
- Run targeted checks after meaningful changes. For notebooks, verify relevant cells, outputs and execution order. Do not add artificial tests or complex tooling for simple document changes.
- Explain the impact and obtain approval before expensive processing or destructive operations. Model training follows the stricter run-specific authorization rules above.
- Review files one at a time: explain purpose, what is correct, meaningful risks and exact recommended changes. Distinguish required fixes from optional improvements.
- Report checks actually run, results and checks still pending. Never describe unverified work as tested or finally approved.

## Communication and documents

- Use coursework task numbers for notebook main headings (for example, `## Task 2: Exploratory Data Analysis`) and sequential task-based numbers for subsections (for example, `### 2.1 Dataset inspection`, `### 2.2 Records and column types`). Keep the notebook title unnumbered. Do not number individual code cells or short findings paragraphs, and do not add unimplemented task sections merely to complete the numbering.
- Structure each notebook step as purpose and method → code → output → findings. Before the code, use a short Markdown cell to explain what will be done, why and how. Place observed results, anomalies and interpretations after the relevant executed output; do not announce findings before showing their evidence, even when preliminary inspection has already identified them.
- Explain the core idea first, using concise, practical language. End conversational responses with a brief Sinhala explanation.
- Use polished professional English for code documentation, reports, Git messages and other professional artifacts unless instructed otherwise.
- Do not assign a role or title to Chathuranga in documents. Prefer neutral or passive wording; when attribution is necessary, use the personal name or an appropriate cited source role.
- After meaningful changes, report status, changes and file paths, checks, pending reviews or decisions, current branch and the best next step. Suggest Git commands and a commit message only when appropriate; do not execute them without authorization.
