import unittest
from experiments.run_calibration import metrics

class CalibrationBins(unittest.TestCase):
    def test_constant_predictions_share_one_bin(self):
        rows=[{'p':.2,'y':int(i<20)} for i in range(100)]
        result=metrics(rows)
        self.assertEqual(len(result['bins']),1)
        self.assertAlmostEqual(result['ece'],0)
    def test_tied_probability_order_invariance(self):
        rows=[{'p':.1,'y':i%2} for i in range(30)]+[{'p':.4,'y':int(i<3)} for i in range(30)]
        self.assertEqual(metrics(rows),metrics(list(reversed(rows))))
