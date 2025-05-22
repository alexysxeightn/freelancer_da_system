import unittest
from database import load_dataset_into_sqlite
from llm_utils import generate_sql_query, generate_human_answer
from schema import schema_description


class TestFreelancerAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, cls.df = load_dataset_into_sqlite("freelancer_earnings_bd.csv")
        cls.sample_data = cls.df.head()

    def test_generate_sql(self):
        question = "Какой средний доход у фрилансеров из Европы?"
        sql = generate_sql_query(question, schema_description, self.sample_data)
        self.assertIn("SELECT", sql.upper())

    def test_generate_answer(self):
        question = "Какой средний доход у фрилансеров из Европы?"
        answer = generate_human_answer(question, 45000)
        self.assertTrue(len(answer) > 10)

    def test_sql_cleaning(self):
        from llm_utils import clean_sql_query

        dirty = "```sql SELECT * FROM freelancers; ```"
        clean = clean_sql_query(dirty)
        self.assertNotIn("```", clean)


if __name__ == "__main__":
    unittest.main()
