import unittest
import main

class MyTestCase(unittest.TestCase):

    # 测试用例1：测试 get_graph() 返回不为空
    def test_get_graph_not_empty(self):
        self.service = main.Service()
        result = self.service.get_graph()
        # 断言：返回结果不是 None
        self.assertIsNotNone(result, "get_graph() 方法返回了空值！")

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

if __name__ == '__main__':
    unittest.main()
