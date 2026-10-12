"""Offline installed-workflow boundaries; no workflow event or provider invocation."""
import copy
from pathlib import Path
import unittest
import yaml
from test_managed_controller import fixture, m, NOW

ROOT = Path(__file__).resolve().parent


class Installation(unittest.TestCase):
    def test_installed_permissions_pins_and_dependencies_match_reviewed_template(self):
        source = yaml.load((ROOT / 'k14-managed.yml.disabled').read_text(), Loader=yaml.BaseLoader)
        target = yaml.load((ROOT.parents[2] / '.github/workflows/k14-managed.yml').read_text(), Loader=yaml.BaseLoader)
        self.assertEqual(target['name'], 'k14-managed')
        self.assertEqual(target['on'], source['on'])
        self.assertEqual(target['permissions'], {})
        self.assertEqual(target['env'], source['env'])
        self.assertEqual(target['concurrency'], source['concurrency'])
        normal = copy.deepcopy(target)
        normal['name'] = source['name']
        normal['jobs']['guard']['needs'] = []
        for name in ('guard', 'receipt'):
            self.assertIn("vars.K14_ENABLED == 'true'", target['jobs'][name]['if'])
            normal['jobs'][name]['if'] = source['jobs'][name]['if']
        self.assertEqual(normal, source)
        self.assertNotIn('needs', target['jobs']['guard'])

    def test_wrong_request_or_launch_identity_stops_before_api(self):
        from unittest.mock import patch
        c, e = fixture()
        for field in ('request_login', 'launch_login'):
            for value in ('typo', 'Magic', '404-AC-NOTFOUND', '', None):
                broken = copy.deepcopy(c); broken[field] = value
                with self.subTest(field=field, value=value), patch.object(m, 'api') as api, self.assertRaises(m.Stop):
                    m.gates(broken, e, NOW)
                api.assert_not_called()
