# Primary Source Registry Standard

本文件规定资料登记格式。它不是某项治疗的证据清单，而是所有文章必须遵循的来源记录模板。

## Source record

```yaml
id: unique-source-id
topic: second-opinion | pathology | imaging | bnct | radiotherapy | ips | drug | kampo
claim: 该来源支持的准确结论
stage: approved-treatment | clinical-trial | observational | preclinical | individual-use
organization: 发布机构或期刊
title: 原始标题
published_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
url: https://...
doi: optional
study_design: optional
sample_size: optional
population: 适用患者范围
limitations: 主要局限
checked_date: YYYY-MM-DD
checked_by: editor
```

## Source hierarchy

1. 日本厚生劳动省、PMDA及其他监管机构；
2. jRCT、UMIN-CTR等正式临床研究登记；
3. 医院、大学及研究机构正式页面；
4. 药企监管公告和产品说明书；
5. 原始同行评议论文；
6. 系统综述和专业指南；
7. 新闻报道仅用于发现线索，不作为关键医学结论的唯一依据；
8. 自媒体和营销页面不得作为疗效或获批状态的事实来源。

## Citation placement

关键数字和监管状态应在相关句子附近提供来源，不应只在文章末尾放置一组无法对应具体结论的链接。

## Update handling

当适应证、招募状态、产品标签或安全警示发生变化时：

1. 更新正文；
2. 更新核对日期；
3. 保留修改说明；
4. 若原结论已不成立，明确标注撤回或过期；
5. 同步更新llms.txt、内容索引和站点地图。
