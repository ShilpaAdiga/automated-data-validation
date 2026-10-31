from main import (
    is_valid_email,
    is_valid_phone,
    is_valid_website,
    is_valid_date   
)

def test_valid_email():
    assert is_valid_email("alex@example.com") is True


def test_invalid_email():
    assert is_valid_email("not-an-email") is False


def test_valid_phone():
    assert is_valid_phone("1234567890") is True


def test_invalid_phone():
    assert is_valid_phone("123") is False


def test_valid_website():
    assert is_valid_website("https://example.com") is True


def test_invalid_website():
    assert is_valid_website("not-a-website") is False


def test_valid_date():
    assert is_valid_date("2026-10-27") is True


def test_invalid_date():
    assert is_valid_date("27-10-2026") is False


def test_email_with_whitespace():
    assert is_valid_email("  alex@example.com  ") is True


def test_missing_email():
    assert is_valid_email(None) is False


def test_phone_with_separators():
    assert is_valid_phone("+1-234-567-8901") is True


def test_missing_website():
    assert is_valid_website(None) is False

