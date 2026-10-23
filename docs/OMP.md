# Running claude-seo on omp

omp reads this repository as a native plugin. Nothing has to be rewritten per
install: the marketplace catalog, the skill layout, the agents, and the bundled
Python runtime all work as-is.

## Install

### Plugin (recommended)

```bash
omp plugin marketplace add AgriciDaniel/claude-seo
omp plugin install claude-seo@agricidaniel-claude-seo
/skill:seo setup      # builds the isolated Python runtime + headless browser
```

`omp plugin install` copies the plugin into `~/.omp/plugins/cache/` and enables
its `package.json` extension, `skills/`, `commands/`, and `agents/`.

### Point omp at a checkout

```bash
git clone https://github.com/AgriciDaniel/claude-seo.git
cd claude-seo
omp                   # .omp/config.yml adds ./skills to skills.customDirectories
./scripts/claude-seo setup
```

Without a plugin install, `/seo` (from `commands/seo.md`) is not discovered;
use `/skill:seo`, or run the launcher directly.

## What maps to what

| Claude Code | omp |
|---|---|
| `skills/<name>/SKILL.md` | Same layout, discovered one level under `skills/` |
| `/seo <command>` | `commands/seo.md`, `$ARGUMENTS` = `<command> <url>`; `/skill:seo` also works |
| `agents/*.md` | Same files, discovered from the plugin root |
| `${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo` | Exported as an environment variable by `omp/plugin-root.ts` |
| `${CLAUDE_PLUGIN_ROOT}/skills/...` (Read paths) | `skill://<skill>/<path>` |
| `hooks/hooks.json` | Not loaded (Claude Code hook format) |

## Path rules

omp's Read tool does not expand environment variables, so a
`${CLAUDE_PLUGIN_ROOT}/skills/...` path passed to `read` fails. Cross-skill
references therefore use omp's URL scheme:

```text
skill://seo/references/cwv-thresholds.md
skill://seo-agentic/references/vendor-matrix.md
```

Bash commands are different: the bash tool inherits the process environment, so
the canonical launcher form still works verbatim everywhere, including inside
task subagents:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run pagespeed_check.py https://example.com --json
```

`omp/plugin-root.ts` sets `CLAUDE_PLUGIN_ROOT` (and `OMP_PLUGIN_ROOT`) to the
installed plugin root at startup. If you run the skills from a checkout without
the extension, export it yourself:

```bash
export CLAUDE_PLUGIN_ROOT=/path/to/claude-seo
```

## Slash command

`commands/seo.md` takes the rest of the line as `$ARGUMENTS` and hands it to the
`seo` skill:

```text
/seo audit https://example.com
/seo schema https://example.com
```

## Known gaps

- `hooks/hooks.json` (Claude Code `PostToolUse` format) is not loaded. The
  JSON-LD validator it runs is still available as
  `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run ...` and through `/seo schema`.
- `extensions/*/install.sh` targets a Claude Code install tree. Installing an
  optional MCP extension for omp means copying its `skills/` directory into
  `skills.customDirectories` or a plugin of your own.
- `model: sonnet` in agent frontmatter is ignored for Claude-format plugins, so
  subagents run on the session model.

## Verify

```bash
omp skill list | grep '^seo'                   # 26 skills
omp read skill://seo/references/cwv-thresholds.md
omp -e ./omp/plugin-root.ts -p 'Run bash: echo $CLAUDE_PLUGIN_ROOT'
```
