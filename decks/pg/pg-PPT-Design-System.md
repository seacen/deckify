# P&G-PPT-Design-System

> 为 P&G 制作的所有 deck 共用的视觉语言。请严格遵循，让每一份新 deck 都一眼被识别为同一家族。

---

<!--
  TEMPLATE NOTES (delete this comment block in the generated output):

  Sections marked <!-- BRAND-VARIABLE --> must be filled with brand-specific content.
  Sections marked <!-- ENGINEERING-DNA --> must be copied verbatim. They came from
  real, painful bugs in production decks. Do NOT "simplify" or "trim" them — every
  line earns its place.

  Placeholder syntax: TOKEN. Replace each from $WS/decisions.json.
-->

## 1. 设计理念

<!-- BRAND-VARIABLE: 1-2 paragraphs capturing the brand's mood + a "Constraints vs Freedom" block -->

**保留 P&G 1837 年起就在用的视觉气质：饱和的 Pantone 286 深蓝画布、白色 Montserrat 大标题、标题以 **句号** 收尾的标志性印刷修辞、纪实摄影的真实人物镜头。每一张 slide 都应该让人秒认是 P&G —— 不是某家「现代简洁」的科技公司，而是一家把日常用品做了 187 年、被 Fortune 评为最具创新力公司的全球 CPG 巨头。美学坐标：corporate scientific optimism；参考 IBM 企业沟通、Unilever 年报、Johnson & Johnson editorial。**

> 可参考的 mood 段落示例（挑一个最贴近的、混合或改写后再用）：
> - **奢侈品 / 编辑 / 字体主导**："借鉴奢侈品牌传播语言：慷慨的留白、高对比的字体、克制的颜色。每个元素都凭功能存在。不要装饰性渐变、不要 stock icon、不要 emoji。"
> - **工程感 / 网格驱动**："像开发者文档站点一样组织：紧凑网格、monospace 强调、可复制的 code block、大量克制的灰度配一个强 accent。"
> - **大胆色彩 / 消费向**："高能量、高饱和度、英雄字体、大块插画形状。留白是为了让颜色更亮，不是为了降低噪音。"
> - **极简单色**："还原性强、近单色调色板、accent 仅用于强调，字体承担所有视觉重量。"

**两种模式：**
- **桌面端 (≥ 769 px)**：1280 × 720 px 画布，运行时 scale-to-fit (§5)，键盘/点击导航。
- **移动端 (≤ 768 px)**：所有 slide 垂直堆叠成一张可滚动的长页；单栏布局。

### 设计品味 <!-- ENGINEERING-DNA: design-taste -->

**承诺一个清晰的审美立场。** 本 DS 是品牌工具，不是 SaaS 通用模板。基于它做的每一份 deck 第一眼就该让人认出这是 *该品牌* — 不是"又一份得体的商务演示"。极致繁复与极致简约都能成立；失败模式是中庸。

**反 AI 套路规则**（每张 slide、每个组件、每个变体都适用）：

- **不用通用字体默认值。** 品牌字体在 §3 已指定，必须使用。需要 fallback 时也应选最有辨识度的，不能把 Arial / system-ui 当做"设计选择"。
- **不用陈词滥调的配色。** 纯白底 + 一个紫/蓝色 accent + 板岩灰字 = AI 套路签名。§2 调色板有主导和弦与辅助 accent — 按层级使用，不要扁平化成"白+灰+一种 accent"。
- **不用等权重的多色装饰网格。** 6 个等权 accent 看起来像 Storybook 配色矩阵，不像品牌。一个主导和弦 + 2–3 个语义 accent（含明确含义）才是正确形态。
- **不用现成 SaaS 仪表盘 chrome。** 每个组件都 8 px 圆角 + 柔和 drop-shadow + 整齐间距，会把所有品牌做成一个样。按 §2 匹配品牌实际的圆角 / 阴影 / 密度。
- **不用空洞的氛围词。** "现代、简洁、大胆"什么都形容因此什么都不形容。Slide 标题和段落文案应该具体、具象。
- **一个编排好的入场动效，而非分散的小动画。** 大部分 slide 只需要一次激活时的内容错时显现；不要给每张卡都加 hover 抖动。

### 约束 vs 自由 <!-- ENGINEERING-DNA framing; bullet contents are BRAND-VARIABLE -->

本 Design System 定义了 **硬约束**（永远不能破的）与 **可复用组件**（按需选用的）。它不定义现成配方 — 每张 slide 都应为它自己的内容构图，而不是从模板拼接。

**硬约束（锁死）：**
- Colour palette (§2 tokens only — no ad-hoc colours)
- Montserrat typeface, no serif/display fonts （不混 Inter / Roboto / 系统字体；P&G 公开站点的实测渲染就是单 Montserrat 家族）
- 12 px 可读性下限
- 每一张 slide 都必须有 logo
- **每张 slide 的内容必须包在一个 `.sc` 容器里**（即使是 bespoke 满屏的 Type J / Type A 也是）。`.sc` 是 `fit_contract_intact` 唯一扫描的位置 — bespoke 布局如果直接画在自定义 shell 里，会**静默绕过** absorber 检测、移动端 catch-all、602 px 预算这三道保险。没有 `.sc`，就没有契约。
- **Logo `<symbol>` 内部不能含任何 `fill` 属性**（包括 wrapper `<g>` 上的 `fill="none"`）。任何内层 fill 都会盖过 `currentColor` 级联，使 wordmark 完全不可见 —— 而 byte 级检查（path d 长度、viewBox、visible_on_cover）会一切显示 PASS。`embed_logo.py` 在物化时已 strip 这些；`logo_renders` hard check 会拒绝任何漏网的。
- 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 和几何指示符允许
- 不用装饰性 stock photography
- `.shd` header strip on content slides
- `.sw` border-left accent

**可复用组件（按需选用，不强制）：**
- §7 组件库提供卡片、表格、图表、标签、标记 — 适合时用，不适合时跳过用 bespoke 布局。

**Bespoke 元素（鼓励）：**
- **在调色板内自由发挥。** 比如：用「类目色点」作为标题左侧的小圆点（橙=创新、蓝=品牌、绿=可持续），用「标题以句号收尾」作为印刷签名，用 Pantone 286 深蓝整版做章节封页 —— 这些都是 P&G 官网真实的视觉调性，可以在 token 体系内自由组合，但不要为了「现代」而把它们抹平。
- 判定标准是：该元素是否只用了定义过的颜色 token、品牌字体、并尊重可读性下限？如果是，即便不匹配任何具名组件也算"在系统内"。
- **不要自我限制在具名组件里。** 如果某 slide 需要 §7 不存在的东西，就从 token 出发自己造。最好的 slide 都是从系统 token 出发的 bespoke 构图。

---

## 2. 颜色令牌 <!-- BRAND-VARIABLE: hex values + brand-palette names; core role token names are invariant -->

颜色 token 系统有三层：

1. **核心角色 token** — 所有品牌之间名字不变。它们标识颜色 *扮演什么角色*，而不是 *它是什么颜色*。红色品牌的 `--primary` 是红色；蓝色品牌的 `--primary` 是蓝色。
2. **语义 token** — 所有品牌之间名字不变；编码含义（正向 / 负向 / 警告 / 信息）而不是颜色身份。
3. **品牌调色 token** — 品牌特有的名字 + hex。这些是品牌实际用到的额外 accent（如 Unilever 的 `--lilac` 和 `--water`、P&G 的 `--spark`、Stripe 的 `--lavender`）。命名按品牌实际叫法 — Phase 1 时从 `brand.json` 抓取。

```css
:root {
  /* ── Core role tokens (invariant names) ── */
  --primary:  #003DA5;   /* Dominant brand chord — cover bg, primary mark colour */
  --accent:   #E87722;   /* CTA / link / single saturated highlight */
  /* ── Neutrals ── */
  --surface:  #FFFFFF;   /* Paper / slide bg */
  --white:    #FFFFFF;
  --ink:      #0B1220;   /* Body text on light surfaces */
  --mid:      #5B6573;   /* Secondary text / muted labels */
  --rule:     #E1E5EB;   /* Dividers / hairlines */
  --tint:     #F2F7FF;   /* Subtle row / section bg */
  /* ── Semantic (invariant names; values may map to brand-palette colours) ── */
  --green:    #97D700;   /* Positive */
  --green-bg: #F0F7E0;
  --red:      #C8102E;   /* Negative */
  --red-bg:   #FBE9EC;
  --warn:     #E87722;   /* Warning / caution */
  --warn-bg:  #FCEFE3;
  --teal:     #00A3E0;   /* Informational / neutral highlight */
  --teal-bg:  #E0F4FB;
  /* ── Brand palette (brand-specific names; expanded from brand.json accents+neutrals) ── */
  /* P&G 专有令牌 */
  --pg-cyan:        #00A3E0;   /* 浅蓝高光（年报、品牌卡） */
  --pg-tint:        #F2F7FF;   /* 极浅蓝底纹，区分行/卡片 */
  --pg-ink-soft:    #0F5780;   /* 二级深蓝文案，封面副标 */
  --pg-warm:        #E87722;   /* 创新章橙色类目点 */
  --pg-green:       #97D700;   /* 可持续章绿色类目点 */
}
```

