import copy,json,unittest
from pathlib import Path
import backup_chain_audit as m

class Behavior(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((Path(__file__).parent/'example.json').read_text())
    def bad(self):
        with self.assertRaises(m.InputError):m.analyze(self.d)
    def test_unknown_field_rejected(self):
        self.d['unknown']=True;self.bad()

    def test_chain_and_shared_bytes(self):
        r=m.analyze(self.d);self.assertEqual(r['needed_snapshots'],['base','delta']);self.assertEqual(r['needed_bytes'],120);self.assertEqual(r['eligible_delete'],['obsolete'])
    def test_blocked_base(self):
        self.d['delete']=['base'];r=m.analyze(self.d);self.assertEqual(r['blocked_delete'],['base']);self.assertTrue(r['findings'])
    def test_missing_parent_withholds_deletion(self):
        self.d['snapshots'][1]['parent']='lost';r=m.analyze(self.d);self.assertTrue(r['deletion_eligibility_withheld']);self.assertEqual(r['eligible_delete'],[])
    def test_missing_target(self):
        self.d['retain']=['lost'];self.assertEqual(m.analyze(self.d)['findings'][0]['kind'],'missing_snapshot')
    def test_cycle(self):
        self.d['snapshots'][0]['parent']='delta';self.assertEqual(m.analyze(self.d)['findings'][0]['kind'],'cycle')
    def test_unverified_chain(self):
        self.d['snapshots'][0]['verified']=False;self.assertEqual(m.analyze(self.d)['findings'][0]['kind'],'unverified_snapshot')
    def test_shared_ancestor_counted_once(self):
        self.d['retain']=['base','delta'];self.assertEqual(m.analyze(self.d)['needed_bytes'],120)
    def test_input_order_does_not_change_chain(self):
        expected=m.analyze(self.d);self.d['snapshots'].reverse();self.assertEqual(m.analyze(self.d),expected)
    def test_unknown_delete_rejected(self):
        self.d['delete']=['lost'];self.bad()
    def test_duplicate_snapshot_rejected(self):
        self.d['snapshots'].append(self.d['snapshots'][0]);self.bad()
    def test_boolean_bytes_rejected(self):
        self.d['snapshots'][0]['bytes']=True;self.bad()
    def test_duplicate_retain_rejected(self):
        self.d['retain']=['delta','delta'];self.bad()

if __name__ == '__main__':unittest.main()
