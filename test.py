import unittest
from script import process_lines


class TestProcessLines(unittest.TestCase):
    def test_simple(self):
        test_case = ['Booker T., Washington, 87360, 373 781 7380, yellow',
                        'Chandler, Kerri, (623)-668-9293, pink, 123123121',
                        'James Murphy, yellow, 83880, 018 154 6474',
                        'asdfawefawea'
                        ]
        expected = dict()
        expected['entries'] = list()
        expected['errors'] = [1, 3]
        item2 = {
            "color": "yellow",
            "firstname": "Booker T.",
            "lastname": "Washington",
            "phonenumber": "373-781-7380",
            "zipcode": "87360"
        }
        expected['entries'].append(item2)
        item1 = {
            "color": "yellow",
            "firstname": "James",
            "lastname": "Murphy",
            "phonenumber": "018-154-6474",
            "zipcode": "83880"
        }
        expected['entries'].append(item1)
        self.assertEqual(process_lines(test_case), expected)


if __name__ == '__main__':
    unittest.main()
