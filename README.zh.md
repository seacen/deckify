<div align="center">

# deckify

### 别再做 slide 了。让 AI 用 HTML 来写——那才是它与生俱来的媒介。

> 任何品牌的网站，变成只有这个品牌能做出的 slides。

[English](README.md) · [**中文**](README.zh.md)

</div>

---

## deckify 做什么

你给 deckify 任何一个品牌的网站。几分钟之后你会拿到：

1. **一份完整的 Design System** —— 这个品牌的颜色、字体、logo、调性，以及每张 slide 应该遵守的规则。存成一个 `.md` 文件，可以交给任何 AI agent 反复使用。
2. **一份 9 页示范 deck** —— 已经按品牌视觉语言做好，浏览器直接打开。是「活的 HTML」，不是 PPT 文件。

就这样。不需要会设计。不需要 PowerPoint。不用跟模板较劲。

```
你:      use deckify on https://www.tiffany.com
deckify: ... 像设计师一样阅读 tiffany.com
         ... 提取颜色、字体、logo、氛围
         ... 写出一份 Design System
         ... 用 Tiffany 的视觉语言搭建 9 页 deck
         ... 自检自己的工作，发现问题就修
         ✓ 完成。打开 ~/deckify/decks/tiffany/tiffany-deck.html
```

---

## deckify 与众不同之处

### 1. 它「看着学」品牌

deckify 像设计师一样浏览品牌网站 —— 点进首页、关于我们、媒体页；找到真正的 logo（不是占位符）；读出真实的颜色和字体；感受调性。大多数「AI 设计工具」是从 prompt 生成的；**deckify 是从证据学习的**。

### 2. 它会自检自己的工作 —— 然后自己改

deckify 做完 slide 之后不会简单地说「完成了」。它会运行 **11 项自动检查**（「尺寸对吗？」「logo 真的能看见吗？」「在手机上能正常显示吗？」），再用 **6 项视觉标准**给自己的输出打分（「品牌感对吗？」「字体节奏好吗？」「内容读起来顺吗？」）。

哪一项分低，它就改哪部分，再跑一遍检查。你看到的 deck，是 deckify 自己也认为足够好可以交付的版本。

### 3. 它知道哪些规则永远不能变

做 slide 是有规则的：每张 slide 必须有 logo；字小于 12px 不可读；移动端必须折叠成单栏。大多数 AI slide 工具每次都要重新踩一次坑。deckify 把 40+ 条这种规则烙进核心，每个品牌只有「真该变的部分」（颜色、字体、调性）变化。结果：每个 deck 都长得像那个品牌、同时在工程上也站得住——桌面端、移动端、投影仪、打印件都行。

---

## 看看实际效果

deckify 已经为 9 个参考品牌生成了完整 deck。在浏览器打开 HTML 文件就能翻看：

| 品牌 | 调性 | 目录 |
|---|---|---|
| **Tiffany & Co.**（中文版） | 编辑式奢侈，Didone 衬线，克制的 Tiffany Blue | [`decks/tiffany/`](decks/tiffany/) |
| **Apple** | 极简，完美字体，柔和灰阶 | [`decks/apple/`](decks/apple/) |
| **Stripe** | 工程精度，Söhne 风 sans，强紫色渐变 | [`decks/stripe/`](decks/stripe/) |
| **Unilever** | 温暖人文，可持续叙事，自定义字体 | [`decks/unilever/`](decks/unilever/) |
| **P&G** | 企业蓝徽章，渐变 logo，克制 chrome | [`decks/pg/`](decks/pg/) |
| **Coca-Cola** | 编辑式遗产，Georgia 衬线，深红 | [`decks/coca-cola/`](decks/coca-cola/) |
| **Mars** | 自信企业，多事业部调色 | [`decks/mars/`](decks/mars/) |
| **L'Oréal** | 法式时尚编辑感，高对比衬线 | [`decks/loreal/`](decks/loreal/) |

每个目录里：一份 `*-PPT-Design-System.md`（规范）和一份 `*-deck.html`（用浏览器打开）。

---

## 安装

