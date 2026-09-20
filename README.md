# Bing Daily Wallpaper

> **说明：本项目 100% 由 AI 生成，代码、工作流和文档均由 AI 完成，人工含量为零。**

每天自动获取中国区微软必应每日一图的 UHD 版本，并通过 GitHub Pages 提供固定链接。

## 固定链接

- UHD 图片：<https://nafeuy.github.io/bing-daily-wallpaper/bing-daily-uhd.jpg>
- 图片信息：<https://nafeuy.github.io/bing-daily-wallpaper/info.json>
- 展示页面：<https://nafeuy.github.io/bing-daily-wallpaper/>

`info.json` 包含日期、标题、版权信息和当天的必应 UHD 原始链接。固定图片地址由
GitHub Pages 托管，因此不会随着必应每天更换原始 URL 而改变。

## 工作方式

GitHub Actions 每天北京时间 03:00（UTC 前一天 19:00）运行，也支持手动触发。工作流会：

1. 请求必应中国区每日图片元数据；
2. 根据 `urlbase` 下载 `_UHD.jpg`，并验证响应是 JPEG；
3. 生成静态页面和 `info.json`；
4. 使用 GitHub 官方 Pages Actions 部署 `_site`。

首次部署时，工作流会尝试自动启用 GitHub Pages。如果仓库或组织策略禁止自动启用，
请在 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。

## 本地构建

```bash
python scripts/build_site.py
```

生成结果位于 `_site/`。必应图片可能受到版权或下载限制；请遵守图片所附版权信息，
不要将本项目提供的固定链接视为再分发授权。