**规则：** <!-- ENGINEERING-DNA -->
- **Token 名是角色抽象，不是颜色名。** `--primary` 是品牌的主导和弦，不论那是 navy / red / yellow / black。Slide CSS 读 `var(--primary)` 就能拿到当前 brand DS 对应的正确颜色。
- **每张 slide 只有 *一个* 主导 accent 颜色。** 用 `--accent` 做 slide 的标志性高亮（CTA、callout 边线、chart 主条）。品牌调色 token（如 `var(--lilac)`）是按需取用的装饰，不是并行 accent — 一张 slide 最多用一个装饰性品牌色。
- **语义颜色仅在含义彼此独立、相对时才同时出现** — 例如一张对比 slide 的 ✓ (`--green`) / ✗ (`--red`)。否则只取一种。
- **`--tint` 用于行底色，不用于卡片填充。**
- **永远不用纯黑。** `--primary` 是品牌真实的深色；如果品牌没有深色，用 `--ink` 作为本会用到黑的位置。
- **永远不在 slide CSS 里写临时 hex。** 每个颜色都必须来自 token（核心 / 语义 / 品牌调色）。`token_only_colors` hard check 会强制执行。

---

## 3. 字体 <!-- BRAND-VARIABLE: font family + fallback; the scale below is mostly invariant -->

**Montserrat** — 唯一字体。字重 300 / 400 / 600 / 800（300 提供 italic 用于封面副标）。`system-ui` 作为 极小尺寸下的兜底；webfont 加载失败时整体降级。

> P&G 的字体哲学是「单字族 + 重字重 + 全大写小幅 + 句号收尾」。Montserrat 的几何骨架配合 800 字重，刻出的是企业气质；不要为了花哨混入 serif 或 display。**章节大标题强制以句号结束（'Innovation.'、'Brands.'、'Sustainability.'）—— 这是 P&G 排印的视觉签名。**

### CJK 字体回退链 <!-- ENGINEERING-DNA: cjk-fallback -->

中文 deck 不能直接用拉丁字体当 body font。Century Gothic / Helvetica Neue / SF Pro / Stripe Sans / Georgia 等都不含 CJK 字形，浏览器对 CJK 字符自动回退到系统默认（macOS 上是 STHeiti 细体，Windows 是微软雅黑 Light），**视觉上立刻显得廉价**。

**最低要求**：font-family 链里**必须至少出现一个 CJK 字体名**（PingFang SC / Hiragino Sans GB / Microsoft YaHei / Source Han Sans 等），否则 CJK 字符 100% 落到 OS 默认。`cjk_font_quality` hard check 会强制执行这一条。

**两种合理的字体顺序**（按 deck 的语言比例选）：

1. **CJK-first**（推荐用于中文密度高的 deck）：CJK 字体放最前，拉丁 brand 字体兜底。中英混排时 PingFang 的拉丁补丁会渲染英文，整体风格最统一，中文不会因为字重不匹配显得瘦弱。
2. **Latin-first**（适用于 brand 拉丁字面强、deck 大量英文术语的场景，如 Stripe API 文档风格）：拉丁 brand 字体放前，CJK 字体跟在后面。CJK 字符会走 CJK 字体，但拉丁部分保留 brand 表达。`cjk_font_quality` 在这种情况下会带 `warning`（不阻断），由 vision judge 决定视觉是否可接受。

```css
/* 中文 deck 推荐字体链 — CJK 优先，拉丁兜底 */
font-family:
  /* macOS / iOS 中文（最高优先级 — 对中英都比 brand-latin 干净） */
  'PingFang SC', '苹方-简',
  /* macOS 较旧 / 阅读体严肃面 */
  'Hiragino Sans GB', '冬青黑体简体中文',
  /* Windows 中文 */
  'Microsoft YaHei', '微软雅黑',
  /* Linux / Android / 通用 */
  'Source Han Sans SC', 'Noto Sans SC', 'Noto Sans CJK SC',
  /* Brand 拉丁字体 — 仅作 brand-mark / display 修饰 */
  '[BRAND-LATIN]',
  /* 系统通用 */
  system-ui, -apple-system, sans-serif;
```

**Sans-serif brand**（Unilever / Stripe / Apple / P&G）→ 配 PingFang SC / Microsoft YaHei / Source Han Sans 这类 sans CJK 字体。
**Serif brand**（Coca-Cola Georgia / 编辑感品牌）→ 配 `'Songti SC', '宋体-简', 'Source Han Serif SC', 'Noto Serif SC'`，否则 Georgia + 黑体的混搭会跳戏。

**字重提升（CJK-first 时尤其重要）**：PingFang SC 的 Regular（400）较细 — 大字标题用 700（Semibold/Bold），正文用 500（Medium）以上，避免"中文显瘦"的廉价感。

**禁止**：font-family 链里完全没有 CJK 字体。`cjk_font_quality` hard check 会立刻 FAIL。

### 字号阶梯 <!-- ENGINEERING-DNA — sizes are invariant; the scale is what makes decks readable -->

| 用途 | 字号 | 字重 | 字距 | 备注 |
|---|---|---|---|---|
| 封面大标 | 82 px | 900 | −0.03 em | 行高 0.98 |
| 封面副标 | 22 px | 300 斜体 | +0.01 em | |
| 内页标题 | 50 px | 900 | −0.025 em | 行高 1.06 |
| 内页副标 | 20 px | 600 | +0.01 em | `--mid` |
| Eyebrow / 徽章 | 11–12 px | 800 | +0.18–0.24 em | 全大写 |
| 卡片标题 | 28 px | 900 | −0.01 em | |
| 正文 / 列表 | 16 px | 600 | 默认 | 行高 1.5–1.6 |
| 表格 / 数据 | 13–14 px | 700–800 | +0.1 em | 全大写 |
| 说明 / 元信息 | 12–13 px | 700–800 | +0.14 em | 绝不低于 12 px |

### 可读性 <!-- ENGINEERING-DNA -->

1. **最大化**：默认用合适的最大字号。半空 slide 配 14 px 正文 = 设计失败。
2. **Floor**: Nothing below 12px <!-- ENGINEERING-DNA: typography-floor -->. If content doesn't fit at min sizes, change layout — never shrink font.

| 用途 | 最低 | **强制默认** |
|---|---|---|
| 内页标题 | 38 px | **50 px** — 仅在密内容多行时降到下限 |
| 卡片标题 | 22 px | **28 px** |
| 主正文 / 列表 | 14 px | **16 px** — slide 级段落、主要内容 |
| 组件次级文字 | 13 px | **13–14 px** — 卡片内描述、列表条目细节、组件标题下的辅助文字 |
| 副标 | 16 px | **20 px** |
| 徽章 / 标签 | 12 px | **13 px** |

**强制规则**：slide 主内容区域的标题低于 50 px、主正文低于 16 px 都是 bug。组件内部的次级文字（卡片描述、列表细节）可用 13–14 px，以维持组件内部标题与描述之间的视觉层级。

### 3.1 字体安全 <!-- ENGINEERING-DNA: typography-safety -->

Slide "好看"是可工程量化的。下面的规则是硬规则；`text_layout_safe` 自动检查执行其中大部分。

1. **永远不要贴底**：内容页最底的可见文字元素到 slide 底边距离必须 ≥ 18 px（目标 24–48 px）。`.sw` / `.sc` 的 `padding-bottom` 当做防线；不要把内容推到边缘。
2. **永远不能截断**：任何 `overflow:hidden` 的文字容器必须满足 `scrollHeight ≤ clientHeight`。如果内容可能溢出，用 `text-overflow: ellipsis` 或 `-webkit-line-clamp` 显式声明最大行数 — 永远不要"赌"它正好放得下。
3. **永远不要任意换行**：H1/H2/H3 单标题 ≤ 3 行；正文段落 ≤ 5 行。中日韩标题避免在词语中间换行 — 用 `word-break: keep-all; line-break: strict;` 配合更短文案，不要让自动换行接管。
4. **全局布局法则**（基础）：
   - 全局禁用 `hyphens: auto`（混合 CJK 环境会产生破碎连字符）。
   - 正文 `line-height` ≥ 1.4，标题 ≥ 1.15 — 不能更紧。
   - 卡片 / 段落之间至少 12 px 间距（与 §5 的 12 px 下限一致）；两个文字块永远不能相触。
   - 一个 `.sc` 内层级最多 3 层（标题 → 副标 / 图 → 列表 / 卡片）。需要更多就拆 slide。
5. **构建时自检**（写完 HTML 后运行）：
   ```js
   document.querySelectorAll('.slide').forEach((s, i) => {
     const slideBottom = s.getBoundingClientRect().bottom;
     let maxBottom = -Infinity;
     s.querySelectorAll('h1,h2,h3,h4,p,li').forEach(el => {
       if ((el.textContent||'').trim().length < 3) return;
       const r = el.getBoundingClientRect();
       if (r.height > 0) maxBottom = Math.max(maxBottom, r.bottom);
       if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow === 'hidden')
         console.warn(`slide ${i+1}: ${el.tagName} text truncated →`, (el.textContent||'').slice(0,40));
     });
     const gap = slideBottom - maxBottom;
     if (gap < 18) console.warn(`slide ${i+1}: text only ${gap.toFixed(1)}px from bottom (need ≥ 18)`);
   });
   ```
