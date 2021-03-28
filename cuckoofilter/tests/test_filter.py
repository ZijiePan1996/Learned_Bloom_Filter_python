import pytest
import cuckoofilter

@pytest.fixture
def cf():
    return cuckoofilter.CuckooFilter(1000, 4)

def test_insert(cf):
    assert cf.insert('hello')
    assert cf.size == 1

def test_insert_second_position(cf):
    for _ in range(cf.bucket_size - 1):
        cf.insert('hello')
    i1 = cf.insert('hello')
    i2 = cf.insert('hello')
    assert i1 != i2

def test_insert_full(cf):
    # A cuckoofilter can hold at most 2 * bucket_size of the same fingerprint
    for _ in range(cf.bucket_size * 2):
        cf.insert('hello')

    with pytest.raises(Exception) as e:
        cf.insert('hello')

    assert str(e.value) == 'Filter is full'
    assert cf.size == (cf.bucket_size * 2)

def test_insert_over_capacitiy(cf):
    with pytest.raises(Exception) as e:
        for i in range((cf.capacity * cf.bucket_size) + 1):
            cf.insert(str(i))
    assert str(e.value) == 'Filter is full'
    assert cf.load_factor() > 0.9

def test_contains(cf):
    cf.insert('hello')
    assert cf.contains('hello'), 'Key was not inserted'

def test_contains_builtin(cf):
    cf.insert('hello')
    assert 'hello' in cf

def test_delete(cf):
    cf.insert('hello')
    assert cf.delete('hello')
    assert not cf.contains('hello')
    assert cf.size == 0

def test_delete_second_bucket(cf):
    for _ in range(cf.bucket_size + 1):
        cf.insert('hello')
    for _ in range(cf.bucket_size + 1):
        cf.delete('hello')
    assert cf.size == 0

def test_delete_non_existing(cf):
    assert not cf.delete('hello')

def test_load_factor_empty(cf):
    assert cf.load_factor() == 0

def test_load_factor_non_empty(cf):
    cf.insert('hello')
    assert cf.load_factor() == (1 / (cf.capacity * cf.bucket_size))
