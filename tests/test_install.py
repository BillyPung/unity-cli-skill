import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_install_update_and_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'path with spaces' / 'skills' / 'unity-cli'
            installer.install(target)
            self.assertTrue((target / 'references/pipeline-package.md').is_file())
            metadata = json.loads((target / '.unity-cli-install.json').read_text())
            self.assertEqual(metadata['version'], (installer.REPO / 'VERSION').read_text().strip())
            (target / 'local-customization.txt').write_text('preserve me')
            _, backup = installer.install(target)
            self.assertEqual((backup / 'local-customization.txt').read_text(), 'preserve me')
            self.assertFalse((target / 'local-customization.txt').exists())
            self.assertTrue((target / 'SKILL.md').is_file())

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'skills/unity-cli'
            installer.install(target, dry_run=True)
            self.assertFalse(target.parent.exists())

    def test_failed_replacement_restores_old_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'skills/unity-cli'
            installer.install(target)
            (target / 'local.txt').write_text('keep')
            original_rename = Path.rename
            def rename(path, to):
                if path.name.startswith('.unity-cli-stage-'):
                    raise OSError('simulated replacement failure')
                return original_rename(path, to)
            with mock.patch.object(Path, 'rename', rename):
                with self.assertRaises(OSError):
                    installer.install(target)
            self.assertEqual((target / 'local.txt').read_text(), 'keep')

    def test_source_and_wrong_folder_refused(self):
        with self.assertRaises(ValueError):
            installer.install(installer.SOURCE)
        with self.assertRaises(ValueError):
            installer.install(Path(tempfile.gettempdir()) / 'skills')

    def test_project_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            for client, folder in [('codex', '.agents'), ('claude', '.claude'),
                                   ('opencode', '.opencode'), ('omp', '.omp')]:
                self.assertEqual(installer.destination(client, tmp),
                                 Path(tmp).resolve() / folder / 'skills/unity-cli')

    def test_symlink_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            actual = base / 'actual'
            actual.mkdir()
            link = base / 'linked'
            try:
                link.symlink_to(actual, target_is_directory=True)
            except OSError:
                self.skipTest('Symlink creation unavailable for this Windows account')
            with self.assertRaises(ValueError):
                installer.install(link / 'unity-cli')


if __name__ == '__main__':
    unittest.main()
