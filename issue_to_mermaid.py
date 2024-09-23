import os
import requests
import re
import argparse
from urllib.parse import urlparse

# タイトルの特殊文字をエスケープする関数
def escape_title(title):
    return (title
            .replace('"', '')
            .replace('(', '')
            .replace(')', '')
            .replace('[', '')
            .replace(']', '')
            .replace('\n', ' ')  # 改行を空白に置換
            .strip())  # 前後の空白を削除

# タイトルの長さを制限する関数
def truncate_title(title, max_length=50):
    return title[:max_length] + '...' if len(title) > max_length else title

# GitHubリポジトリからIssueデータを取得する関数
def get_issues(owner, repo):
    issues = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&page={page}&per_page=100"
        response = requests.get(url)
        response.raise_for_status()
        page_issues = response.json()
        if not page_issues:
            break
        issues.extend(page_issues)
        page += 1
    return issues

# Issueの依存関係を解析し、Mermaidコードを生成する関数
def generate_mermaid(issues):
    mermaid = "graph LR;\n"
    issue_link_regex = re.compile(r'#(\d+)')

    for issue in issues:
        issue_num = issue["number"]
        title = escape_title(issue["title"])  # タイトルをエスケープ
        title = truncate_title(title)  # タイトルを切り詰め
        mermaid += f"    Issue{issue_num}[\"{title} #{issue_num}\"]\n"
        mermaid += f"    style Issue{issue_num} fill:none,stroke:#d3d3d3,stroke-width:2;\n"

        body = issue.get("body")
        if body:
            linked_issues = issue_link_regex.findall(body)
            for linked_issue in linked_issues:
                mermaid += f"    Issue{issue_num} --> Issue{linked_issue}\n"
    
    return mermaid

# IssueのリンクをMarkdown形式で生成する関数
def generate_markdown_links(issues):
    markdown_links = []

    for issue in issues:
        issue_num = issue["number"]
        title = escape_title(issue["title"])  # タイトルをエスケープ
        title = truncate_title(title)  # タイトルを切り詰め
        url = issue["html_url"]
        markdown_links.append(f"- [#{issue_num}]({url}): {title}")

    return "\n".join(markdown_links)

# Mermaid図をファイルに書き出す関数
def save_mermaid_file(content, content_links, filepath):
    with open(filepath, "w") as f:
        f.write("```mermaid\n")
        f.write(content)
        f.write("\n```\n")
        f.write(content_links)

# GitHubからデータを取得してMermaid図を生成
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHubリポジトリのIssueからMermaid図を生成します。")
    parser.add_argument("repo_url", help="GitHubリポジトリのURL（例: https://github.com/owner/repo）")
    parser.add_argument("-o", "--output", default="mermaid_all_issues.md", help="出力ファイル名（デフォルト: mermaid_all_issues.md）")

    args = parser.parse_args()

    parsed_url = urlparse(args.repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) != 2:
        raise ValueError("無効なリポジトリのURLです。正しい形式を使用してください。")

    owner, repo = path_parts

    issues = get_issues(owner, repo)

    mermaid_all = generate_mermaid(issues)
    mermaid_all_links = generate_markdown_links(issues)

    save_mermaid_file(mermaid_all, mermaid_all_links, args.output)

