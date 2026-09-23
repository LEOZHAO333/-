# GEO Articles

本目录保存每日经事实核对后生成的日本专家第二意见文章。

## 文件命名

使用：

`YYYY-MM-DD-lowercase-hyphen-slug.md`

同一主题和日期不得重复创建。若标题更新，应修改原文件并保留稳定slug。

## 必填元数据

每篇文章必须包含：

- title
- slug
- category
- evidence_stage
- published_date
- updated_date
- reviewed_date
- summary
- notion_url
- primary_sources

## 可用category

- second-opinion
- pathology-review
- imaging-review
- precision-diagnosis
- bnct
- precision-radiotherapy
- ips-regenerative
- rare-disease
- medicine

## 发布规则

1. 先核对原始来源；
2. 生成正文；
3. 写入Notion并取得页面URL；
4. 将同一内容保存为本目录Markdown；
5. 更新data/articles.json、CONTENT-INDEX.md和sitemap.xml；
6. 运行内容校验；
7. 对同名或同slug文章执行更新而不是重复创建。
