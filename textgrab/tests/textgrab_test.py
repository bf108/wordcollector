import pytest

from textgrab import (check_url_schema,
                                format_url,
                                check_req_status,
                                collect_url_text,
                                normalize,
                                split_words,
                                word_count_dict,
                                sort_words_desc)
              
def test_check_url_schema():
    assert check_url_schema('www.test.com') == 'https://www.test.com', "Expected: https://www.test.com"
    assert check_url_schema('') == 'https://', "Expected: https://"
    assert check_url_schema('http://www.test.com') == 'http://www.test.com', "http://www.test.com"
    assert check_url_schema('https://www.test.com') == 'https://www.test.com', "Expected: https://www.test.com"

def test_format_url():
    assert format_url('  www.test.com   ') == 'https://www.test.com', "Expected: https://www.test.com"
    assert format_url('') == 'https://', "Expected: https://"
    assert format_url('http://www.TEST.com') == 'http://www.test.com', "Expected: http://www.test.com"
    assert format_url('wWw.TesT.Com') == 'https://www.test.com', "Expected: https://www.test.com"

def test_normalize():
    #Check for correct lowercase
    assert normalize('AbcdEF') == 'abcdef', "Expected: abcdef"
    #Check for removal of whitespace
    assert normalize('  AbcdEF  ') == 'abcdef', "Expected: abcdef"
    #Remove trailing and leading punctuation
    assert normalize('!.AbcdEF!.!!!?') == 'abcdef', "Expected: abcdef"
    #Remove and digits
    assert normalize('!.AbcdEF123!.!!!?') == 'abcdef', "Expected: abcdef"
    #Check times
    assert normalize('14:56') == '', "Expected: ''"

def test_split_words():
    assert split_words('Skip to content') == ['Skip','to','content'], "Expected: ['Skip','to','content']"
    assert split_words('') == [], "Expected: []"
    assert split_words('Skip    to      content') == ['Skip','to','content'], "Expected: ['Skip','to','content']"

def test_sort_words_desc():
    assert sort_words_desc({'foo':10,'bar':5,'fizz':6,'buzz':12}) == [("buzz",12),("foo",10),("fizz",6),("bar",5)], "Expected: [('buzz':12),('foo':10), ('fizz':6), ('bar': 5)]"


