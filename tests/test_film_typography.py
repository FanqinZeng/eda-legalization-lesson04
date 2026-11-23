import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from film_common import Film

class Typography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.film=Film(ROOT,'zh')
    def test_explicit_paragraph_breaks_preserve_all_visible_characters(self):
        text='一个候选，只访问一次。\n先合并横腿和竖腿中的重复格子。'
        lines=self.film.wrap(text,36,790,'zh')
        self.assertEqual(''.join(lines),text.replace('\n',''))
        self.assertTrue(all('\n' not in line for line in lines))
    def test_grid_numbers_fit_narrow_cells_including_repeating_fractions(self):
        for value in ['0.4375','≈0.1667','1.125']:
            size=self.film.fit_size(value,92,28,mono=True)
            self.assertLessEqual(self.film.font(size,True).getlength(value),92)
if __name__=='__main__':unittest.main()
