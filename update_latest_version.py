"""
This script fetches the latest version number of OpenZoomstack from the 
OS Downloads API and saves it to a file named `latest_version.txt`.
"""

import requests


def update_latest_openzoomstack_version():
    """
    Makes the fetch request to the OS Downloads API to get the latest version of OpenZoomstack and
    saves it to a file named `latest_version.txt`. 
    The version is formatted as YYYYMM. If the request fails it prints an error
    """
    api_url = "https://api.os.uk/downloads/v1/products/OpenZoomstack"

    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP errors

        data = response.json()
        latest_version = data.get("version", None)

        # The latest version tends to be in the format YYYY-MM
        # As we need it as a comparable number we can convert it to YYYYMM by removing the dash
        if latest_version and "-" in latest_version:
            latest_version = latest_version.replace("-", "")
            print(
                f"Latest OpenZoomstack version (formatted): {latest_version}")

        # Save the latest version to a file
        with open("latest_version.txt", "w", encoding="utf-8") as file:
            file.write(latest_version)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the latest version: {e}")


if __name__ == "__main__":
    update_latest_openzoomstack_version()