deckify 支持三个 AI 编程 agent —— **Claude Code**、**Codex** 和 **OpenClaw**。从下方挑你的；如果你不想自己折腾，**直接把 [给 AI agent 的安装指令](#让你的-ai-agent-自动安装) 粘贴给你的 agent，让它帮你装**。

### Claude Code

```bash
claude plugin marketplace add https://github.com/seacen/deckify
claude plugin install deckify
```

重启 Claude Code，然后输入：`use deckify on https://example.com`。

### Codex

```bash
git clone https://github.com/seacen/deckify.git ~/.codex/deckify
mkdir -p ~/.agents/skills
ln -sf ~/.codex/deckify/skills/deckify ~/.agents/skills/deckify
```

重启 Codex，然后输入：`use deckify on https://example.com`。

### OpenClaw

```bash
git clone https://github.com/seacen/deckify.git ~/openclaw-deckify
mkdir -p ~/.openclaw/workspace/skills
ln -sf ~/openclaw-deckify/skills/deckify ~/.openclaw/workspace/skills/deckify
```

重启 OpenClaw，然后输入：`use deckify on https://example.com`。

### 验证依赖

deckify 用 [`agent-browser`](https://github.com/vercel-labs/agent-browser) 像真正的浏览器一样读网站。安装完成后跑：

```bash
python3 ~/<安装路径>/skills/deckify/scripts/setup.py
```

如果 `agent-browser` 不在 PATH，脚本会打印对应平台的安装命令。

---

## 让你的 AI agent 自动安装

> 👋 如果你是正在阅读本文的 AI agent ——用户想让你在这台机器上安装 deckify。请识别你所在的 host 环境，执行下方对应的命令块。然后确认安装完成。除非 `agent-browser` 安装失败，否则不要让用户手动操作。

**Claude Code**（你有 `/skill-creator`、`/loop` 等命令）:
```
claude plugin marketplace add https://github.com/seacen/deckify
claude plugin install deckify
```

**Codex CLI**（你跑在 `codex` 交互模式里）:
```
git clone https://github.com/seacen/deckify.git ~/.codex/deckify
mkdir -p ~/.agents/skills
ln -sf ~/.codex/deckify/skills/deckify ~/.agents/skills/deckify
```

**OpenClaw**（你的 workspace 在 `~/.openclaw/workspace/`）:
```
git clone https://github.com/seacen/deckify.git ~/openclaw-deckify
mkdir -p ~/.openclaw/workspace/skills
ln -sf ~/openclaw-deckify/skills/deckify ~/.openclaw/workspace/skills/deckify
```

安装完成后，让用户**重启 agent host** 让 skill 被识别，然后跑 `scripts/setup.py` 验证依赖。skill 就可以通过 `use deckify on https://...` 触发了。

---

## 怎么用 deckify

```
你:        use deckify on https://www.your-brand.com

deckify:  （第 1 阶段）读首页 + 5–8 个子页，截图，提取颜色/字体/logo
          （第 2 阶段）就那 1–2 个真的不确定的点问你（语言、有歧义的 logo 等）
          （第 3 阶段）写出 ~/deckify/decks/<品牌>/<品牌>-PPT-Design-System.md
          （第 4 阶段）搭出 ~/deckify/decks/<品牌>/<品牌>-deck.html
          （第 5 阶段）跑 11 项硬检查 + 给自己的视觉质量打分
          （第 6 阶段）把两份文件 + 一页摘要交给你
```

总耗时：**大多数品牌 5–10 分钟**，反爬严的网站会再长一点。

输出**永远**落在 `~/deckify/decks/<品牌>/`，无论你从哪个目录运行命令。

---

## 文件落在哪里

```
~/deckify/                          ← 你生成的所有品牌输出
└── decks/
    └── <品牌>/
        ├── <品牌>-PPT-Design-System.md   ← 主交付物
        ├── <品牌>-deck.html              ← 示范 deck，浏览器直接打开
        └── source/                        ← logo、品牌画像、抓取的页面
```

每次运行的报告（截图、通过/失败日志）落在 `~/deckify/reports/runs/<时间戳>/`。

---

## 这个仓库里到底有什么

| 文件夹 | 是什么 |
|---|---|
| [`skills/deckify/`](skills/deckify/) | skill 本体 —— 装到你机器上的内容 |
| [`decks/`](decks/) | 9 个参考品牌的输出，作为学习材料 |
| [`tools/phase-a/`](tools/phase-a/) | 维护者专用 —— 用来持续打磨 skill |
| [`TESTING.md`](TESTING.md) | 双层测试模型（skill 整体质量 vs 单个 deck 质量）|
| [`CLAUDE.md`](CLAUDE.md) | 任何 AI agent 在这个仓库工作的规则 |

---

## 协议

[**PolyForm Noncommercial 1.0.0**](LICENSE) —— 个人、教育、研究、慈善和非商业用途免费使用。**商业用途需要单独授权。** 必须署名：再分发或基于 deckify 二次开发时必须保留 LICENSE 文件。

如果不确定你的使用是不是「非商用」，请在 GitHub 提 issue 询问。

---

## 致谢

由 **Xichang (Seacen) Zhao** 创建 —— [github.com/seacen](https://github.com/seacen)。

Engineering DNA 提炼自数次失败的 slide。`references/ds-template.md` 里的每一行都来自一次真实的生产 bug。

为 AI 时代而生。
