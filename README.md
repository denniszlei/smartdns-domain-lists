# SmartDNS Domain Rules

自动从以下上游规则源拉取并转换为 SmartDNS 可直接使用的 domain list：

- Loyalsoldier direct-list
- Loyalsoldier apple-cn
- pmkol cdn_domain_list
- Loyalsoldier proxy-list
- Loyalsoldier gfw

## 输出文件

- `dist/direct-list.txt`
- `dist/cn-apple-list.txt`
- `dist/cn-cdn-list.txt`
- `dist/proxy-list.txt`
- `dist/gfw-list.txt`

## 转换规则

- `full:example.com` -> `-.example.com`
- `domain:example.com` -> `example.com`
- `regexp:*` -> 忽略

## Raw 下载地址

```text
https://raw.githubusercontent.com/<你的用户名>/<仓库名>/main/dist/direct-list.txt
https://raw.githubusercontent.com/<你的用户名>/<仓库名>/main/dist/cn-apple-list.txt
https://raw.githubusercontent.com/<你的用户名>/<仓库名>/main/dist/cn-cdn-list.txt
https://raw.githubusercontent.com/<你的用户名>/<仓库名>/main/dist/proxy-list.txt
https://raw.githubusercontent.com/<你的用户名>/<仓库名>/main/dist/gfw-list.txt