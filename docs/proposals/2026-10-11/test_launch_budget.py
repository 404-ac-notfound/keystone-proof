"""Offline launch boundary tests; no account reads or provider execution."""
import copy
import datetime as dt
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import yaml
from test_managed_controller import fixture, m, NOW, ROOT, FakeAPI


class LaunchBudget(unittest.TestCase):
    def test_workflow_caps_match_budget_and_preserve_template(self):
        jobs = yaml.load((ROOT.parents[2] / '.github/workflows/k14-managed.yml').read_text(), Loader=yaml.BaseLoader)['jobs']
        self.assertEqual(sum(int(j['timeout-minutes']) for j in jobs.values()), 73)
        self.assertEqual(m.LAUNCH_BUDGET_MINUTES, 73 + 10 + 15)
        self.assertEqual(m.POLL_SECONDS, 720)
        for name in ('author', 'revise'):
            self.assertEqual(int(jobs[name]['timeout-minutes']), 8)
        for name in ('verify1', 'verify2'):
            self.assertEqual(int(jobs[name]['timeout-minutes']), 14)

    def test_exact_98_minutes_allowed_one_second_less_rejected(self):
        c, e = fixture()
        edge = NOW + dt.timedelta(minutes=22)
        m.launch_budget(c, e, edge)
        with self.assertRaisesRegex(m.Stop, '98 minutes'):
            m.launch_budget(c, e, edge + dt.timedelta(seconds=1))

    def test_each_use_bound_can_stop_launch(self):
        c, e = fixture()
        for key in ('author_credential', 'request_credential'):
            changed = copy.deepcopy(c)
            changed[key]['use_until'] = (NOW + dt.timedelta(minutes=97)).isoformat().replace('+00:00', 'Z')
            with self.subTest(key=key), self.assertRaises(m.Stop):
                m.launch_budget(changed, e, NOW)
        changed = dict(e, K14_CASH_CHECKED_AT=(NOW-dt.timedelta(minutes=23)).isoformat().replace('+00:00','Z'))
        with self.assertRaises(m.Stop):
            m.launch_budget(c, changed, NOW)

    def test_configuration_evidence_oldest_check_limits_budget(self):
        from test_configuration_admission import admitted_fixture, NOW as admission_now
        c, e = admitted_fixture()
        m.launch_budget(c, e, admission_now)
        for key in ('repo_review_configuration', 'owner_app_installation_scope'):
            changed = copy.deepcopy(c)
            changed['configuration_admission'][key]['checked_at'] = (admission_now-dt.timedelta(minutes=23)).isoformat().replace('+00:00','Z')
            with self.subTest(key=key), self.assertRaises(m.Stop):
                m.launch_budget(changed, e, admission_now)

    def test_budget_is_rechecked_after_review_reads_before_claim_write(self):
        c, e = fixture()
        api = FakeAPI()
        # gates then budget, repeated after isolation GETs.
        clock = iter([NOW, NOW, NOW+dt.timedelta(minutes=23), NOW+dt.timedelta(minutes=23)])
        with tempfile.TemporaryDirectory() as temp:
            event = Path(temp)/'event.json'
            event.write_text(json.dumps({'action':'labeled','label':{'name':'ready'},
                'sender':{'login':c['launch_login']},'issue':{'number':c['seed_issue']}}))
            with patch.dict(os.environ, {**e,'GITHUB_EVENT_PATH':str(event)}), patch.object(m,'api',api), patch.object(m,'now_utc',side_effect=lambda:next(clock)):
                with self.assertRaisesRegex(m.Stop, '98 minutes'):
                    m.guard(c)
            self.assertEqual(len(api.calls), 2)
            self.assertTrue(all(call[1]=='GET' for call in api.calls))
            self.assertEqual(api.refs,{})
