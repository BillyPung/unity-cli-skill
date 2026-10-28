#!/usr/bin/env python3
"""Copy the portable skill into a client's discovery path; preserve old copies."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / 'skills' / 'unity-cli'


def destination(client, project=None):
    home = Path.home()
    if project:
        base = Path(project).expanduser().resolve()
        paths = {'generic': '.agents/skills', 'codex': '.agents/skills',
                 'claude': '.claude/skills', 'opencode': '.opencode/skills',
                 'omp': '.omp/skills', 'codex-legacy': '.codex/skills'}
        return base / paths[client] / 'unity-cli'
    paths = {
        'generic': home / '.agents/skills',
        'codex': home / '.agents/skills',
        'claude': Path(os.environ.get('CLAUDE_CONFIG_DIR', str(home / '.claude'))) / 'skills',
        'opencode': Path(os.environ.get('XDG_CONFIG_HOME', str(home / '.config'))) / 'opencode/skills',
        'omp': home / '.omp/agent/skills',
        'codex-legacy': Path(os.environ.get('CODEX_HOME', str(home / '.codex'))) / 'skills',
    }
    return paths[client] / 'unity-cli'


def check_target(target):
    target = Path(os.path.abspath(target.expanduser()))
    if target.name != 'unity-cli':
        raise ValueError('Destination must end in unity-cli (the skill folder, not its parent).')
    for part in (target, *target.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError(f'Refusing linked destination component: {part}')
    resolved = target.resolve()
    if resolved == REPO or REPO in resolved.parents or resolved in SOURCE.parents:
        raise ValueError('Destination overlaps the source repository.')
    if target.exists() and not target.is_dir():
        raise ValueError('Destination exists and is not a directory.')
    return target


def revision():
    try:
        return subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'],
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def install(target, dry_run=False):
    target = check_target(target)
    if not (SOURCE / 'SKILL.md').is_file():
        raise ValueError('Missing source SKILL.md; run from a complete repository checkout.')
    backup = None
    if target.exists():
        backup = target.parent.parent / '.unity-cli-backups' / (
            datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8])
        for part in (backup.parent, *backup.parent.parents):
            if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
                raise ValueError('Refusing linked backup directory.')
    if dry_run:
        print(f'Would install {target}' + (f' (backup: {backup})' if backup else ''))
        return target, backup
    target.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.unity-cli-stage-', dir=target.parent))
    moved = False
    try:
        shutil.copytree(SOURCE, stage, dirs_exist_ok=True)
        (stage / '.unity-cli-install.json').write_text(json.dumps({
            'version': (REPO / 'VERSION').read_text().strip(), 'commit': revision(),
            'source': 'https://github.com/BillyPung/unity-cli-skill',
        }, indent=2) + '\n', encoding='utf-8')
        if backup:
            backup.parent.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
            moved = True
        try:
            stage.rename(target)
        except OSError:
            if moved:
                backup.rename(target)
            raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    print(f'Installed {target}')
    if backup:
        print(f'Previous copy preserved at {backup}')
    return target, backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client', choices=['generic', 'codex', 'codex-legacy', 'claude', 'opencode', 'omp'])
    parser.add_argument('--project', type=Path, help='Install into this project instead of the user directory')
    parser.add_argument('--destination', type=Path, help='Exact custom skill directory, ending in unity-cli')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if bool(args.client) == bool(args.destination):
        parser.error('Choose exactly one of --client or --destination.')
    if args.destination and args.project:
        parser.error('--project cannot be combined with --destination.')
    try:
        target = args.destination if args.destination else destination(args.client, args.project)
        install(target, args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Install failed: {error}\n')


if __name__ == '__main__':
    main()
