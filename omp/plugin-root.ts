import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";

// Every skill, agent and doc in this plugin calls the bundled Python runtime as
// "$CLAUDE_PLUGIN_ROOT/scripts/claude-seo". omp never expands that token in
// prose, but the bash tool inherits this process environment, so exporting it
// once keeps all existing instructions working without rewriting them.
const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

export default function pluginRootEnv(_pi: ExtensionAPI): void {
  process.env.CLAUDE_PLUGIN_ROOT ??= pluginRoot;
  process.env.OMP_PLUGIN_ROOT ??= pluginRoot;
}
