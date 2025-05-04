# NEAR Rubric: Category Breakdown

This page provides a friendly, human-readable overview of the NEAR Rubric used for project evaluation. Each category is scored independently, with clear guidelines for what constitutes a high, medium, or low score.

---

## 1. NEAR Protocol Integration (20 pts)
**What it means:**
- How deeply and effectively does the project integrate with NEAR? Are NEAR standards, SDKs, and wallet integrations used in a meaningful way?

**Scoring Guidelines:**
- **16–20:** Deep integration, NEAR standards usage, wallet integration, on-chain innovation
- **10–15:** Moderate NEAR use, partial integrations
- **0–9:** Minimal to no direct integration

**What to look for:**
- **Use of NEAR SDKs (e.g., near-sdk-rs, near-sdk-js)**
  - Good: `use near_sdk::env;` and contract macros like `#[near_bindgen]` are present in Rust code.
  - Bad: No NEAR SDK imports; generic Rust or JS code with no blockchain-specific logic.
- **Smart contract structure and NEAR-specific features**
  - Good: Contract uses NEAR-specific macros, storage, and event standards.
  - Bad: Contract is a simple function with no NEAR-specific logic or structure.
- **Wallet connection and NEAR account management**
  - Good: Frontend uses `near-api-js` to connect to NEAR Wallet and manage accounts.
  - Bad: No wallet integration; users cannot log in with NEAR accounts.
- **Advanced features like cross-contract calls**
  - Good: Contract makes `Promise::new` calls to interact with other contracts.
  - Bad: No cross-contract calls; only local state changes.

---

## 2. Onchain Quality (20 pts)
**What it means:**
- Are the on-chain interactions meaningful and core to the app, or are they superficial?

**Scoring Guidelines:**
- **16–20:** Real, meaningful interactions with NEAR chain verified through code and live usage
- **10–15:** Occasional useful on-chain transactions
- **0–9:** Superficial or junk transactions

**What to look for:**
- **Smart contract functions that perform real, valuable actions**
  - Good: Functions like `deposit`, `stake`, or `transfer` that affect user balances or app state.
  - Bad: Only a `greet` or `set_message` function that stores a string.
- **State changes that matter to users**
  - Good: Contract updates balances, ownership, or other critical state.
  - Bad: State changes are trivial or unused (e.g., incrementing a counter for no reason).
- **Evidence of complex contract calls or logic**
  - Good: Implements multi-step transactions, checks for permissions, or handles callbacks.
  - Bad: Only single-step, trivial logic with no error handling or checks.

---

## 3. Offchain Quality (15 pts)
**What it means:**
- How robust and complex are the off-chain components (frontend, backend, scripts)?

**Scoring Guidelines:**
- **12–15:** Dedicated standalone app, complex architecture, robust back-end integrations
- **7–11:** Browser extension, moderate complexity
- **0–6:** Simple off-chain scripts, minimal complexity

**What to look for:**
- **Use of modern frameworks (React, Node.js, etc.)**
  - Good: Frontend built with React, backend with Express or similar frameworks.
  - Bad: Only a single HTML file or basic script with no framework.
- **Clear separation of frontend/backend**
  - Good: Separate directories for frontend and backend, clear API boundaries.
  - Bad: All code in one file or directory, no separation of concerns.
- **API integrations, state management, build systems**
  - Good: Uses Redux for state, integrates with NEAR RPC, has a build pipeline (Webpack, etc.).
  - Bad: No state management, no API calls, no build process.

---

## 4. Code Quality & Documentation (15 pts)
**What it means:**
- Is the code clean, modular, well-documented, and tested?

**Scoring Guidelines:**
- **12–15:** Clean, modular, tested code; extensive documentation
- **7–11:** Moderate clarity, some tests/docs
- **0–6:** Poorly organized, minimal/no documentation

**What to look for:**
- **Logical file organization, meaningful names**
  - Good: Files and functions are named after their purpose, organized by feature/module.
  - Bad: Files named `file1.js`, functions like `foo()` or `bar()`.
- **Consistent style, clear comments/docstrings**
  - Good: Uses a linter, has docstrings and inline comments explaining logic.
  - Bad: Inconsistent indentation, no comments, unclear code.
- **Presence of tests (unit/integration)**
  - Good: Has a `tests/` directory or test files, uses frameworks like Jest or Cargo test.
  - Bad: No tests at all, or only placeholder test files.
- **Helpful README and architecture docs**
  - Good: README explains setup, usage, and architecture; diagrams or code examples included.
  - Bad: README is missing, empty, or only says "TODO".

---

## 5. Technical Innovation/Uniqueness (15 pts)
**What it means:**
- Does the project introduce new ideas, clever solutions, or unique approaches?

**Scoring Guidelines:**
- **12–15:** Highly novel solution, advances state-of-the-art
- **7–11:** Some innovative elements, derivative model
- **0–6:** Little/no innovation

**What to look for:**
- **Unique algorithms, contract interactions, or architectures**
  - Good: Implements a new DeFi primitive, novel NFT mechanism, or unique governance logic.
  - Bad: Forks an existing contract with minimal changes.
- **Solutions to previously unsolved problems**
  - Good: Addresses a known pain point in NEAR ecosystem with a new approach.
  - Bad: Solves a problem already addressed by many other projects, or doesn't solve a real problem.
- **Creative combinations of existing technologies**
  - Good: Integrates NEAR with other blockchains or off-chain services in a new way.
  - Bad: Only uses standard NEAR features with no new combinations.

---

## 6. Team Activity & Project Maturity (10 pts)
**What it means:**
- Is the project actively maintained and mature?

**Scoring Guidelines:**
- **8–10:** Active commits, ongoing development, clear roadmap
- **4–7:** Occasional updates, partial roadmap
- **0–3:** Dormant project, unclear future

**What to look for:**
- **Recent commits, versioning, TODOs being addressed**
  - Good: Commits within the last month, version tags, TODOs marked as done.
  - Bad: Last commit was over a year ago, TODOs never resolved.
- **Roadmap or future plans in docs**
  - Good: README or docs include a roadmap, milestones, or future features.
  - Bad: No mention of future plans, or roadmap is outdated.
- **Evidence of ongoing development**
  - Good: Issues and PRs are regularly opened and closed, active discussions.
  - Bad: No recent activity, issues left unanswered.

---

## 7. Grant Impact & Ecosystem Fit (5 pts)
**What it means:**
- How well does the project align with NEAR's goals and ecosystem needs?

**Scoring Guidelines:**
- **4–5:** Strong ecosystem alignment, clear beneficial impact
- **2–3:** Moderate alignment, niche impact
- **0–1:** Weak fit, unclear impact

**What to look for:**
- **Project addresses a real need in NEAR**
  - Good: Fills a gap in DeFi, NFTs, or developer tooling for NEAR.
  - Bad: Project is generic, could run on any chain, or doesn't address a NEAR-specific need.
- **Integrates with or enhances NEAR ecosystem**
  - Good: Works with other NEAR projects, standards, or infrastructure.
  - Bad: No integration with NEAR ecosystem, stands alone.
- **Clear value proposition for NEAR users or developers**
  - Good: Docs explain how NEAR users benefit, or how devs can build on top.
  - Bad: No explanation of value for NEAR community.

---

**For more details, see the rubric JSON or contact the maintainers.** 