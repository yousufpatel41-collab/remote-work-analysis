import re
import sqlite3
import subprocess
import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


class SimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT/'src/generate_data.py')], check=True, capture_output=True)
        cls.frame = pd.read_csv(ROOT/'data/synthetic_workforce_data.csv')

    def test_country_coverage_and_unique_ids(self):
        self.assertEqual(self.frame.groupby('country').size().to_dict(),
                         {'Germany':800,'Hungary':400,'India':300,'Poland':500})
        self.assertTrue(self.frame.employee_id.is_unique)
        self.assertTrue(self.frame[['productivity_score','satisfaction_score']].apply(lambda s:s.between(1,10).all()).all())

    def test_gross_cost_assumptions_by_work_mode(self):
        office_cost=self.frame.country.map({'Germany':12000,'Poland':7000,'Hungary':6500,'India':3500})
        factor=self.frame.work_mode.map({'Fully Remote':1,'Hybrid':.5,'In-Office':0})
        pd.testing.assert_series_equal(self.frame.annual_office_cost_saving_eur, office_cost*factor, check_names=False)

    def test_sql_queries_execute_and_reconcile_headcounts(self):
        with sqlite3.connect(':memory:') as db:
            self.frame.to_sql('workforce',db,index=False)
            sql=re.sub(r'--[^\n]*','',(ROOT/'src/sql_queries.sql').read_text(encoding='utf-8'))
            queries=[q.strip() for q in sql.split(';') if q.strip()]
            self.assertEqual(len(queries),7)
            tables=[pd.read_sql_query(q,db) for q in queries]
        self.assertEqual(int(tables[0].employee_count.sum()),2000)
        self.assertEqual(int(tables[2].employees.sum()),2000)
        for country,group in tables[0].groupby('country'):
            self.assertAlmostEqual(group.pct_of_country.sum(),100,delta=.02)


if __name__=='__main__': unittest.main()
