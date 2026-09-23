# WordPress自动发布设置

目标站点：<https://japanmedicalblog.wordpress.com>

## 当前发布策略

- 监听 `main` 分支内新增或修改的 `wordpress/*.html` 文件。
- 使用文件名生成稳定Slug；同一Slug再次出现时更新旧文章，不重复创建。
- 默认状态为 `draft`，先进行3篇测试。
- 医疗内容必须先通过仓库现有合规检查，再合并至 `main`。
- 不在仓库中保存WordPress密码或患者资料。

## 一次性设置

在GitHub仓库进入：

`Settings → Secrets and variables → Actions`

### Secrets

新增以下Repository secrets：

- `WP_SITE_URL`：`https://japanmedicalblog.wordpress.com`
- `WP_USERNAME`：WordPress登录用户名
- `WP_APP_PASSWORD`：WordPress为本自动发布程序单独创建的应用程序密码

不要填写日常登录密码。应用程序密码应只用于此发布程序，可以随时在WordPress后台撤销。

### Variables

新增Repository variable：

- `WP_POST_STATUS`：先填写 `draft`

完成3篇草稿测试并人工检查标题、正文、来源、链接和分类后，可将它改为 `publish`，之后新文章会自动公开发布。

## WordPress应用程序密码

在WordPress后台打开用户个人资料或安全设置，寻找“Application Passwords / 应用程序密码”，创建名称为：

`GitHub Medical Publisher`

复制生成的密码，并只保存到GitHub的 `WP_APP_PASSWORD` secret。若当前WordPress.com账户不显示应用程序密码，则需改用WordPress.com OAuth授权，不能把网页登录密码写入GitHub。

## 手动测试

进入GitHub：

`Actions → Publish WordPress draft → Run workflow`

可留空文件名，让程序检测最近新增的WordPress文件；也可填写一个准确路径，例如：

`wordpress/2026-09-23-example.html`

运行成功后，到WordPress的“文章 → 草稿”核对。

## 安全边界

- 自动发布不替代医学审核。
- 获批治疗、临床试验、基础研究和个案治疗必须明确区分。
- 不承诺疗效，不公开索取病历。
- 应用程序密码泄露或停止使用时，应立即在WordPress撤销并更新GitHub secret。
