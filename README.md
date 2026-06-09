# `action-post-clang-tidy-results`

> Downloads clang-tidy YAML artifacts, posts inline PR comments, and posts a summary comment.

## Usage

```yaml
- uses: Framework-R-D/action-post-clang-tidy-results@ebe244ff1f0460b5175b6c9ef17da05164b71b29 # v1
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

## License

[Apache 2.0](LICENSE)