6. **检查失败时的修复优先级**：
   - 首先，**改文案**（删字、缩短句子、用名词短语）。
   - 然后，**改布局**（去掉一项、拆分 slide、把列表改成双栏网格）。
   - **永远不要** 通过把字号缩到 12 px 以下或允许截断来"塞下"。

---

## 4. P&G Logo <!-- BRAND-VARIABLE: SVG payload is brand-specific; surrounding pattern + multi-format support is ENGINEERING-DNA -->

### P&G 的 logo 选择：为什么是 PNG 而不是 SVG

P&G 的官方 logo（`P_G_Logo_RGB.svg`）是 **径向渐变的圆形徽章** —— 深蓝→浅蓝渐变背景 + 白色 P&G 字形 + 高光遮罩。它在视觉上是 P&G 187 年品牌资产的核心，**不能** 被简化成单色 wordmark。

但工程上，这个 logo **不能走 Form A（SVG `<symbol>` + `currentColor`）** 路径：

- DS 的 `logo_renders` hard check 要求 `<symbol>` 内层只用 `fill="currentColor"`，目的是支持白底/深蓝底两种翻转色（`.logo.W` / `.logo.L`）。
- 但 `<radialGradient stop-color="..."/>` 和 `<path fill="url(#SVGID_1_)"/>` 的颜色是 **硬编码进 gradient stops 的**，CSS 的 `currentColor` 级联无法覆盖它们。
- 强行 strip 内层 fill 会让圆环和字形塌成同一色 —— 得到一团纯色 blob，不再是 P&G。

所以对于 P&G（以及任何 gradient 徽章型 logo —— 比如 Starbucks 双色咖啡女神、Mastercard 红黄圆环），**Form B（PNG base64 内嵌）才是正确路径**。Form B 用 `<image href="data:image/png;base64,...">` 包进同一个 `<symbol>`，渲染时把彩色徽章作为完整位图盖在 chip 上。

### 定义（每份 HTML 一次）

**A. SVG 矢量路径**（**P&G 不用此路径** —— 仅在你的 brand wordmark 是单色矢量字形时才用）：

```html
<svg style="display:none" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 720 720" fill="currentColor">
    <radialGradient id="SVGID_1_" cx="156.09" cy="143.71" r="661.27" gradientTransform="translate(-6 -6) scale(1.0167)" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#00a1df"/>
    <stop offset=".13" stop-color="#0092d7"/>
    <stop offset=".37" stop-color="#006cc1"/>
    <stop offset=".62" stop-color="#003da6"/>
    <stop offset=".73" stop-color="#043799"/>
    <stop offset=".93" stop-color="#102777"/>
    <stop offset="1" stop-color="#152169"/>
  </radialGradient>
  <circle cx="360" cy="360" r="360"/>
  <radialGradient id="SVGID_2_" cx="107.95" cy="60.5" r="1096.43" gradientTransform="translate(-6 -6) scale(1.0167)" gradientUnits="userSpaceOnUse">
    <stop offset=".02" stop-color="#fff"/>
    <stop offset=".03" stop-color="#fbfeff"/>
    <stop offset=".09" stop-color="#bae7f9"/>
    <stop offset=".14" stop-color="#87d5f4"/>
    <stop offset=".19" stop-color="#63c9f1"/>
    <stop offset=".23" stop-color="#4cc1ef"/>
    <stop offset=".26" stop-color="#44beee"/>
    <stop offset=".28" stop-color="#37b8eb"/>
    <stop offset=".35" stop-color="#19ace5"/>
    <stop offset=".41" stop-color="#07a4e0"/>
    <stop offset=".45" stop-color="#00a1df"/>
    <stop offset=".79" stop-color="#0045ab"/>
    <stop offset=".82" stop-color="#003da6"/>
    <stop offset=".96" stop-color="#0059b6"/>
  </radialGradient>
  <path d="M95.6 359.9C95.6 195 199.7 54.4 345.8.3 153.6 7.8 0 165.9 0 360c0 194.3 153.9 352.6 346.4 359.7C200.1 665.7 95.6 525 95.6 359.9z"/>
  <defs>
    <filter id="Adobe_OpacityMaskFilter" width="346.4" height="719.4" x="0" y=".3" filterUnits="userSpaceOnUse">
      <feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"/>
    </filter>
  </defs>
  <mask id="SVGID_3_" width="346.4" height="719.4" x="0" y=".3" maskUnits="userSpaceOnUse">
    <g filter="url(#Adobe_OpacityMaskFilter)">
      <radialGradient id="SVGID_4_" cx="302.95" cy="349.21" r="381.37" fx="2.18" fy="354.33" gradientTransform="matrix(.03136 -1.0162 1.0341 .03192 -68.63 645.74)" gradientUnits="userSpaceOnUse">
        <stop offset=".1" stop-color="#fff"/>
        <stop offset=".35" stop-color="#fdfdfd"/>
        <stop offset=".45" stop-color="#f6f6f6"/>
        <stop offset=".51" stop-color="#eaeaea"/>
        <stop offset=".57" stop-color="#d9d9d9"/>
        <stop offset=".62" stop-color="#c3c3c3"/>
        <stop offset=".66" stop-color="#a7a7a7"/>
        <stop offset=".7" stop-color="#868686"/>
        <stop offset=".73" stop-color="#606060"/>
        <stop offset=".77" stop-color="#353535"/>
        <stop offset=".8" stop-color="#060606"/>
        <stop offset=".8"/>
      </radialGradient>
      <path d="M95.6 359.9C95.6 195 199.7 54.4 345.8.3 153.6 7.8 0 165.9 0 360c0 194.3 153.9 352.6 346.4 359.7C200.1 665.7 95.6 525 95.6 359.9z"/>
    </g>
  </mask>
  <radialGradient id="SVGID_5_" cx="281.36" cy="290.9" r="445.49" gradientTransform="translate(-6 -6) scale(1.0167)" gradientUnits="userSpaceOnUse">
    <stop offset=".32" stop-color="#44beee" stop-opacity="0"/>
    <stop offset=".48" stop-color="#2b99d9" stop-opacity=".27"/>
    <stop offset=".67" stop-color="#1476c6" stop-opacity=".58"/>
    <stop offset=".82" stop-color="#0561ba" stop-opacity=".84"/>
    <stop offset=".92" stop-color="#0059b6"/>
  </radialGradient>
  <path d="M95.6 359.9C95.6 195 199.7 54.4 345.8.3 153.6 7.8 0 165.9 0 360c0 194.3 153.9 352.6 346.4 359.7C200.1 665.7 95.6 525 95.6 359.9z" mask="url(#SVGID_3_)"/>
  <g>
    <path d="M353.9 325.7c23.9-58.9-20.8-74.9-49.9-74.9h-96.4c8 5.5 6.7 12.8 5.1 17.3l-56.2 179.5c-2.2 7.1-10.6 14.6-15.1 15.7h78c-4.3-.8-10.4-6.9-8.2-15.2l20.4-64.9c.1 0 93.9 12.7 122.3-57.5zm-75.8-58.4c10.2 0 38.5 1.4 20.2 54.9-19.1 56.2-61.5 44.6-61.5 44.6l31.2-99.5h10.1z"/>
    <path d="M416.3 463.4h52.5c-16.8-5.4-41.6-21.3-51.5-32.6 8-8.7 17.9-19.7 19.7-42h-27.2s5.2 3 5.2 9.4c0 5.9-2.4 14.1-7 19.8-8-11.8-16.5-25.3-19.5-45.1 10.7-5.3 25.7-11.1 37.6-21.5 11.3-9.9 13.9-19.3 14.1-25.4v-.8c0-6.4-2.5-12.4-7.1-16.9-7.9-7.8-20.3-11-33.4-8.6-10.5 2-19.4 7.6-23.9 11.7-15.8 14.9-17.8 39.4-17.8 50.5 0 2.7.1 4.7.2 5.9-.9.4-2.5 1-2.5 1-11.6 4.3-42.5 12.5-53.5 37.9-1.4 3.2-3.4 10.2-3.4 18.3 0 7 1.5 14.8 6 21.9 7.8 12.2 21 19.9 42.2 19.5 23-.4 45.7-16.1 49.7-19 3.9 3.7 14.2 13.4 19.6 16zm0-142c-2.7 17.1-24.9 34.4-30.3 36.7-1-9.6-.5-24.8 7.5-37.2 5.3-8.2 12.4-11.8 18.1-9.8 4.6 1.6 5.1 5.8 4.7 10.3zm-30.8 114.4c-3.1 1.9-15.3 8.1-26.7 9.2-10.6 1-28.2-3.1-28.1-24.3 0-18.1 19.7-31.4 30.4-36 4.3 17.5 14 37.3 24.4 51.1z"/>
    <path d="M575.8 267.5c31.2-7.5 56.9 16.9 59.2 18.6l8.9-28.3c-12.3-3.7-101.8-34-165.1 38.2-38.9 44.4-48.4 135.4.9 159.8 52.8 26.1 111.1-4 115.4-6.1l24.1-76.8c2.6-9.3 8.5-15.3 18.9-19.2h-83.8c12.2 5.1 11.3 14.3 10.4 18.1l-24.1 76.8c-3.2.6-70.6 17.4-32.9-100.5 8.3-25.3 31-71.7 68.1-80.6z"/>
  </g>  <!-- 内层 <path>/<g> 不能携带任何 fill 属性，currentColor 才能级联进来。
                                 详见下方 "fill 级联陷阱"。 -->
  </symbol>
</svg>
```

