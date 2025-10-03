import unittest
from unittest.mock import patch
from library_main import add_book_gui, delete_book_gui, lend_book_gui
class TestIntegration(unittest.TestCase):
    @patch("library_model.add_book"); @patch("library_main.display_books")
    def test_add(self,md,ma): add_book_gui("T","A","2021","available"); ma.assert_called(); md.assert_called()
    @patch("library_model.delete_book_by_title"); @patch("library_main.display_books")
    def test_del(self,md,mdel): delete_book_gui("T"); mdel.assert_called(); md.assert_called()
    @patch("library_model.save_books"); @patch("library_model.load_book",return_value=[{"title":"T","status":"available"}]); @patch("library_main.display_books")
    def test_lend(self,md,ml,ms): lend_book_gui("T"); ms.assert_called(); md.assert_called()
if __name__=="__main__": unittest.main()
