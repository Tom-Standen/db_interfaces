import pytest
from unittest.mock import MagicMock, patch
from db_interfaces.FirestoreInterface import FirestoreInterface


class MockDocumentSnapshot:
    """
    It seems like the mocking in the test isn't fully matching the behavior of the real Firestore client. In the real Firestore client, stream() returns a list of Firestore DocumentSnapshot objects. These DocumentSnapshot objects have a to_dict() method, which returns a dictionary representation of the Firestore document.

    However, in your test, you're setting stream() to return a list of plain Python dictionaries. When the select() method attempts to call to_dict() on these dictionaries, it raises an AttributeError, because Python dictionaries don't have a to_dict() method.

    What you need to do is make the mock object act more like the real Firestore DocumentSnapshot. You can do that by adding a to_dict() method to the objects that your mock stream() is returning.
    """
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return self._data


@patch('db_interfaces.FirestoreInterface.firestore.Client')
def test_select(mock_client):
    interface = FirestoreInterface()
    mock_collection = MagicMock()
    mock_client.return_value.collection.return_value = mock_collection
    # We wrap the dictionaries with MockDocumentSnapshot
    mock_collection.where.return_value.stream.return_value = [
        MockDocumentSnapshot({'field1': 'value1', 'field2': 'value2'})
    ]
    model = interface.SelectModel(collection_id='test', filters={'field1': 'value1'})
    result = interface.select(model)
    assert result == [{'field1': 'value1', 'field2': 'value2'}]

@patch('db_interfaces.FirestoreInterface.firestore.Client')
def test_insert(mock_client):
    interface = FirestoreInterface()
    model = interface.InsertModel(collection_id='test', inserts={'field1': 'value1', 'field2': 'value2'})
    mock_client.collection.return_value.document.return_value.set.return_value = None
    # This should not raise any exceptions
    interface.insert(model)


@patch('db_interfaces.FirestoreInterface.firestore.Client')
def test_update(mock_client):
    interface = FirestoreInterface()
    model = interface.UpdateModel(collection_id='test', doc_id='doc1', updates={'field1': 'new_value1'})
    mock_client.collection.return_value.document.return_value.update.return_value = None
    # This should not raise any exceptions
    interface.update(model)


@patch('db_interfaces.FirestoreInterface.firestore.Client')
def test_delete(mock_client):
    interface = FirestoreInterface()
    model = interface.DeleteModel(collection_id='test', doc_id='doc1')
    mock_client.collection.return_value.document.return_value.delete.return_value = None
    # This should not raise any exceptions
    interface.delete(model)

