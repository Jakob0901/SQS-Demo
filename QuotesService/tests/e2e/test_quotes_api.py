import os

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def setup(page: Page):
    port = str(os.environ.get('QUOTES_SERVICE_PORT', 80))
    page.goto('http://localhost:' + port)
    yield page


def test_initial_page_load(page: Page):
    # Check if main UI elements are present
    expect(page.locator('h1')).to_have_text('Zitate-Service')
    expect(page.get_by_text('API-Schlüssel')).to_be_visible()
    expect(page.get_by_text('Zufälliges Zitat')).to_be_visible()
    expect(page.get_by_text('Gespeicherte Zitate')).to_be_visible()

    # Verify initial state
    expect(page.get_by_role('button', name='Verbinden')).to_be_disabled()
    expect(page.get_by_role('button', name='Speichern')).to_be_disabled()
    expect(page.get_by_role('button', name='Neues Zitat')).to_be_enabled()


def test_random_quote_functionality(page: Page):
    # Get initial quote
    initial_quote = page.locator('.card-text').first.text_content()

    # Click new quote button
    page.get_by_role('button', name='Neues Zitat').click()
    page.wait_for_timeout(1000)  # Wait for API response

    # Verify quote changed
    new_quote = page.locator('.card-text').first.text_content()
    assert initial_quote != new_quote, "Quote should change after clicking 'Neues Zitat'"


def test_api_key_connection(page: Page):
    # Enter API key
    page.get_by_placeholder('API-Schlüssel eingeben').fill('test_api_key')
    expect(page.get_by_role('button', name='Verbinden')).to_be_enabled()

    # Connect
    page.get_by_role('button', name='Verbinden').click()

    # Verify connection state
    expect(page.get_by_role('button', name='Speichern')).to_be_enabled()


def test_save_and_load_quotes(page: Page):
    # Connect with API key first
    page.get_by_placeholder('API-Schlüssel eingeben').fill('test_api_key')
    page.get_by_role('button', name='Verbinden').click()

    # Get current quote
    current_quote = page.locator('.card-text').first.text_content()

    # Save quote
    page.get_by_role('button', name='Speichern').click()
    page.wait_for_timeout(1000)  # Wait for API response

    # Verify quote appears in saved quotes list
    saved_quotes = page.locator('.list-group-item')
    expect(saved_quotes).to_contain_text(current_quote)


def test_error_handling(page: Page):
    # Test with invalid API key
    page.get_by_placeholder('API-Schlüssel eingeben').fill('invalid_key')
    page.get_by_role('button', name='Verbinden').click()

    # Try to load saved quotes
    page.get_by_role('button', name='Speichern').click()

    # Verify connection state is reset
    expect(page.get_by_role('button', name='Speichern')).to_be_disabled()