# `action-post-clang-tidy-results`

> Downloads clang-tidy YAML artifacts, posts inline PR comments, and posts a summary comment.

## Usage

```yaml
- uses: Framework-R-D/action-post-clang-tidy-results@81c1a8f0b9125c701c8535fb63a05b8fdb6d968e # v2
  with:
    input-name: value
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `build-path` | Path where build artifacts are located | true | `` |
| `pr-number` | PR number for posting comments | false | `` |
| `post-summary` | Whether to post a summary comment (true/false) | false | `false` |

## Outputs

| Name | Description |
|------|-------------|
| `has_content` | Whether any clang-tidy artifacts with reportable content were found |

## Report containment

Reports are downloaded only from the `clang-tidy-check` artifact in the current repository and workflow run, into a fresh runner-temporary directory. The legacy `build-path` input remains accepted but no longer controls report extraction or consumption; report files cannot overwrite workspace scripts or workflow tooling. Failed downloads are not consumed. Expected report files must be regular files no larger than 2 MB, and PR numbers must be positive integers. Reports are data for comments, not authorization to apply replacements.

Cross-run artifact selection, source-SHA approval, and producer-workflow verification belong to the caller and are not provided by this action. Do not use this comment action to select fixes for privileged application. The pinned inline-comment dependency's open-ended requirements are constrained by the exact direct/transitive versions in this action's `.github/comment-tools/requirements.txt`, consumed through `PIP_CONSTRAINT` and maintained by pip Dependabot updates. Only wheels are permitted, user pip configuration is disabled, and the existing runner Python avoids the dependency's mutable nested `actions/setup-python@v5` step. The upstream installer does not expose a requirements override suitable for pip's hash-checking mode; adding end-to-end wheel hash enforcement requires an upstream installation-interface change or replacement, not a claim that version constraints provide integrity hashes.

## License

[Apache 2.0](LICENSE)
