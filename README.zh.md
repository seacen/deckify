<div align="center">

# deckify

### PPT 翻篇了，AI 用 HTML 接管讲故事的边界。

> 把品牌网站抓成可复用的 Design System——做 deck 这件事，从此交给 AI。

[English](README.md) · [**中文**](README.zh.md)

</div>

---

## deckify 做什么

你给 deckify 任何一个品牌的网站。几分钟之后你拿到**两份能复利的产物**：

1. **一份完整的 Design System** —— 这个品牌的颜色、字体、logo、调性，加上每张 slide 应该遵守的工程规则。一个 `.md` 文件。可以交给任何 AI agent，反复使用。
2. **一份 9 页 demo deck** —— 已经按品牌视觉语言做好。「活的 HTML」，浏览器直接打开。证明这套规范可以工作。

第一份才是会复利的资产。之后每一份 deck 都基于它由 AI 几秒钟生成。不需要会设计。不需要 PowerPoint。不用跟模板较劲。

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

### 1. 它「看着学」品牌，不是从 prompt 编造

deckify 像设计师一样浏览品牌网站 —— 点进首页、关于我们、媒体页；找到真正的 logo（不是占位符）；读出真实的颜色和字体；感受调性。大多数「AI 设计工具」是从 prompt 生成；**deckify 从证据学习**。

### 2. 它产出的是可复用的 Design System，不是一份性的 deck

输出是一份品牌资产，不是一次性产物。这个品牌之后每一份 deck，都由 AI 基于这一份 Design System 文件生成。改一次文件，下游所有 deck 跟着升级。slide 不再是手工一份份做出来的，而是**从一份品牌规范派生出来的**。

### 3. 它会自检自己的工作 —— 然后自己改

deckify 做完 slide 之后不会简单说「完成了」。它会跑 **11 项自动检查**（「尺寸对吗？」「logo 真的能看见吗？」「在手机上能正常显示吗？」），再用 **6 项视觉标准**给自己的输出打分（「品牌感对吗？」「字体节奏好吗？」「内容读起来顺吗？」）。哪一项分低，它就改哪部分，再跑一遍检查。你看到的 deck，是 deckify 自己也认为足够好可以交付的版本。

### 4. 它知道哪些规则永远不能变

做 slide 是有规则的：每张 slide 必须有 logo；字小于 12px 不可读；移动端必须折叠成单栏。大多数 AI slide 工具每次都要重新踩一次坑。deckify 把 40+ 条这种规则烙进核心，每个品牌只有「真该变的部分」（颜色、字体、调性）变化。结果：每个 deck 都长得像那个品牌、同时在工程上也站得住——桌面端、移动端、投影仪、打印件都行。

---

## 看看实际效果

8 个参考品牌，每一份都过了机器检查 + 视觉评审。在浏览器打开 HTML 文件就能翻看：

### Tiffany & Co.（中文版）
*编辑式奢侈，Didone 衬线，克制的 Tiffany Blue。*
[打开 deck →](decks/tiffany/) · [DS markdown](decks/tiffany/tiffany-PPT-Design-System.md)

| 封面 | 内页 |
|:---:|:---:|
| ![Tiffany 封面](assets/showcase/tiffany-cover.png) | ![Tiffany 内页](assets/showcase/tiffany-content.png) |

### Stripe
*工程精度，Söhne 风 sans，强紫色渐变。*
[打开 deck →](decks/stripe/) · [DS markdown](decks/stripe/stripe-PPT-Design-System.md)

| 封面 | 内页 |
|:---:|:---:|
| ![Stripe 封面](assets/showcase/stripe-cover.png) | ![Stripe 内页](assets/showcase/stripe-content.png) |

### Unilever（联合利华）
*温暖人文，可持续叙事，自定义字体。*
[打开 deck →](decks/unilever/) · [DS markdown](decks/unilever/unilever-PPT-Design-System.md)

| 封面 | 内页 |
|:---:|:---:|
| ![Unilever 封面](assets/showcase/unilever-cover.png) | ![Unilever 内页](assets/showcase/unilever-content.png) |

### P&G（宝洁）
*企业蓝，渐变 logo 徽章，从容 chrome。*
[打开 deck →](decks/pg/) · [DS markdown](decks/pg/pg-PPT-Design-System.md)

| 封面 | 内页 |
|:---:|:---:|
| ![P&G 封面](assets/showcase/pg-cover.png) | ![P&G 内页](assets/showcase/pg-content.png) |

### P&G —— 另一版
*同一个品牌，不同氛围；展示同一份 brand 重新生成 Design System 时的另一种情绪。*
[打开 deck →](decks/pg-alt/) · [DS markdown](decks/pg-alt/pg-PPT-Design-System.md)

| 封面 | 内页 |
|:---:|:---:|
| ![P&G alt 封面](assets/showcase/pg-alt-cover.png) | ![P&G alt 内页](assets/showcase/pg-alt-content.png) |

### Coca-Cola（可口可乐）
*编辑式遗产，Georgia 衬线，深红。*
[打开 deck →](decks/coca-cola/) · [DS markdown](decks/coca-cola/coca-cola-PPT-Design-System.md)

| 封面 | 内页 |
|:---:|:---:|
| ![Coca-Cola 封面](assets/showcase/coca-cola-cover.png) | ![Coca-Cola 内页](assets/showcase/coca-cola-content.png) |

### Mars（玛氏）
*自信企业，多事业部调色，结构化网格。*
[打开 deck →](decks/mars/) · [DS markdown](decks/mars/mars-PPT-Design-System.md)

| 封面 | 内页 |
|:---:|:---:|
| ![Mars 封面](assets/showcase/mars-cover.png) | ![Mars 内页](assets/showcase/mars-content.png) |

