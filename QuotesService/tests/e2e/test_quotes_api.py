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

    # Wait for connection to be established
    expect(page.get_by_role('button', name='Speichern')).to_be_enabled()

    # Get current quote and make sure it's loaded
    quote_element = page.locator('.card-text').first
    expect(quote_element).to_be_visible()
    current_quote = quote_element.text_content()
    print(f"Current quote: {current_quote}")

    # Save quote and wait for request to complete
    with page.expect_response(lambda r: '/save' in r.url):
        page.get_by_role('button', name='Speichern').click()

    # Wait for the stored quotes request to complete
    with page.expect_response(lambda r: '/stored_quotes' in r.url):
        page.wait_for_timeout(1000)  # Small buffer for UI update

    # Verify saved quotes list
    saved_quotes_list = page.locator('.list-group')
    expect(saved_quotes_list).to_be_visible()

    saved_quote_items = page.locator('.list-group-item')
    expect(saved_quote_items).to_be_visible()

    # Print debug info if needed
    if not saved_quote_items.count():
        print("Debug: Page content")
        print(page.content())
        print(f"Debug: Looking for quote: {current_quote}")

    # Verify the quote text - only first 15 characters for brevity
    current_quote_short = current_quote[:15]
    saved_quote = saved_quote_items.first.text_content()
    expect(saved_quote[:15]).to_equal(current_quote_short)

def test_error_handling(page: Page):
    # Test with invalid API key
    page.get_by_placeholder('API-Schlüssel eingeben').fill('invalid_key')
    page.get_by_role('button', name='Verbinden').click()

    # Try to load saved quotes
    page.get_by_role('button', name='Speichern').click()

    # Verify connection state is reset
    expect(page.get_by_role('button', name='Speichern')).to_be_disabled()