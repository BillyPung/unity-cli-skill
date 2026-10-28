import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def read(self, path):
        return json.loads((ROOT / path).read_text(encoding='utf-8'))

    def test_native_entrypoints_reach_shared_skill(self):
        claude = self.read('.claude-plugin/marketplace.json')
        codex = self.read('.agents/plugins/marketplace.json')
        self.assertEqual(claude['name'], codex['name'])
        for source in (claude['plugins'][0]['source'], codex['plugins'][0]['source']['path']):
            plugin = (ROOT / source).resolve()
            self.assertTrue((plugin / 'skills/unity-cli/SKILL.md').is_file())
            self.assertTrue((plugin / 'plugin.json').is_file())

    def test_versions_and_identities_match(self):
        version = (ROOT / 'VERSION').read_text().strip()
        for path in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            manifest = self.read(path)
            self.assertEqual(manifest['name'], 'unity-cli')
            self.assertEqual(manifest['version'], version)
        self.assertEqual(self.read('.claude-plugin/marketplace.json')['plugins'][0]['version'], version)
        skill = (ROOT / 'skills/unity-cli/SKILL.md').read_text(encoding='utf-8')
        self.assertIn(f'version: "{version}"', skill)

    def test_portable_manifest_and_presentation(self):
        manifest = self.read('plugin.json')
        self.assertEqual(manifest['$schema'], 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        self.assertNotIn('skills', manifest)
        interface = manifest['extensions']['com.openai']['interface']
        self.assertLessEqual(len(interface['shortDescription']), 30)
        self.assertEqual(interface, self.read('.codex-plugin/plugin.json')['interface'])

    def test_relative_documentation_links(self):
        for path in ROOT.rglob('*.md'):
            if '.git' in path.parts:
                continue
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' not in link and not link.startswith('#'):
                    self.assertTrue((path.parent / link.split('#')[0]).exists(), (path, link))


if __name__ == '__main__':
    unittest.main()
