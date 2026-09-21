这个项目目前是一套 Instagram + TikTok 日本达人建联工作台，核心定位是“帮你找、筛、写、跟”，不是全自动登录账号群发私信。当前公开仓库地址是 sosove-creator-outreach。
它现在能实现的功能
1. 双平台独立建联面板
   - Instagram 面板：/
   - TikTok 面板：/tiktok/
   - 两个平台候选池、字段、规则、数据文件完全独立，互不干扰。
2. 达人候选池管理
   - CSV 导入、导入前预览、重复账号识别和更新合并
   - 手动新增候选
   - 按综合评分、更新时间、粉丝、报价、建联时间、发货时间等排序
   - 状态、等级、关键词筛选
   - 单个删除、删除全部
   - 置顶
   - 导出 CSV
   - 候选数据保存在本地 data 目录
3. 达人发现和采集
   - 打开 Google/平台搜索页
   - 通过 Google Custom Search 或 SerpApi 做公开搜索，识别 Instagram/TikTok 主页链接
   - 粘贴 Google 结果、URL 列表、HTML、@handle 提取候选
   - 网站识别器：抓取公开网页中出现的 Instagram 链接
   - 合规采集器：只解析你提供的文本，不登录 Instagram，也不抓取隐藏接口
   - Hashtag 推荐、自动填入、批量打开
4. 达人评分和筛选
   - Instagram：粉丝区间、互动率、内容匹配、人群匹配、品牌安全、合作信号、可联系性、资料完整度
   - TikTok：平均播放、中位播放、播放粉丝比、互动率、更新频率、内容匹配、品牌安全、可联系性
   - 自动生成 S/A/B/C/D 等级和资料补全建议
5. 达人资料补全
   - Instagram 官方 Graph API 补全：
     - 用户名
     - 昵称
     - 粉丝数
     - 简介
     - 头像
     - 网站
     - 媒体数量
   - 支持 Instagram Login token 和 Facebook/Page 连接的 Business Discovery 模式
   - 支持从公开简介、网页文本中识别邮箱、地区、标签、赛道
6. 建联文案生成
   - DM、Email、Follow-up 三种文案
   - 根据达人昵称、赛道、标签、近期内容生成个性化文案
   - 内置日本女装类本地模板
   - 支持 OpenAI-compatible API 和 CPA 中转
   - 可在网页里配置 Base URL、模型名、API Key
   - 支持测试接口、复制文案、恢复默认
7. 人工确认建联队列
   - 从当前筛选结果按评分逐个处理
   - 自动打开达人主页
   - 自动复制 DM 到剪贴板
   - 你手动发送后，点击“已手动发送，下一个”
   - 自动记录建联时间和下次跟进日期
   - 可以跳过、停止、设置今日目标
8. 回复处理助手
   - 识别报价、有兴趣、想看产品、拒绝合作等回复类型
   - 自动更新候选人状态
   - 生成日文回复草稿
   - 支持本地规则和模型生成
9. 合作结果追踪
   - 发送邀约时间、建联时间
   - 博主 ID、博主类型、粉丝数、主页链接
   - 报价、合作产品、合作阶段
   - 收货姓名、邮编、详细地址、手机号
   - 订单编号、物流单号、发货时间、收货时间
   - 视频进度、发帖日期、帖子链接
   - 优惠码、订单数、收入
   - 自动计算成本和 ROI
10. 今日任务看板
    - 今日跟进
    - 超期未跟
    - 已回复待处理
    - 报价待确认
    - 资料待补
    - 待寄样
    - 运输中
    - 脚本/初稿待审
    - 待发布
11. 部署能力
    - 纯 Python 标准库运行
    - Docker / Docker Compose
    - Windows、macOS、Linux
    - 可直接 IP + 端口访问
    - 数据持久化到 ./data
它能产生的实际效果
- 把散乱的达人链接整理成可筛选、可排序、可追踪的候选池。
- 把“找达人、看资料、写文案、记进度”集中在一个面板里。
- 用评分规则快速筛掉明显不合适的账号。
- 用固定模板或 AI 模型批量生成日语建联文案。
- 把每次建联、寄样、发帖、订单和 ROI 串成一条记录。
- 降低重复劳动，但仍然保留人工确认和人工发送。
它不能实现或故意不做的部分
- 不会自动登录 Instagram 或 TikTok。
- 不会自动发送无人值守的批量私信。
- 不会抓取登录后才能看到的粉丝、评论、私信或隐藏接口。
- Instagram IGAA... token 只能补全授权账号本身，不能查询其他达人。
- 要补全其他达人，需要 Facebook/Page 连接的 Instagram 专业账号，并配置 META_IG_USER_ID。
- 公开搜索 API 只负责找主页链接，不负责抓取达人完整资料。
- 头像批量获取依赖 Instagram Graph API 或你导入的头像链接。
一句话概括：这是一个日本达人开发的 CRM 和建联效率工具，能自动发现线索、评分、生成文案和追踪合作，但私信发送这一步仍然由你人工确认。
# SOSOVE Creator Outreach

Instagram and TikTok creator outreach workspaces for the SOSOVE Japan workflow.

The project is a private operator tool for candidate management, CSV import, public-search connectors, outreach copy drafting, reply handling, and partnership tracking. It does not log in to social accounts, scrape hidden APIs, or send unattended bulk DMs.

## Panels

- Instagram: `http://127.0.0.1:8796/`
- TikTok: `http://127.0.0.1:8796/tiktok/`
- Health check: `http://127.0.0.1:8796/api/health`

Instagram and TikTok use separate data files and endpoints.

## Install On Another Computer

Requirements:

- Git
- Python 3.11 or newer

Clone and start:

```powershell
git clone https://github.com/sosoveooo-bit/sosove-creator-outreach.git
cd sosove-creator-outreach
Copy-Item .env.example .env
python -m instagram_creator_outreach.server --host 0.0.0.0 --port 8796
```

On macOS or Linux:

```bash
git clone https://github.com/sosoveooo-bit/sosove-creator-outreach.git
cd sosove-creator-outreach
cp .env.example .env
python3 -m instagram_creator_outreach.server --host 0.0.0.0 --port 8796
```

The application uses the Python standard library only, so there is no `pip install` step for the core server.

## Docker

Create `.env` first:

```bash
cp .env.example .env
docker compose up -d --build
```

Change the public port when needed:

```env
PANEL_PORT=8796
```

Persistent candidate data is stored in `./data` on the host.

## Environment Variables

Start with [.env.example](.env.example). The most common integrations are:

```env
GOOGLE_CSE_API_KEY=
GOOGLE_CSE_CX=
SERPAPI_API_KEY=

META_ACCESS_TOKEN=
META_IG_USER_ID=

OUTREACH_COPY_MODEL_PROVIDER=cpa
OUTREACH_COPY_MODEL_BASE_URL=
OUTREACH_COPY_MODEL_NAME=
OUTREACH_COPY_MODEL_API_KEY=
OUTREACH_COPY_MODEL_AUTH_MODE=bearer
```

The model gateway is OpenAI-compatible. CPA proxy mode uses the `/chat/completions` endpoint and bearer authentication by default.

Keep `.env` private. The repository intentionally ignores `.env`, runtime data, logs, CSV exports, and candidate JSON files.

## Tests

```powershell
python -m unittest discover -s instagram_creator_outreach/tests -v
python -m unittest discover -s tiktok_creator_outreach/tests -v
```

## VPS Notes

The Docker command publishes the service directly on the selected port. If the VPS firewall is enabled, allow that port. For public internet exposure, place the panel behind an access-control layer such as a VPN, firewall allowlist, or reverse proxy with authentication.