> ⚠️ **fill 级联陷阱** <!-- ENGINEERING-DNA: logo-inner-fill -->
> 很多品牌站点的 SVG 导出器会把真实字形 path 包在一个默认组里：
> `<g fill="none" fill-rule="evenodd"><g><path d="..."/></g></g>`。原样粘贴进我们的
> `<symbol fill="currentColor">` 会让内层 `fill="none"` **赢过** 父级 currentColor 级联 ——
> wordmark 渲染出来 **100% 不可见**，而 byte 级检查（path d 长度、viewBox、
> `visible_on_cover` 通过 getBoundingClientRect）全都会显示 PASS。
> **在 embed 前必须 strip 所有内层 `fill` 属性，包括 `fill="none"`。**
> `embed_logo.py` 会自动 strip；如果你手工粘贴 logo，必须手工 strip。
> `logo_renders` hard check 会拒绝任何不是 `fill="currentColor"` 的内层 fill。

**B. PNG/JPG/WebP base64 内嵌**（位图 fallback） — 仅有位图 logo 时（最小 64×64），base64 编码后通过 `<image href>` 包进同一个 `<symbol>`：

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 720 720">
    <image href="data:image/png;base64,<!-- N/A — P&G uses SVG vector form A above; raster fallback unused -->" width="720" height="720"/>
  </symbol>
</svg>
```

> ⚠️ **禁止用文字 placeholder 伪装 logo**：用品牌名 `<text>` 假冒 logo（如 `<text>P&G</text>`、字母圆盘）属于构建失败。`logo_renders` hard check 会拒绝只含 `<text>` 的 `<symbol>` 块。如果没有任何来源能产出真实 logo，**停下来向用户索要原始文件** — 永远不要编造 placeholder。

来源解析顺序（`embed_logo.py` 实际尝试的顺序）：
1. 页面 `<header>` 中的 inline SVG（过滤掉 viewBox < 60 px 的实用图标）
2. 品牌的 Wikipedia infobox logo 文件
3. apple-touch-icon（通常 ≥ 180 px PNG）
4. favicon（SVG 或 PNG）
5. og:image / twitter:image
6. 常见路径猜测（/logo.svg、/assets/logo.svg ……）

### 用法

```html
<!-- 白色（深色 slide 上） -->
<svg class="logo W" viewBox="0 0 720 720" aria-label="P&G">
  <use href="#brand-wm"/>
</svg>

<!-- 品牌深色（浅色 slide 上） -->
<svg class="logo L" viewBox="0 0 720 720" aria-label="P&G">
  <use href="#brand-wm"/>
</svg>
```

```css
/* fill: currentColor 必须放在 .logo 上 — 不要放在 .logo path 上。
   CSS 选择器无法穿透 SVG <use> 的 shadow DOM。
   外层 <svg> 上的继承 fill 才能正确级联进去。 */
