import math
import unittest
from raven.disclosure import disclosure_probability
from raven.probabilities import sigmoid,features
from tests.test_constraints import pair

class Probabilities(unittest.TestCase):
    def test_finite(self):
        for x in (-1e300,-100,0,100,1e300):
            p=sigmoid(x);self.assertTrue(math.isfinite(p));self.assertGreater(p,0);self.assertLess(p,1)
    def test_disclosure(self):
        a,b=pair();a['fields']['schedule']=None;a['field_status']['schedule']='declined'
        self.assertEqual(disclosure_probability(a,'constraints'),0)
        a['field_status']['schedule']='not_asked';self.assertEqual(disclosure_probability(a,'constraints'),1)
    def test_no_identity_or_future_features(self):
        a,b=pair();x=features(a,b)
        a.update(member_id='unrelated',truth={'secret':123},exit_day=99,response_rate=.1)
        self.assertEqual(x,features(a,b))
    def test_missingness_not_zero_or_decline(self):
        a,b=pair();a['fields']['relationship_goal']=None;b['fields']['relationship_goal']=None
        x=features(a,b);a['fields']['relationship_goal']='long_term';b['fields']['relationship_goal']='long_term'
        self.assertNotEqual(x,features(a,b))
