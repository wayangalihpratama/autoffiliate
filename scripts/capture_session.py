import sys
import os
from playwright.sync_api import sync_playwright


def capture_session(target_url, output_path):
    """
    Opens a browser for manual login and saves the session state.
    """
    print(f"\n--- SESSION CAPTURE TOOL ---")
    print(f"Target: {target_url}")
    print(f"Saving to: {output_path}")
    print(
        f"Instructions: Log in manually in the browser window. Once logged in, close the browser.\n"
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(target_url)

        # Wait until the browser is closed manually
        print("Waiting for you to log in and close the browser...")
        browser.on("disconnected", lambda: print("Browser closed."))

        # Keep the script running until the browser is closed
        try:
            while browser.is_connected():
                page.wait_for_timeout(1000)
        except:
            pass

        # Save storage state
        context.storage_state(path=output_path)
        print(f"SUCCESS: Session saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 capture_session.py [tiktok|kalodata]")
        sys.exit(1)

    choice = sys.argv[1].lower()
    if choice == "tiktok":
        capture_session("https://www.tiktok.com/login", "sessions/tiktok.json")
    elif choice == "kalodata":
        capture_session(
            "https://www.kalodata.com/login", "sessions/kalodata.json"
        )
    else:
        print("Invalid choice. Use 'tiktok' or 'kalodata'.")
