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

## License

[Apache 2.0](LICENSE)
