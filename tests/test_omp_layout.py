"""omp surfaces must stay consistent with the Claude Code plugin manifest."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))


def test_omp_catalog_ships_the_plugin_as_the_repo_root():
    catalog = json.loads((ROOT / ".omp-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert catalog["owner"]["name"], "omp marketplace needs owner.name"
    entries = {entry["name"]: entry for entry in catalog["plugins"]}
    assert PLUGIN["name"] in entries, "catalog must list the plugin.json name"
    assert entries[PLUGIN["name"]]["source"] == "./"


def test_package_json_version_matches_plugin_json():
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert package["version"] == PLUGIN["version"]


def test_package_json_extension_entries_exist():
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    entries = package["omp"]["extensions"]
    assert entries, "the plugin-root extension is what exports CLAUDE_PLUGIN_ROOT"
    for entry in entries:
        assert (ROOT / entry.removeprefix("./")).is_file(), entry


def test_project_config_registers_the_skills_directory():
    config = (ROOT / ".omp" / "config.yml").read_text(encoding="utf-8")
    assert "customDirectories" in config
    assert "./skills" in config


def test_seo_slash_command_exists():
    command = (ROOT / "commands" / "seo.md").read_text(encoding="utf-8")
    assert "$ARGUMENTS" in command


def test_skill_and_agent_docs_do_not_use_unexpandable_env_paths():
    """omp's Read tool never expands ${CLAUDE_PLUGIN_ROOT}; use skill:// instead."""
    offenders = []
    docs = [*ROOT.glob("agents/*.md"), *ROOT.glob("skills/**/*.md")]
    for path in docs:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "${CLAUDE_PLUGIN_ROOT}/skills/" in line:
                offenders.append(f"{path.relative_to(ROOT)}:{line_no}")
    assert not offenders, "use skill://<skill>/<path> in: " + ", ".join(offenders)
