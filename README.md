# GitHub Issue Mermaid Generator

このスクリプトは、指定したGitHubリポジトリの全Issueを取得し、Mermaid形式のダイアグラムとMarkdownリンクを生成します。これにより、リポジトリのIssueの依存関係を視覚化しやすくします。

## 必要条件

- Python 3.x
- `requests`ライブラリ

```bash
pip install requests
```

## 使用方法

1. リポジトリのURLを準備します。形式は `https://github.com/owner/repo` です。

2. スクリプトを実行します。

```bash
python issue_to_mermaid.py
```

3. プロンプトが表示されたら、対象のGitHubリポジトリのURLを入力します。

4. スクリプトが実行されると、リポジトリの全Issueが取得され、`mermaid_all_issues.md`というファイルにMermaid形式のコードとMarkdown形式のリンクが書き出されます。

## 機能

- **タイトルのエスケープ**: 特殊文字を取り除いて、Mermaidダイアグラムに適した形式に変換します。
- **タイトルの長さ制限**: タイトルの長さを指定された最大長に制限し、視覚化をスムーズにします。
- **依存関係の解析**: Issueの本文内のリンクを解析し、依存関係をMermaid図として表示します。
- **Markdownリンクの生成**: 各IssueへのリンクをMarkdown形式で生成し、ドキュメント内で利用可能にします。

## 出力例

- `mermaid_all_issues.md`には、次のような内容が含まれます：

    ```mermaid
    graph LR;
        Issue1["タイトル1 #1"]
        style Issue1 fill:none,stroke:#d3d3d3,stroke-width:2;
        Issue1 --> Issue2
    ```

    - Markdownリンク例:
    
    ```
    - [#1](https://github.com/owner/repo/issues/1): タイトル1
    ```