.logo   { height: 44px; width: auto; flex-shrink: 0; fill: currentColor; }
.logo.W { color: #fff; }
.logo.L { color: var(--primary); }
```

### 摆放规则 <!-- ENGINEERING-DNA -->
- **每张 slide** 都必须有 logo — 封面与所有内容页。
- **封面**：`.cov-top` flex 行的右上角。
- **内容页**：`.shd` 页头条的右端（左 = 标题 eyebrow / slide 编号，右 = logo）。
- Logo 周围最小留白 = logo 高度（44px）四周都留。
- 不要拉伸、不要在 `W`/`L` 之外重新着色、不要把 logo 叠在带图案的区域上。

> **P&G logo 的特殊性**：官方 P_G_Logo_RGB.svg 是带 radialGradient 的圆形徽章 （深蓝 → 浅蓝径向渐变 + 白色 P&G 字形），所以 `currentColor` 翻转不会影响渐变 stop-color。
> - 在 **白色 / 浅蓝底** 上：直接用 `<svg class="logo L">` —— 圆徽章本身就是品牌标志的天然形态，最佳显示场景。
> - 在 **深蓝 / 深色底** 上：用 `.logo.W` 类配合 `filter: drop-shadow(0 0 1px rgba(255,255,255,.6))` 给徽章一圈极细白描边，防止徽章外圈深蓝与背景融合；或在封面专用 `.cov-mark` 类里把徽章包在 36px 白色圆形 chip 内（白底徽章）。

---

## 5. 幻灯片架构 <!-- ENGINEERING-DNA — the entire section, invariant -->

### 脚手架
```
#wrap — fixed fullscreen, flex-centre, background: var(--ink)
  #deck — 1280 × 720, position:relative, overflow:hidden (hard contract)
    .slide × N — absolute inset, opacity show/hide, overflow:hidden (hard contract)
```

`#wrap` 与 `body` 的 background **必须用 `var(--ink)`**，不能写死 `#000` / `#1A1A1A` / `#1F1F22` — 这些会被 `token_only_colors` hard check 抓到。每个 brand 的 `--ink` 已经是各自真实的深色基调（Coca-Cola 纯黑、Unilever warm graphite、Apple near-black），letterbox 跟随它就是对的。

### 全屏适配 — 运行时缩放 <!-- ENGINEERING-DNA: scale-to-fit -->

The deck is a **fixed-size 1280×720 canvas** at the DOM level. To fill any viewport without black borders, scale at runtime via CSS transform — never resize the canvas itself. This keeps every measurement, every fit-contract calculation, every `offsetWidth` value invariant; the auto-eval and the visual reality both stay coherent.

```css
/* Required CSS hooks */
#deck { transform-origin: center center; will-change: transform; }
```

```html
<!-- Required JS at the end of <body>; runs on load + resize -->
<script>
(function () {
  var deck = document.getElementById('deck');
  function scaleDeck() {
    if (!deck) return;
    if (window.matchMedia('(max-width: 768px)').matches) {
      deck.style.transform = 'none';
      return;
    }
    var s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    deck.style.transform = 'scale(' + s + ')';
  }
  window.addEventListener('resize', scaleDeck);
  window.addEventListener('load', scaleDeck);
  scaleDeck();
})();
</script>
```

**Why a CSS transform and not a viewport unit on the canvas itself:**
- `transform: scale()` does not change `offsetWidth` / `offsetHeight`, so every layout calculation, fit-contract budget (602 px content area), and auto-eval measurement remains exact.
- A viewport-relative `width: 100vw` on the canvas would warp the type scale; a slide tuned for 50 px headlines becomes 38 px on a small laptop.
- Mobile is exempt: the mobile media query already turns the deck into a flow document, so `transform: none` is required there or the stacked slides scale with the canvas and break.

**Anti-pattern**: shipping a deck without `scaleDeck()` lets `#wrap`'s flex-centre place a 1280×720 deck inside a 1920×1080 viewport with 320 px / 180 px of dark border — the deck looks unfinished even when content is correct. Every brand DS must wire scale-to-fit into the verification deck.

### 显示状态
```css
.slide          { opacity: 0; pointer-events: none; transition: opacity .38s ease; overflow: hidden; }
.slide.active   { opacity: 1; pointer-events: auto; }
.slide.active .sc { animation: enter .42s cubic-bezier(.4,0,.2,1) both; }
```

### 内容页 (`.sw`)
```css
.sw { background: var(--surface); border-left: 3px solid var(--accent); display: flex; flex-direction: column; height: 100%; }
/* Default: symmetric padding. Override with asymmetric bottom pad for visible breathing room. */
.sw .sc { flex: 1; padding: 32px 80px 32px 96px; display: flex; flex-direction: column; overflow: hidden; }
```

### 页头条 (`.shd`) — 每张内容页都有
```css
.shd { display: flex; align-items: center; justify-content: space-between; padding: 0 80px 0 96px; flex: 0 0 54px; border-bottom: 1px solid var(--rule); }
.shd-num { font-size: 11px; font-weight: 800; letter-spacing: .2em; text-transform: uppercase; color: var(--accent); }
```

---

### 5.1 单页适配契约（来之不易，不可妥协） <!-- ENGINEERING-DNA: fit-contract -->

**避免所有"内容溢出 deck"bug 的那一条规则：** 内容页是 *固定大小的盒子*，不是滚动文档。每张 slide 都必须放进 720 px 之内并保留可见的底部呼吸空间。装不下就减内容 — 永远不要发布会剪裁或溢出的 slide。

#### 三层 overflow 安全网 <!-- ENGINEERING-DNA: three-layer-overflow -->

每张堆叠的内容页都必须在三个层级都带 `overflow: hidden`。多层防护：任何一层漏掉的，另一层都接得住。

```css
.slide   { overflow: hidden; }   /* Layer 1 — absolute stop at deck edge */
.sw .sc  { overflow: hidden; }   /* Layer 2 — content area stop */
.row-x   { overflow: hidden; }   /* Layer 3 — any flex:1 absorber inside .sc */
.card    { overflow: hidden; }   /* Layer 4 — any card with bounded height */
```

没有这些，一个超大的 bullet 会向外级联把 deck 推过 720 px。有了它们，最差情况只是剪裁 — 丑，但永远不会让布局崩坏。

#### 内容高度预算（记住这个算式）

对于一张默认 54 px 页头条 + 对称 32 px 上下内边距的标准内容页：

```
Deck height         720 px
− header strip      54 px
− top padding       32 px
− bottom padding    32 px
─────────────────────────
= content area     602 px   ← all section heights + gaps must fit in here
```

如果用非对称 padding（上 24 / 下 40）创造可见的底部呼吸空间：

```
Deck 720 − 54 − 24 − 40 = 602 px content area
Visible bottom margin from deck edge = 40 px (from padding) + any flex spacer
```

**写 HTML 前，先把计划的段高 + 间距加起来。** 总和超过 602 px 就删内容。不要把字号缩到 12 px 下限以下。不要赌浏览器"会自己处理"。数字不会撒谎。

#### "单 flex:1 absorber" 规则

`.sc` 内 N 个区段的垂直堆叠中，**必须恰好有一个** 区段吸收剩余空间。其余都是自然高度。

```html
<div class="sc">
  <div class="hero">     <!-- flex: 0 0 auto — natural height -->
  <div class="tl-wrap">  <!-- flex: 0 0 auto — natural height -->
  <div class="row-top">  <!-- flex: 1 1 0; min-height: 0; overflow: hidden — absorbs remaining -->
  <div class="row-risk"> <!-- flex: 0 0 auto — natural height -->
</div>
```

**Why:** With one absorber, total height = always exactly 602 px. Zero is wrong (content collapses). Two+ absorbers race for space and one gets squashed. Exactly one is the only stable configuration.

The absorber MUST carry `min-height: 0` (so it can shrink below its content's natural size) AND `overflow: hidden` (so its children clip instead of pushing it taller). Both are required — missing either breaks the contract.

#### 非对称下内边距 — 看得见的呼吸空间

Default `.sc` padding is symmetric `32 80 32 96`. For weekly-status / progress-report slides where the audience reads top-down and the bottom edge carries visual weight, prefer:

```css
.sw .sc { padding: 24px 80px 40px 96px; }   /* 24 top / 40 bottom */
```

The extra bottom padding creates deliberate visible breathing — roughly half a section-gap worth — between the last content block and the deck edge. This reads as "composed" rather than "crammed."

#### 编写前清单（写 HTML 之前做）

1. **List your sections** and assign each a role: `absorber` (exactly one) or `natural`.
2. **Estimate natural heights** using the type scale. A card with head (30) + label (14) + 5 single-line 13 px bullets (~125) + V-padding (34) = ~203 px.
3. **Sum fixed sections + gaps**. Confirm total ≤ (602 − absorber minimum) — the absorber needs at least ~160 px to hold meaningful content.
4. **Write the copy short enough that single-line bullets don't wrap**. In a half-width column at 13 px CJK, budget ~28 characters per bullet before wrapping.
5. **Render at 1280×720 and eye the bottom edge.** Not at 1920×1080 (the `transform: scale()` masks overflow by rescaling). The native canvas is the source of truth.

#### 导致 overflow 的反模式

- **N 个自然高度区段且没有 absorber**：总和超过 602 px，内容溢出 deck。漏了"一个 absorber"规则。
- **Absorber 缺 `min-height: 0`**：flex 拒绝把它压到内容自然高度以下，本规则就废了。
- **Absorber 缺 `overflow: hidden`**：超大子元素穿透 flex:1，把父容器挤破。
- **`.slide`/`.sc` 漏 `overflow: hidden`**：算式稍有偏差，内容就漏出 deck 渗到 body。安全网失效。
- **Packing 2 section labels + 5+ bullets into one card that gets ~240 px of flex:1 space**: natural content ~260 px, clipping guaranteed. Merge into one section, or cut bullets.
- **相信 1920×1080 渲染**：`transform: scale()` 等比例缩小所有内容 — 一份 730 px 的 deck 在 scaled 视图下看起来还行，但它 *已经坏了*。永远在原生 1280×720 验证。

---

## 6. 幻灯片类型 <!-- BRAND-VARIABLE: emphasis order varies; the type definitions are mostly invariant -->

> **Emphasis for P&G**: 用户选定特别突出 **Cover（深蓝大标题 + 句号）/ Data table & Chart（年报式硬数据）/ Pullquote（领导话语）** 三类。这三种 slide 是 P&G 视觉语言的核心载体，应当在 deck 中分配最大画面权重；其它类型仍要覆盖（DS 必须支持完整 slide 工具箱），但卡片密度可以更克制。
> Foreground these types when designing decks: Type A 封面、Type G 数据表 & Type H 图表、Type J 大段 pullquote.
> Use sparingly: Type E 多卡网格（>6 卡）、Type I 时间轴（仅当真有时间维度才用）.

### Type A — 封面
- 背景：`var(--primary)（深 P&G 蓝整版）`
- 结构：Logo 右上角 → Eyebrow → 巨型标题 → 斜体副标 → Meta 行
- **不允许任何装饰线** — 不要 hairline、不要 accent line、不要渐变边框。背景就是表面。

### Type B — 双栏内容
对比、特性列表、指标。`grid-template-columns: 1fr 1fr; gap: 20px`。移动端会折叠为单栏。

### Type C — 全宽叙事
单栏、大字号、配 pull-quote。用于上下文、摘要、推荐建议页。

### Type D — 翻面卡片
两张卡片并排。正面 = `--primary`，背面 = `var(--pg-ink-soft)`（比 `--accent` 柔和）。**Hover + 点击翻面** — JS `onclick` 切换 `.on` class（移动端必需）。正面有 ghost 罗马数字。背面留白宽（32 px padding，≤ 4 个内容元素）。

**字体 — 必须大而有力：**

| 元素 | Class | 字号 | 字重 |
|---|---|---|---|
| 正面标题 | `.cnm` | **28px** | 900 |
| 正面正文 | `.cbd` | **17px** | 600 |
| 正面提示 | `.ht` | 13px | 800 |
| 背面标签 | `.bkl` | 13px | 800 |
| 背面标题 | `.bkt` | **22px** | 900 |
| 对比标签 | `.vs .vt` | 13px | 900 |
| 对比正文 | `.vs .vb` | **16px** | 700 |
| 结论 | `.ccl` | **15px** | 600 |

**不要用 inline style 覆盖** 把 flip card 文字缩到这些字号以下。装不下就减项数 — 不要减字号。

### Type E — 数据/对比页
以表格或结构化数据网格为主体的 slide。用于特性对比、TCO 分析、规格矩阵。表格组件规范（§7.7）定义元素级设计；本类型定义何时用、以及如何在它周围布局。

**原则：** 表格是主角 — 标题 + 表格 + 底部可选一行 callout。不要有侧栏抢戏。如果表格有 6 列以上，让它占满整宽。

**Row-count rule** <!-- ENGINEERING-DNA: type-e-row-count -->
- 5 行是标准 14 px 行内边距（单元格 `padding: 14px 18px`）下的舒适行数。
- 6 行以上要么 (a) 把单元格内边距收紧到 `padding: 10px 16px`，要么 (b) 把数据拆到两张 slide。不要让 absorber 剪裁 — `text_layout_safe` hard check 会捕获。
- 如果表格既要 6 行以上 AND absorber 里又要侧栏 callout，那就拆开 — 不要硬塞。

### Type F — 图像页
一张或多张图占据 slide 主体，文字锚定在安静区域。用于展示真实产品 UI、真实截图、或将抽象概念具象化的环境照片。

**原则：**
- 图像必须服务于理解 — 不要装饰性 stock photo。优先：产品 UI 截图、真实数据可视化、能说明具体观点的环境照片。
- 构建 deck 时，**主动 web 搜相关图片**（产品 logo、UI 截图、现实案例）来支撑叙事。
- 图像处理：`border-radius: 4px`，可选 `1px solid var(--rule)` 边框。深色背景不需要边框。
- 布局：图像占 slide 区域 50–70%。文字放在旁边或叠在带 tint 的区域上。绝不在繁忙图片上直接放文字而不加 scrim。
- 图下说明：`.cap` 样式（13 px、字重 800、全大写、`--mid`）。

### Type G — 交互演示
嵌在 slide 内的自包含、点击推进的微体验。目的：让观众 *看到* 概念在工作，而不只是读它。

**何时用：** 场景演练、前后对比、多步流程可视化。

**结构：** 一块"屏幕"区域（深色 bg `--primary` 或 `#1a1a2e`，4 px 圆角）+ 点击推进的逐步内容。控件：前后按钮或带编号的步骤。内容通过 CSS transition 出现。

**设计规则：**
- 必须像精致的产品 demo，不是 prototype。整洁字体、克制动效。
- 只用 CSS `@keyframes` — 不用 JS 动效库。每个 demo 的 CSS 不超过 50 行。
- 每一步只承载一个清晰想法。每个 demo 最多 5 步。
- 移动端：滚动时自动推进，或点击目标 ≥ 44 px。

### Type H — 图表/数据洞察
由一个或多个数据可视化主导的 slide。用于定量论证、趋势分析、性能对比。图表组件规范（§7.8）定义元素级设计；本类型定义 slide 级原则。

**原则：**
- 每张 slide 一个主图。次要小图可接受 — 但必须直接支撑主图。
- 标题陈述洞察，不是图表类型。好："P&G 在三项维度都领先"。坏："柱状图对比"。
- 图表占 slide 区域 50–70%。剩余空间：标题 + 一段解读或一个 callout。
- 入场动效以增强叙事冲击力。

### Type I — 标签页
多个内容视图通过标签切换。当内容有自然分类时，能在一张 slide 上容纳更多信息。Tab 组件规范见 §7.9。

**原则：** 最多 4 个标签。每个 tab panel 都是自包含的"slide-中-slide" — 可以用 §7 任何组件。不要把标签当成 slide 内容塞太满的拐杖；如果 2 个标签各自都显稀疏，就合并成一个视图。

### Type J — 引言/抽词
一句强烈的话锚定叙事时刻。用于关键 takeaway、受众重置、可记忆的金句。

**结构（标准版）：** 大号引用文字（28–36 px、字重 700、`--ink`）居中或左对齐。可选下方署名（14 px、`--mid`）。左边 accent 边线（`3px solid --accent`）或无。

**结构（满屏 bespoke 变体）：** 部分品牌偏爱整张满屏 `--primary` + 多行海报型大字（如 Mars Five Principles 页：6 行 Inter Black 900 竖排，部分词用 `--accent` 或某个品牌色染色）。这种 slide：

1. **构图依然必须包在 `.sw + .sc` 里。** 用 `.sw`（覆写 `background: var(--primary)`）+ 一个 `.sc` 装自定义布局。**不要**自创平级 shell class（`.fpwrap`、`.poster-wrap` 等）—— bespoke shell 会**静默绕过** `fit_contract_intact`（没有 `.sc` = absorber 数 0 = `bad_slides: [{absorbers: 0}]`）。
2. **`.sc` 内必须恰好一个 absorber**，带 `flex: 1 1 0; min-height: 0; overflow: hidden` —— 通常是装大字的中间带。顶部 header 带和底部署名带都 `flex: 0 0 auto`。
3. **按行数反推字号上限。** absorber 的 `clientH` ≈ `(720 − 54 header − 32 top − 32 bottom) − 顶部带 − 底部带`。例如 5 行排版下顶部带约 120 px、底部带约 30 px，absorber ≈ 420 px —— 每行字号 ≤ `floor((420 − 4×gap) / 5) ≈ 78 px`。**84 px × 5 行会溢出约 40 px。** 字号来自预算，不是反过来。
4. **满屏 Type J 不用 `.shd` 页头条。** Logo + slide-eyebrow 直接写在 `.sc` 顶部一行。

### Type K — 时间线/路线图
横向或纵向的里程碑序列。用于项目计划、演化叙事、阶段描述。组件规范见 §7.12。

---

## 7. 组件库 <!-- ENGINEERING-DNA — every component preserved verbatim -->

可在 **任何** slide 类型上使用的可复用元素。一张 slide 可以组合多个组件，也可以一个都不用 — 直接用颜色 token + 字号阶梯做 bespoke 布局。组件库是工具箱，不是约束。如果 slide 内容需要这里没列的东西，就从系统 token（§2 颜色、§3 字体、§12 间距）出发自己造。

### 7.1 Panel Card (Tier 1 — "big card")

满高对比面板。当 2–3 个选项需要深度、结构化对比时使用。

```css
.panel {
  flex: 1; padding: 22px;
  display: flex; flex-direction: column; gap: 8px;
  background: var(--white); border: 1px solid var(--rule);
  border-top: 3px solid var(--rule);
}
.panel.blue { border-top-color: var(--accent); }
.panel.dark { background: var(--primary); color: #fff; border: none; border-top: 3px solid rgba(255,255,255,.2); }
```

内部结构：`.cap` eyebrow → 标题（18–22 px 900）→ 行（`.panel-row`：surface 底色、8 px 12 px 内边距）→ 可选 callout。

### 7.2 Showcase Card (Tier 2 — "block card")

整洁、优雅的内容分组块。白底、细色 top accent、内容优先。**不要厚重的彩色 header 条** — 卡片应像优质文具，而不是仪表盘小部件。

**设计处理：**
- 背景：`var(--white)`，配 `1px solid var(--rule)` 边框
- **顶部 accent 线**：`3px solid var(--accent)`（默认）。可按上下文换成 `--primary`、`--green`、`--red`。是一条细而优雅的线 — 不是填充的 header 块。
- **没有强制 label 条。** 标题在卡片正文里，作为内容的一部分。
- 标题：20 px 字重 900 `--ink`
- 内容：15–16 px 字重 600 `--mid`，慷慨的 12 px+ 间距
- 可选 SVG 图标：32–36 px，inline 放在标题旁或上方。
- **Hover**：微微上浮（`translateY(-2px)`）+ 阴影

```css
.show-card {
  flex: 1; display: flex; flex-direction: column;
  background: var(--white); border: 1px solid var(--rule);
  border-top: 3px solid var(--accent);
  padding: 20px 22px;
  gap: 10px;
  transition: transform .22s ease, box-shadow .22s ease;
}
.show-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.08); }
.show-card .show-title { font-size: 20px; font-weight: 900; color: var(--ink); line-height: 1.15; }
.show-card .show-desc { font-size: 15px; font-weight: 600; color: var(--mid); line-height: 1.5; }
.show-card.accent-navy { border-top-color: var(--primary); }
.show-card.accent-green { border-top-color: var(--green); }
.show-card.compact { padding: 16px 18px; gap: 8px; }
.show-card.compact .show-title { font-size: 18px; }
```

**反模式**：在 6 张以上卡片网格里每张都用填充色 header 条 — 视觉单调。改用细 top accent 线。

### 7.3 Item Card (Tier 3 — "list card")

用于结构化列表的小型横向卡片。左 accent 边线 + 前导指示符 + 内容。

```css
.bitem {
  display: flex; align-items: flex-start; gap: 14px;
  padding: 12px 16px;
  background: var(--white);
  border-left: 3px solid var(--accent);
}
```

**前导指示符** — 灵活：
- **Ghost 数字**（默认）：`20px 900, --accent, opacity .4` — 用于顺序列表（`01`、`02`、`03`）
- **图标圆**：小圆（24 px）+ 符号（`!`、`✓`、`→`）— 用于发现项、告警。配语义背景色。
- **字母 / 标签**：单字母或短标签，同样的 ghost 样式 — 用于分类条目。

### 7.4 Stat Card (Tier 4 — "number card")

紧凑指标展示。`stat-num`（36 px 900 `--primary`）+ `stat-label`（12 px 800 全大写 `--mid`）。

### 7.5 Callout / Note

**轻量**（内嵌备注）：
```css
.snote { border-left: 3px solid var(--primary); padding: 10px 18px; background: var(--tint); font-size: 14px; font-weight: 700; }
```

**深色**（结论 / 建议条）：
用于 slide 末尾 takeaway 的全宽 navy 块。文字：13–16 px 700–800，`rgba(255,255,255,.85)`。关键词加粗用 `color: #fff`。不要 border-left — 实心 navy 填充本身就是强调。

### 7.6 Marks, Badges & Chips

**状态标记**：
```css
.mark::before { display: inline-block; width: 18px; height: 18px; border-radius: 50%; text-align: center; line-height: 18px; font-size: 11px; font-weight: 900; margin-right: 8px; }
.mark.yes::before { content: '✓'; background: var(--green); color: #fff; }
.mark.no::before  { content: '−'; background: var(--red); color: #fff; }
```

**徽章** — 小型标签胶囊（`.bg-g`、`.bg-r`、`.bg-b`）用于行内状态。12–13 px、字重 900、全大写。

**技术 chip** — 紧凑的行内标签，用于技术 / 特性名。13 px 700，`min-height: 26px`。

### 7.7 Table (`.dt`)

```css
.dt { width: 100%; border-collapse: collapse; font-size: 14px; font-weight: 600; }
.dt th { background: var(--primary); color: #fff; font-size: 13px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; text-align: left; padding: 10px 14px; }
.dt td { padding: 10px 14px; color: var(--ink); border-bottom: 1px solid var(--rule); }
.dt tr.hi td { background: var(--tint); }
.dt .pos { color: var(--green); font-weight: 800; }
.dt .neg { color: var(--red); font-weight: 800; }
.dt .neu { color: var(--mid); font-weight: 600; }
```

**规则：**
- Navy 表头行是唯一的色块。所有数据单元格：白底、`--ink` 文字。
- **`<table>` 单元格里不要彩色徽章** — 用字重 / 颜色强调。
- 可选一行 `--tint` 高亮，仅给最重要的那一行。
- "整洁网格"测试：眯眼看表格。看到一堆彩色方块拼贴，就是设计失败了。

### 7.8 Charts

| Type | Primary colour | Secondary | Neutral | Notes |
|---|---|---|---|---|
| Bar (H / V) | `--accent` | `--primary` | `--rule` | Animated grow on entrance |
| Progress / gauge | `--accent` fill | — | `--rule` track | 8px height, 4px radius |
| Pie / donut | `--primary` | `--accent` | `--rule` | Max 3 segments |
| Timeline | `--primary` dots | — | `--rule` dots | Key nodes: `--tint` ring |

每张图最多 2 种颜色（+ `--rule` 中性色）。入场动效：bar 增长、计数器累加。

### 7.9 Tabs

```css
.tabs { display: flex; gap: 6px; margin-bottom: 14px; }
.tb { padding: 7px 16px; border: 1px solid var(--rule); background: transparent; font: 800 12px/1 'Montserrat'; letter-spacing: .06em; color: var(--mid); cursor: pointer; }
.tb:hover { border-color: var(--accent); color: var(--accent); }
.tb.on { background: var(--primary); border-color: var(--primary); color: #fff; }
.tc { display: none; } .tc.on { display: block; }
```

最多 4 个标签。

### 7.10 Sequential steps / barriers
用 monospace-weight span 的数字标签 `01` `02` `03`、`--accent` 色，而不是 bullet 或装饰 emoji。

### 7.11 Decision questions
前缀用 `Q.1` / `Q.2` 的 span，`--accent` 色、字重 800、字距 0.12 em。

### 7.12 Timeline

横向里程碑序列，配连接线。

**关键布局规则 — dot 永远位于线上、线穿过 dot 中心：**
`.tl-line` 用固定 `top` 值，由 dot 中心以上的总空间算出。日期块用 `min-height` 装文字 + `margin-bottom` 给呼吸空间。

**重要：日期到 dot 的间距用 `margin-bottom`，不要用 `padding-bottom`。** 在 `box-sizing: border-box` 下，padding 在 `min-height` 之内 — 它会压缩内容区，而不是增加空间。`margin` 在盒子外面。

```
Date height:    min-height = 48px
Date-to-dot gap: margin-bottom = 16px
Total above dot: 64px → dot center: 73px → line top: 73px
```

```css
.tl-wrap { position: relative; padding: 0 10px; }
.tl-line { position: absolute; top: 73px; left: 30px; right: 30px; height: 3px; background: var(--rule); }
.tl-row { display: flex; position: relative; z-index: 1; }
.tl-node { flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 4px; }
.tl-date-top {
  font-size: 22px; font-weight: 900; letter-spacing: -.01em; color: var(--accent);
  min-height: 48px; margin-bottom: 16px;
  display: flex; align-items: flex-end; justify-content: center;
}
.tl-dot2 { width: 18px; height: 18px; border-radius: 50%; background: var(--rule); margin-bottom: 12px; flex-shrink: 0; transition: transform .3s ease; }
.tl-name { font-size: 18px; font-weight: 900; color: var(--ink); line-height: 1.2; margin-bottom: 4px; }
.tl-detail { font-size: 14px; font-weight: 600; color: var(--mid); line-height: 1.3; }
```

### 组件选择指引

| 内容 | 组件 | 布局 |
|---|---|---|
| 2–3 个深度对比 | Panel | side-by-side flex |
| 2–3 个带 label 概念块（高端） | Showcase Card | side-by-side flex 或 3 栏 grid |
| 3–4 个带 label 概念块（紧凑） | Showcase Card `.compact` | 3 栏或 2×2 grid |
| 顺序步骤、特性列表 | Item Card | 堆叠列 |
| 带状态图标的发现项 | Item Card（图标变体） | 堆叠列 |
| 关键指标 | Stat Card | 3–4 列一行 |
| 交互式对比 | Flip Card (Type D) | 2 张并排 |
| 单条 takeaway | Callout / Note（轻量） | 全宽 |
| Slide 结论 / 建议 | Callout / Note（深色） | 全宽 |
| 项目里程碑 | Timeline | 横向 flex |

---

## 8. 图像与视觉佐证 <!-- BRAND-VARIABLE intro; rules are ENGINEERING-DNA -->

### 原则

**P&G 摄影法则**：纪实风格（科学家、员工、家庭、自然），不要插画、不要抽象渐变、不要 stock 摄影。色温偏冷或自然光；浅景深；构图给标题留呼吸位（hero 大字会压在画面下三分之一）。可以引用 P&G 公开素材（Brands / Innovation / Sustainability 页面的 hero 图）作为参考。

### 何时加入图像

- **产品 UI 截图**：当讨论某具体工具时，展示它的真实界面。
- **数据可视化**：当某个数字或趋势是核心时，建一张图（Type H）。
- **环境照片**：当某场景需要视觉锚点时，搜并放一张相关图。
- **图示**：当某概念具有结构（层级、流程、对比）时，用 CSS/SVG 画出来，而不是用文字描述。

### 如何获取图像

1. **主动搜索**：用 web search 找相关产品截图、图示、环境照片。优先选官方素材。
2. **CSS 绘制替代品**：柱状图、进度条、时间线图 — 数据简单时优于外部图片。
3. **绝不用**：装饰性 stock photo、抽象渐变、AI 生成的占位艺术、与 slide 主旨无关的图片。

### 图像处理

- `border-radius: 4px`。浅色背景上可选 `1px solid var(--rule)` 边框。
- 深色背景上的图：不要边框。
- 说明文字：图下方使用 `.cap` 样式。
- 绝不在繁忙图像上直接放文字而不加 scrim（最少 `rgba(0,0,0,.5)`）。

---

## 9. 导航 <!-- ENGINEERING-DNA -->

### 圆点导航 — 底部居中，横向

```css
#nav { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 7px; z-index: 99; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,.25); cursor: pointer; transition: all .22s ease; }
.dot.on { width: 20px; border-radius: 3px; background: rgba(255,255,255,.85); }
```

### Slide 计数器 — 右下角
`SLIDE N / TOTAL` — 12 px、字重 700、35% 白。

### 控件
键盘：`← → Space Home End`。触屏：48 px 滑动阈值。

---

## 10. 移动端 <!-- ENGINEERING-DNA — every line invariant; this section saved real decks -->

```css
@media (max-width: 768px) {
  body { overflow-y: auto; }
  #wrap { position: static; display: block; }
  #deck { width: 100%; position: static; transform: none !important; }
  .slide { position: relative !important; opacity: 1 !important; pointer-events: auto !important; min-height: 100dvh; }
  /* Cover and content shells must fill the slide on mobile — `.slide` only sets min-height,
     which a child's `height: 100%` does not inherit, so each shell needs its own min-height. */
  .cov, .sw { min-height: 100dvh; height: auto; }
  .cov-title { font-size: 48px; } .stitle { font-size: 32px; }
  .shd { padding: 0 20px; } .sw .sc { padding: 24px 20px; }
  /* All multi-col → single-col */ .g2,.g3,.flip-row,.tabs { grid-template-columns: 1fr; flex-direction: column; }
  #nav, #ctr { display: none; }
}
```

所有交互元素 ≥ 44×44 px 点击区域。移动端绝不用 `vh` 作为字号/内边距。

### inline-flex 陷阱（关键） <!-- ENGINEERING-DNA: inline-flex-trap -->

**移动端布局失败的最根本原因**：多列布局用 inline `style="display:flex"` 而非 CSS class（`.g2`, `.g3`）。移动端 media query 把 `.g2,.g3` 折叠成单列，但 inline `style="display:flex"` 对 class-based media query 免疫 — 在移动端依然横向，卡片小到无法阅读。

**预防规则**：`.sc` 内每个多列布局的 flex/grid 方向都必须用 CSS class（`.g2`, `.g3`, `.fr`）。如果 inline `style="display:flex"` 不可避免（如 bespoke 一次性布局），移动端 CSS 必须包含 **catch-all 覆盖规则**：

```css
@media (max-width: 768px) {
  /* Catch-all: force ALL flex layouts inside content areas to stack */
  .sc div[style*="display:flex"] { flex-direction: column !important; }
  .sc div[style*="grid-template-columns"] { grid-template-columns: 1fr !important; }
  /* Panel cards should not have fixed flex ratios on mobile */
  .pnl { flex: none !important; width: 100% !important; }
}
```

**首选方式**：用 `.g2` / `.g3` class 而不是 inline flex。inline flex 应是例外，上面的 catch-all CSS 是安全网。

**Checklist 补充**：发布前把浏览器拉到 375 px 宽，确认每一张 slide 都垂直堆叠。任何在移动端仍并排显示的 slide 都是 bug。

### 移动端 flip card 修复 <!-- ENGINEERING-DNA: flip-card-mobile -->

CSS `:hover` 在触屏设备上不生效。Flip 卡 **必须** 有 JS `onclick` handler 来切换 `.on` class。这是 **唯一** 可靠的跨平台翻面机制。

**每张 flip card 必需的 JS：**
```html
<div class="fc" onclick="this.classList.toggle('on')">
```

**必需的 CSS — 桌面与移动端：**
```css
/* 桌面：hover + .on 都触发翻面 */
.fc:hover .fc-inner, .fc.on .fc-inner { transform: rotateY(180deg); }

/* 移动端：禁用所有 3D transform，改用 show/hide */
@media (max-width: 768px) {
  .fc { perspective: none !important; min-height: auto !important; }
  .fc .fc-inner { transform-style: flat !important; transition: none !important; height: auto !important; transform: none !important; }
  .fc:hover .fc-inner, .fc.on .fc-inner { transform: none !important; }
  .fc .ff { position: relative !important; backface-visibility: visible !important; transform: none !important; }
  .fc .ff-back { display: none; transform: none !important; }
  .fc.on .ff-front { display: none; }
  .fc.on .ff-back { display: flex; transform: none !important; }
}
```

---

## 11. 动画 <!-- ENGINEERING-DNA -->

### 核心过渡

| 元素 | 动效 | 时长 | 缓动 |
|---|---|---|---|
| Slide 切换 | opacity | 380 ms | ease |
| 内容入场 | translateY(14px) → 0 + 淡入 | 420 ms | cubic-bezier(.4,0,.2,1) |
| Flip card | rotateY 180° | 650 ms | cubic-bezier(.4,0,.2,1) |
| 圆点导航 | 宽度展开 | 220 ms | ease |

### 叙事动效

| 元素 | 规格 | 何时用 |
|---|---|---|
| 错时入场 | 项之间 80 ms 延迟，每项 350 ms | 列表、网格 |
| 计数器滚动 | 0 → 目标值，1200 ms | 统计 |
| 柱状图增长 | 宽度 0 → 目标值，600 ms + 100 ms 错时 | 对比 |
| 缩放进入 | scale(.85) → 1，400 ms | Callout 卡 |

### 原则

- 每个动效都服务于理解。纯装饰的删掉。
- 入场播放一次。不循环（flip card 的 hover 除外）。
- 每张 slide 的 **入场动效** 总时长 ≤ 2 秒。交互演示和 flip card 不适用。

### 叙事优先设计

1. **Flip card 用于揭示**：问题/解决、前/后、误区/真相。
2. **具体优于抽象**：具体场景胜过泛泛描述。
3. **视觉证据**：图表 > 文字、截图 > 描述、图示 > bullet 列表。
4. **截图测试**：如果没人愿意把这张 slide 截图保存，它就缺一个视觉钩子。

---

## 12. 布局规则 <!-- ENGINEERING-DNA -->

### Overflow 预防

每张 slide 装进 720 px。太密：减小间距 → 正文降到 14 px → 拆 slide。绝不剪裁或滚动。

**"蓝块"陷阱**：右下角的深色 callout = 视觉失衡。改成全宽底部、用 `.snote` 替代、或把深色卡放在顶部。

**"蓝叠 navy"陷阱**：在深色 slide（`--primary` bg）上，永远不要用 `--accent` 当文字或 accent — 会产生刺眼、廉价感的对比。用白色（`#fff`）或半透明白（`rgba(255,255,255,.85)`）做强调。深色背景上的低调 CTA：`rgba(255,255,255,.08)` bg 填充 + 白字。

**"深色堆叠"陷阱**：当一个深色元素直接放在另一个深色元素下方时，它们在视觉上合并。深色元素之间至少留 12 px `--surface` 或 `--tint` 间距。

**Header-内容去重**：`.shd-n` 条已经承载了 slide 的章节标签。不要在内容区里再重复同样的文字作为单独的 eyebrow/标题。

### 间距

| Token | 值 |
|---|---|
| 左水平内边距 | 96 px |
| 右水平内边距 | 80 px |
| 上下内边距 | 32 px |
| 页头高度 | 54 px |
| 卡片间距 | 20 px |
| 卡片内边距 | 32 px |
| 圆角 | 6px（卡片）/ 0（按钮内 chip）/ 50%（数据徽章） |
| 分隔线粗细 | 1 px |
| Accent 边线 | 3 px |

---

## 13. 上线前检查清单 <!-- ENGINEERING-DNA: pre-ship-checklist -->

分享 deck 之前，逐项核对。

### 品牌与 Token
- [ ] 每张 slide 都有 logo（封面右上、内容页 `.shd` 右端）
- [ ] **Logo 在封面肉眼可见** —— 打开 deck，看 slide 1 右上角。"内嵌成功但不可见"是最常见的失败模式（见 §4 fill 级联陷阱）。`has_real_vector_path: true` 单独并不能保证视觉上看得见。
- [ ] Logo `<symbol>` 块内部不含任何 `fill` 属性（含 `<g fill="none">` wrapper）—— 只允许 `fill="currentColor"`
- [ ] **每张 slide 内容都包在 `.sc` 容器内** —— 包括 bespoke 满屏 Type J / Type A。不能用平级 shell 如 `.fpwrap` / `.poster-wrap`（这种自定义 shell 会**静默绕过** `fit_contract_intact`）
- [ ] 颜色：只用系统 token — 不用临时 hex
- [ ] 所有 bespoke 元素都仅基于系统 token 构造（见 §1 约束 vs 自由）
- [ ] 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 可用
- [ ] Montserrat 300 / 400 / 600 / 800（含 300 italic） 已加载；不用 serif / display 字体
- [ ] 封面副标：仅用 Montserrat 300 斜体（如果 300 italic 不可用，用品牌等价值）

### 字体与可读性
- [ ] 没有低于 12 px 的文字 — 特别注意徽章 / 标签列
- [ ] Slide 标题 ≥ 50 px（仅在密集多行例外时降到 38 px）
- [ ] 非表格 slide 的正文 ≥ 16 px（仅在数据密集表格上用 14 px）
- [ ] 副标 ≥ 20 px
- [ ] 中文与对应英文字号 / 字重一致（混排时）

### 幻灯片结构
- [ ] 每张内容页都有 `.shd` 页头条 + slide 编号 + logo
- [ ] 封面没有装饰线 — 不要 hairline、不要 accent line、不要渐变边框
- [ ] 每张 slide 都在 720 px 内 — 没有内容剪裁或溢出
- [ ] 没有"蓝块"陷阱 — 深色 callout 不孤立在双栏布局的右下角
- [ ] 只扫标题也能讲通整个故事

### 适配契约 (§5.1) — 布局安全门
- [ ] `.slide` 和 `.sw .sc` 都带 `overflow: hidden`（三层安全网）
- [ ] 每个 flex:1 absorber 也带 `overflow: hidden` AND `min-height: 0`
- [ ] `.sc` 里的垂直堆叠只有 **一个** `flex: 1 1 0` absorber；其余行都是 `flex: 0 0 auto`
- [ ] 自然段高 + 间距之和 ≤ 602 px（标准内容区）
- [ ] 最后一段内容到 deck 底边的可见间距 ≥ 20 px
- [ ] 在原生 **1280 × 720** 下验证 — 缩放后看不到溢出
- [ ] 没有任何一张卡在半栏 absorber 槽里塞了 2 个段标签 + 5+ 条 bullet — 合并或删减

### 组件与交互
- [ ] Flip card 在桌面 hover-only、移动端 click-to-toggle（JS `onclick` 切换 `.on`）
- [ ] 表格：单元格里不要彩色徽章 — 仅用文字颜色（`.pos` / `.neg` / `.neu`）
- [ ] 卡片层级与内容密度匹配（不要只有 bitem 的稀疏 slide）
- [ ] 交互元素有可见的 hover / focus 状态

### 视觉与图像
- [ ] 图像服务于理解 — 不用装饰性 stock photo
- [ ] 图上文字有 scrim（≥ 50% 不透明度深色蒙层）
- [ ] 图说用 `.cap` 样式

### 动画
- [ ] 入场动效在 slide 激活时播放
- [ ] 每张 slide 的入场动效总时长 ≤ 2 秒（交互演示与 flip card 不适用）
- [ ] 入场动效不循环

### 响应式（移动端对齐 — 不可妥协）
- [ ] 所有多栏布局在 ≤ 768 px 时折叠为单栏 — **包括 inline `style="display:flex"` 布局**（在 375 px 宽下验证）
- [ ] inline `display:flex` 必须配移动端 CSS 的 catch-all（见 §10「inline-flex 陷阱」）
- [ ] 触屏滑动可用（48 px 阈值）
- [ ] 移动端滚动模式下圆点导航隐藏
- [ ] 移动端点击目标 ≥ 44×44 px
- [ ] Flip card 在移动端通过点击工作（不只是 hover）— 每个 `.fc` 都带 `onclick="this.classList.toggle('on')"`
- [ ] 完工前在 **375 px 宽** 下测试浏览器
