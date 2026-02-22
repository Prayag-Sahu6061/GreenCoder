import token
import requests

def get_repo_contents(owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": "TOKEN = "YOUR_TOKEN_HERE"",
        "User-Agent":"Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    print("Status:", response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error response:", response.json())
        return []

def collect_python_files(owner, repo, path=""):
    contents = get_repo_contents(owner, repo, path)
    python_files = []

    for item in contents:
        if not isinstance(item, dict):
            continue

        if item.get("type") == "file" and item.get("name", "").endswith(".py"):
            python_files.append(item.get("download_url"))

        elif item.get("type") == "dir":
            python_files.extend(
                collect_python_files(owner, repo, item.get("path"))
            )

    return python_files


def download_files(file_urls, limit=10):
    code_list = []
    for url in file_urls[:limit]:
        file_response = requests.get(url)
        if file_response.status_code == 200:
            code_list.append(file_response.text)
    return code_list



if __name__ == "__main__":
    repo_input = input("Enter repo (owner/repo): ")

    try:
        owner, repo = repo_input.split("/")
    except ValueError:
        print("Invalid format. Use owner/repo")
        exit()
    file_urls = collect_python_files(owner, repo)
    print("Found Python files:", len(file_urls))
    code_list = download_files(file_urls, limit=10)
    print(f"Collected {len(code_list)} Python files successfully.")