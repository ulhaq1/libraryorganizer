import unittest, json
from unittest.mock import patch, mock_open
from library_model import add_book, delete_book_by_title, load_book, save_books
def _joined(mo): return "".join(c.args[0] for c in mo.return_value.write.call_args_list)
class TestLibraryModel(unittest.TestCase):
    @patch("builtins.open",new_callable=mock_open,read_data="[]")
    def test_add(self,mo):
        add_book("Test","Auth",2021,"available")
        obj=json.loads(_joined(mo)); self.assertEqual(obj[0]["title"],"Test")
    @patch("builtins.open",new_callable=mock_open,read_data='[{"title":"Test","author":"A","year":2021,"status":"available"}]')
    def test_load(self,mo):
        books=load_book(); self.assertEqual(books[0]["title"],"Test")
    @patch("builtins.open",new_callable=mock_open,read_data='[{"title":"Test","author":"A","year":2021,"status":"available"}]')
    def test_delete(self,mo):
        delete_book_by_title("Test"); obj=json.loads(_joined(mo)); self.assertEqual(obj[0]["status"],"deleted")
    @patch("builtins.open",new_callable=mock_open)
    def test_save(self,mo):
        save_books([{"title":"X","author":"Y","year":2000,"status":"available"}])
        obj=json.loads(_joined(mo)); self.assertEqual(obj[0]["title"],"X")
if __name__=="__main__": unittest.main()
