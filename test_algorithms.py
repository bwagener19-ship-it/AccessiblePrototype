import unittest
from data_structures import dijkstra_shortest_path, greedy_assemble_fragments, max_overlap_kmp

class TestAlgorithms(unittest.TestCase):
    def test_dijkstra_simple(self):
        edges = {
            'A': [('B',1),('C',4)],
            'B': [('A',1),('C',2),('D',5)],
            'C': [('A',4),('B',2),('D',1)],
            'D': [('B',5),('C',1)]
        }
        path, dist = dijkstra_shortest_path(edges, 'A', 'D')
        self.assertEqual(dist, 4) 
        self.assertIn('A', path); self.assertIn('D', path)

    def test_max_overlap_and_assembly(self):
        a = "ABCDEF"
        b = "DEFXYZ"
        ol = max_overlap_kmp(a, b)
        self.assertEqual(ol, 3) 
        assembled = greedy_assemble_fragments([a,b])
        self.assertTrue("ABCDEF" in assembled or "DEFXYZ" in assembled or len(assembled) < len(a)+len(b))

if __name__ == '__main__':
    unittest.main()
