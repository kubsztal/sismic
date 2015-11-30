import unittest
from pyss import load


class ToDictTests(unittest.TestCase):
    def test_simple(self):
        load.from_yaml(open('../examples/simple.yaml')).to_dict()

    def test_composite(self):
        load.from_yaml(open('../examples/composite.yaml')).to_dict()

    def test_history(self):
        load.from_yaml(open('../examples/history.yaml')).to_dict()

    def test_actions(self):
        load.from_yaml(open('../examples/actions.yaml')).to_dict()


class TraversalTests(unittest.TestCase):
    def setUp(self):
        self.sm = load.from_yaml(open('../examples/composite.yaml'))

    def test_ancestors(self):
        self.assertEqual(self.sm.ancestors_for('s2'), [])
        self.assertEqual(self.sm.ancestors_for('s1a'), ['s1'])
        self.assertEqual(self.sm.ancestors_for('s1b1'), ['s1b', 's1'])

    def test_descendants(self):
        self.assertEqual(self.sm.descendants_for('s2'), [])
        s1 = self.sm.descendants_for('s1')
        self.assertTrue('s1a' in s1)
        self.assertTrue('s1b' in s1)
        self.assertTrue('s1b1' in s1)
        self.assertTrue('s1b2' in s1)
        self.assertTrue(len(s1) == 4)

    def test_depth(self):
        self.assertEqual(self.sm.depth_of(None), 0)
        self.assertEqual(self.sm.depth_of('s1'), 1)
        self.assertEqual(self.sm.depth_of('s1a'), 2)
        self.assertEqual(self.sm.depth_of('s1b1'), 3)
        self.assertEqual(self.sm.depth_of('s2'), 1)
        self.assertEqual(self.sm.depth_of('s1b2'), 3)

    def test_lca(self):
        self.assertEqual(self.sm.least_common_ancestor('s1', 's2'), None)
        self.assertEqual(self.sm.least_common_ancestor('s1', 's1a'), None)
        self.assertEqual(self.sm.least_common_ancestor('s1a', 's1b'), 's1')
        self.assertEqual(self.sm.least_common_ancestor('s1a', 's1b1'), 's1')