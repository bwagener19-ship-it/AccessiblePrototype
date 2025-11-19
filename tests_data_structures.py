import unittest
from data_structures import Stack, Queue, HashTable, PriorityQueue, BinarySearchTree, Graph, kmp_search

class TestDataStructures(unittest.TestCase):
    def test_stack(self):
        s = Stack()
        s.push(1); s.push(2)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.peek(), 1)

    def test_queue(self):
        q = Queue()
        q.enqueue('x'); q.enqueue('y')
        self.assertEqual(q.dequeue(), 'x')
        self.assertFalse(q.is_empty() == True)

    def test_hashtable(self):
        ht = HashTable()
        ht.set('k','v')
        self.assertEqual(ht.get('k'),'v')
        ht.remove = getattr(ht, 'remove', None) 

    def test_priority_queue(self):
        pq = PriorityQueue()
        pq.push(10,'low'); pq.push(1,'high')
        self.assertEqual(pq.pop(),'high')

    def test_bst(self):
        bst = BinarySearchTree()
        bst.insert(10,'ten'); bst.insert(5,'five'); bst.insert(15,'fifteen')
        self.assertEqual(bst.search(5),'five')
        self.assertIsNotNone(bst.inorder())

    def test_graph_dijkstra(self):
        g = Graph()
        g.add_edge('s','a',1); g.add_edge('a','t',2); g.add_edge('s','t',10)
        path, dist = g.shortest_path('s','t')
        self.assertEqual(dist, 3)
        self.assertEqual(path, ['s','a','t'])

    def test_kmp(self):
        text = "abxabcabcaby"
        self.assertEqual(kmp_search(text, "abcaby"), 6)

if __name__ == '__main__':
    unittest.main()
