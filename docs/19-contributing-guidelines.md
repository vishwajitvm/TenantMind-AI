# 19. Contributing Guidelines

We welcome contributions to TenantMind AI. Follow these procedures to submit code changes.

## 1. Branch Strategy & Standards
* **`main`**: Production branch. Requires sign-off from administrators.
* **`develop`**: Primary staging and integration branch. All PRs should be submitted here.
* **Feature Branches**: Named `feature/<name>` or `bugfix/<name>`.

---

## 2. Development Process
1. Fork the repo and checkout a new branch from `develop`.
2. Configure your local environment and verify all tests pass.
3. Code styling rules:
   * **Python**: Strict conformance to **PEP 8**, formatted with `black` and checked with `flake8`.
   * **TypeScript/React**: Linted using `eslint` and formatted with `prettier`.

---

## 3. Pull Request Checklist
Before requesting review:
* [ ] Verify that all unit and integration tests run successfully.
* [ ] Include new test coverages for any added features or endpoint logic.
* [ ] Update relevant documentation manuals or features registries.
* [ ] Ensure commit messages follow the Conventional Commits format (e.g. `feat: add Stripe payment gateway integration`).