### L'Oréal（欧莱雅）
*法式时尚编辑感，高对比衬线，杂志感时刻。*
[打开 deck →](decks/loreal/) · [DS markdown](decks/loreal/loreal-PPT-Design-System.md)

| 封面 | 内页 |
|:---:|:---:|
| ![L'Oréal 封面](assets/showcase/loreal-cover.png) | ![L'Oréal 内页](assets/showcase/loreal-content.png) |

---

## 安装 —— 把这段粘给你的 AI agent

复制下面整段。粘给你用的任何 AI 编程 agent（Claude Code、Codex、OpenClaw、Hermes、Cursor、OpenCode、自定义都行），告诉它：「**装 deckify**」。剩下的它自己搞定。

```
👋 你好 agent，用户希望你在这台机器上安装 deckify。

deckify 在 https://github.com/seacen/deckify（一个公开的 Git 仓库），
是一个标准的「skill / agent prompt」格式 —— SKILL.md + scripts/ 目录。
请识别你当前所在的 host 环境，按下方对应的命令安装。如果你的 host
不在列表里，按 GENERIC 那一档自适应即可。

────────────────────────────────────────────────────────────────────
CASE: Claude Code  (你能用 /skill-creator、/loop 等命令)

    claude plugin marketplace add https://github.com/seacen/deckify
    claude plugin install deckify

────────────────────────────────────────────────────────────────────
CASE: Codex CLI  (你跑在 `codex` 交互模式里)

    git clone https://github.com/seacen/deckify.git ~/.codex/deckify
    mkdir -p ~/.agents/skills
    ln -sf ~/.codex/deckify/skills/deckify ~/.agents/skills/deckify

────────────────────────────────────────────────────────────────────
CASE: OpenClaw  (你的 workspace 在 ~/.openclaw/workspace/)

    git clone https://github.com/seacen/deckify.git ~/openclaw-deckify
    mkdir -p ~/.openclaw/workspace/skills
    ln -sf ~/openclaw-deckify/skills/deckify ~/.openclaw/workspace/skills/deckify

────────────────────────────────────────────────────────────────────
CASE: GENERIC  (Hermes、OpenCode、Cursor、Continue、Aider 或别的)

    git clone https://github.com/seacen/deckify.git ~/deckify-skill
    # 然后两选一：
    #  (a) 把 ~/deckify-skill/skills/deckify symlink 到你 host 的
    #      skills 目录（如果你的 host 有这个机制 —— 查它的文档）；
    #     或者
    #  (b) 让 SKILL.md 作为长 prompt / context attachment 注入：
    #      用户调起 deckify 时，把 ~/deckify-skill/skills/deckify/
    #      SKILL.md 当 system instruction 加进上下文。SKILL.md 是
    #      自描述的 —— 任何 agent 看完都知道怎么驱动它。

────────────────────────────────────────────────────────────────────
安装后：验证 agent-browser 依赖

    python3 <安装路径>/skills/deckify/scripts/setup.py

如果 agent-browser 不在 PATH，脚本会给出对应平台的安装命令。如果你
有 shell 权限，请直接帮用户执行；不要让用户自己折腾。

最后让用户**重启 agent host**，让 skill 被识别。skill 就可以通过
"use deckify on https://example.com" 触发。
```

如果你想直接自己跑命令，[上面每个 host 那段就是命令](#安装--把这段粘给你的-ai-agent) —— 挑你用的那一档执行。

---

## 一次运行长什么样

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

## 这个仓库里有什么

| 文件夹 | 是什么 |
|---|---|
| [`skills/deckify/`](skills/deckify/) | skill 本体 —— 装到你机器上的内容 |
| [`decks/`](decks/) | 8 个参考品牌的输出，作为学习材料 |
| [`tools/phase-a/`](tools/phase-a/) | 维护者专用 —— 用来持续打磨 skill |
| [`TESTING.md`](TESTING.md) | 双层测试模型（skill 整体质量 vs 单个 deck 质量）|

---

## 协议

[**PolyForm Noncommercial 1.0.0**](LICENSE) —— 个人、教育、研究、慈善和非商业用途免费使用。**商业用途需要单独授权。** 必须署名：再分发或基于 deckify 二次开发时必须保留 LICENSE 文件。

如果不确定你的使用是不是「非商用」，请在 GitHub 提 issue 询问。

---

## 致谢

由 **Xichang (Seacen) Zhao** 创建 —— [github.com/seacen](https://github.com/seacen)。

Engineering DNA 提炼自数次失败的 slide。`references/ds-template.md` 里的每一行都来自一次真实的生产 bug。

---

## One more thing —— 一封写给 AI 时代的信

留意一下刚才发生了什么。你没打开 PowerPoint。你没挪过一个文本框。你没和模板较劲。PPT 是**为「人手绘」而设计的** —— 每个方块、每段渐变、每行间距，都靠手摆。这在过去五十年里讲得通。

但 slide 的制作方式变了。slide 不再被「画」出来，它们被**想象出来、描述出来**。创作者已经从人变成了 AI，而 AI 的母语不是 `.pptx` 二进制 —— 是 HTML。活的标签、可动画、可被查询、可被改写、可粘贴进任何对话。PPT 拖慢 AI 的地方，HTML 让 AI 跑起来。

deckify 存在的意义就在这里。它不是「一个更好的做 slide 的工具」 —— 它是**让 AI 能做 slide 的那份资产**，在 AI 与生俱来的媒介里。把品牌的规范建一次；之后每一份 deck，都让 AI 来写。

欢迎来到 AI 时代的 deck。

—— deckify
