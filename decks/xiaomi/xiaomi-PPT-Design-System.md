# 小米-PPT-Design-System

> 为 小米（Xiaomi）制作的所有 deck 共用的视觉语言。请严格遵循，让每一份新 deck 都一眼被识别为同一家族。

来源：基于 https://www.mi.com/global/ 抓取的 7 个子页（home / about / about-founder / about-sustainability / hyperos / mobile / smart-home / xiaomi-17-ultra）合成。

---

## 1. 设计理念

**Xiaomi 的视觉语言是一句话：「工程精度 × 戏剧性产品摄影 × 单一橙色徽章。」**

白色是停顿、黑色是舞台、橙色 squircle 是签名。每一张 slide 像 Xiaomi 自己的产品页那样运作：大尺寸 hero（往往是黑底高质感产品照或人物特写）+ 极简几何字体（MiSans Latin）+ 唯一一抹 #FF6700 在 logo / eyebrow / CTA 上点睛。其余全部是中性灰阶，把视觉权重让给摄影和字号本身。

参考的 mood：**工程美学 × 影院级产品光线 × 平价旗舰的克制**。Apple 产品页的留白节奏、Leica 的镜头气质（Xiaomi 现在把 Leica 联名挂在首屏）、Samsung Galaxy 旗舰页的 spec 密度——但比这三家都更白、更克制、更让产品摄影承担深度。

**两种模式：**
- **桌面端 (≥ 769 px)**：1280 × 720 px 画布，运行时 scale-to-fit (§5)，键盘/点击导航。
- **移动端 (≤ 768 px)**：所有 slide 垂直堆叠成一张可滚动的长页；单栏布局。

### 设计品味 <!-- ENGINEERING-DNA: design-taste -->

**承诺一个清晰的审美立场。** 本 DS 是品牌工具，不是 SaaS 通用模板。基于它做的每一份 deck 第一眼就该让人认出这是 *小米* —— 不是"又一份得体的商务演示"。Xiaomi 的失败模式是中庸：紫色渐变 + 灰字 + 一堆等权 stat card —— 那是 SaaS slop，不是小米。

**反 AI 套路规则**（每张 slide、每个组件、每个变体都适用）：

- **不用通用字体默认值。** MiSans Latin 在 §3 已指定，必须使用 —— 通过 Xiaomi 官方 CDN `@import` 加载。fallback 链里 PingFang SC / Hiragino Sans GB / Microsoft YaHei 兜底 CJK；不要把 Inter / Arial / system-ui 当做"设计选择"。
- **不用陈词滥调的配色。** 紫/蓝色 accent + 板岩灰字 = AI 套路。Xiaomi 的色谱是 `--ink`（深灰近黑）+ `--paper`（纯白）+ `--accent`（#FF6700 橙）。不要塞紫、青、洋红进 accent 槽。
- **不用等权重的多色装饰网格。** 6 张 stat card 各染不同色 = Storybook 配色矩阵。Xiaomi 只有一个主导色（橙），其余全部是字号 + 灰阶层级。
- **不用现成 SaaS 仪表盘 chrome。** 不要每张卡都加柔和 drop-shadow。Xiaomi 的产品页几乎是平的——深度由摄影提供，不由阴影提供。
- **不用空洞的氛围词。** "现代、简洁、大胆"什么都形容因此什么都不形容。Xiaomi 的 voice 是 **「为发烧而生 / Innovation for everyone」**——具体、技术、平价旗舰式自信。
- **一个编排好的入场动效，而非分散的小动画。** 大 hero 适合一次 fade-up；不要给每张 stat card 加 hover 抖动。

### 约束 vs 自由 <!-- ENGINEERING-DNA framing; bullet contents are BRAND-VARIABLE -->

本 Design System 定义了 **硬约束**（永远不能破的）与 **可复用组件**（按需选用的）。它不定义现成配方 —— 每张 slide 都应为它自己的内容构图，而不是从模板拼接。

**硬约束（锁死）：**
- Colour palette (§2 tokens only — no ad-hoc colours)
- MiSans Latin typeface, no serif/display fonts；CJK 走 PingFang SC / Hiragino Sans GB / Microsoft YaHei 系
- 12 px 可读性下限
- 每一张 slide 都必须有 logo
- **每张 slide 的内容必须包在一个 `.sc` 容器里**（即使是 bespoke 满屏的 Type J / Type A 也是）。`.sc` 是 `fit_contract_intact` 唯一扫描的位置 — bespoke 布局如果直接画在自定义 shell 里，会**静默绕过** absorber 检测、移动端 catch-all、602 px 预算这三道保险。没有 `.sc`，就没有契约。
- **Logo 是 B 档（multi）**：橙色 squircle + 内白 mi 标，必须保留双色，**永远不要**通过 CSS `fill:` 给 `.logo` 重新染色（会把 squircle 压成单色不可见，详见 §4）。
- 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 和几何指示符允许
- 不用装饰性 stock photography —— Xiaomi 用真实产品摄影 / 真实截图
- `.shd` header strip on content slides
- `.sw` border-left accent

**可复用组件（按需选用，不强制）：**
- §7 组件库提供卡片、表格、图表、标签、标记 — 适合时用，不适合时跳过用 bespoke 布局。

**Bespoke 元素（鼓励）：**
- **在调色板内自由发挥。** 例如：满屏黑色 hero + 大字白色标题 + 右上橙色 squircle；产品摄影占 60% 宽 + 左侧 spec 数字大字纵列；时间线上里程碑节点用 `--accent` 实心圆 + `--mid` 虚连线。
- 判定标准是：该元素是否只用了定义过的颜色 token、品牌字体、并尊重可读性下限？如果是，即便不匹配任何具名组件也算"在系统内"。
- **不要自我限制在具名组件里。** 如果某 slide 需要 §7 不存在的东西，就从 token 出发自己造。最好的 slide 都是从系统 token 出发的 bespoke 构图。

---

## 2. 颜色令牌 <!-- BRAND-VARIABLE: hex values + brand-palette names; core role token names are invariant -->

颜色 token 系统有三层：

1. **核心角色 token** — 所有品牌之间名字不变。它们标识颜色 *扮演什么角色*，而不是 *它是什么颜色*。
2. **语义 token** — 所有品牌之间名字不变；编码含义（正向 / 负向 / 警告 / 信息）。
3. **品牌调色 token** — 小米特有的命名 + hex（橙、深炭、舞台黑）。

```css
:root {
  /* ── Core role tokens (invariant names) ── */
  --primary:  #191919;   /* Dominant brand chord — cover bg, primary mark colour (Xiaomi 的"舞台深炭") */
  --accent:   #FF6700;   /* CTA / link / single saturated highlight — Xiaomi 橙 */
  /* ── Neutrals ── */
  --surface:  #FFFFFF;   /* Paper / slide bg — Xiaomi 全球站主表面 */
  --white:    #FFFFFF;
  --ink:      #191919;   /* Body text on light surfaces — 与 --primary 同源 */
  --mid:      #898989;   /* Secondary text / muted labels (recon 中 #898989 ×72) */
  --rule:     #E5E5E5;   /* Dividers / hairlines — 与 --tint 区分 */
  --tint:     #F5F5F5;   /* Subtle row / section bg (recon 中 #F5F5F5 + #F7F7F7) */
  /* ── Semantic (invariant names; values may map to brand-palette colours) ── */
  --green:    #2DA44E;   /* Positive — Xiaomi 商城 "Buy Now" 绿 */
  --green-bg: #E6F7EC;
  --red:      #E11D48;   /* Negative */
  --red-bg:   #FCE7EB;
  --warn:     #F0C36D;   /* Warning / caution — recon 中的黄色 #F0C36D 系 */
  --warn-bg:  #FEF3C7;
  --teal:     #1D4ED8;   /* Informational / neutral highlight — recon link 蓝 */
  --teal-bg:  #DBEAFE;
  /* ── Brand palette (brand-specific names; expanded from brand.json accents+neutrals) ── */
  --xiaomi-orange: #FF6700;   /* The signature chord — same value as --accent, separate name for semantic clarity */
  --xiaomi-orange-soft: #FF6900;   /* Logo-internal variant from the inline-svg fill */
  --stage:    #000000;        /* Pure black — for cinematic hero/cover stages (Leica banner, 17 Ultra) */
  --carbon:   #191919;        /* Deep ink — content bg alternative; same as --ink */
  --carbon-light: #2A2A2A;    /* Lighter carbon — for camera-ring inner, depth highlights on dark stages, low-contrast bezels */
  --halo-tint: rgba(255,103,0,0.08);   /* Used on dark covers as faint orange wash behind eyebrows */
}
```

**规则：** <!-- ENGINEERING-DNA -->
- **Token 名是角色抽象，不是颜色名。** `--primary` 是品牌的主导和弦 —— Xiaomi 的主导色是深炭舞台 #191919；`--accent` 是单一的橙色徽章。Slide CSS 读 `var(--primary)` 拿到的就是当前 brand DS 对应的正确颜色。
- **每张 slide 只有 *一个* 主导 accent 颜色。** 用 `--accent` 做 slide 的标志性高亮（CTA、callout 边线、chart 主条、eyebrow 上的 ✦）。`--xiaomi-orange-soft` 仅在 logo 内部出现，不要拿来做 slide accent。一张 slide 最多用一个橙色高亮 —— 双橙立刻廉价。
- **语义颜色仅在含义彼此独立、相对时才同时出现** — 例如规格对比 slide 的 ✓ (`--green`) / ✗ (`--red`)。否则只取一种。
- **`--tint` 用于行底色，不用于卡片填充。** 卡片填白（`--white`）。
- **永远不用纯黑做正文。** `--primary` (#191919) 已经是 Xiaomi 真实的深炭，纯 #000 留给 cover stage。
- **永远不在 slide CSS 里写临时 hex。** 每个颜色都必须来自 token（核心 / 语义 / 品牌调色）。`token_only_colors` hard check 会强制执行。

**深色 cover 配色处方：**
- 背景：`var(--stage)` 或 `var(--primary)`
- 标题：`#FFFFFF`（直接用 `--white`）
- Eyebrow：`var(--accent)`（橙色徽章+小三角符号 ✦）
- 副标：`rgba(255,255,255,.7)`
- 不要在深色 cover 上同时用 `--accent` 和 `--teal` —— 会刺眼

---

## 3. 字体 <!-- BRAND-VARIABLE: font family + fallback; the scale below is mostly invariant -->

**MiSans Latin** —— 唯一字体。字重 300 / 400 / 500 / 600 / 700（无斜体；Xiaomi 没有发布 italic 子集）。`PingFang SC / Hiragino Sans GB / Microsoft YaHei` 作为 CJK 字符的回退。

> MiSans Latin 是小米 2021 年开源发布的几何无衬线，由汉仪与小米联合设计 —— 字面方正、字重过渡平滑、x-height 较高（屏幕可读性强）。在 Xiaomi 全球站，它统一了从导航到产品 hero 到 spec 表的所有西文字符。Deck 沿用同一字体即视觉一致。

### 加载方式（Xiaomi 官方 CDN）

```css
/* 在 deck HTML <head> 第一行加这一句即可，无需自托管 woff2 */
@import url('https://i02.appmifile.com/i18n/fonts/MiSansLatin/index.css');
```

这是 Xiaomi 自己的 CDN，已包含 light / regular / medium / semibold / bold 五个字重的全 Unicode 子集（Latin / Latin-Ext / Cyrillic / Greek / Vietnamese）。`font-display: swap` 由 Xiaomi 端配置，离线时 fallback 链接管。

### CJK 字体回退链 <!-- ENGINEERING-DNA: cjk-fallback -->

中文 deck 不能直接用拉丁字体当 body font。MiSans Latin 不含 CJK 字形，浏览器对 CJK 字符自动回退到系统默认（macOS 上是 STHeiti 细体，Windows 是微软雅黑 Light），**视觉上立刻显得廉价**。

**最低要求**：font-family 链里**必须至少出现一个 CJK 字体名**（PingFang SC / Hiragino Sans GB / Microsoft YaHei / Source Han Sans 等），否则 CJK 字符 100% 落到 OS 默认。`cjk_font_quality` hard check 会强制执行这一条。

**Xiaomi 中文 deck 的字体链（CJK-first，推荐）：**

```css
/* 中文 deck 推荐字体链 — CJK 优先，MiSans Latin 兜底拉丁 */
font-family:
  /* macOS / iOS 中文（最高优先级 — 干净、与 MiSans 同为现代几何无衬线） */
  'PingFang SC', '苹方-简',
  /* macOS 较旧 / 阅读体严肃面 */
  'Hiragino Sans GB', '冬青黑体简体中文',
  /* Windows 中文 */
  'Microsoft YaHei', '微软雅黑',
  /* Linux / Android / 通用 */
  'Source Han Sans SC', 'Noto Sans SC',
  /* 拉丁 brand 字体 — 渲染所有英文/数字 */
  'MiSans Latin', 'MiSans',
  /* 系统通用 */
  system-ui, -apple-system, 'Helvetica Neue', sans-serif;
```

**字重提升**：PingFang SC 的 Regular（400）较细 —— 大字标题用 700（Bold），正文用 500（Medium）以上，避免"中文显瘦"的廉价感。MiSans Latin 与 PingFang SC Medium 在视觉权重上匹配良好，混排不跳戏。

**禁止**：font-family 链里完全没有 CJK 字体。`cjk_font_quality` hard check 会立刻 FAIL。

### 字号阶梯 <!-- ENGINEERING-DNA — sizes are invariant; the scale is what makes decks readable -->

| 用途 | 字号 | 字重 | 字距 | 备注 |
|---|---|---|---|---|
| 封面大标 | 82 px | 700 | −0.03 em | 行高 0.98（MiSans 没有 900 字重，700 是最重） |
| 封面副标 | 22 px | 300 | +0.01 em | 不用斜体（MiSans 无斜体；用 300 weight 区分层级） |
| 内页标题 | 50 px | 700 | −0.025 em | 行高 1.06 |
| 内页副标 | 20 px | 600 | +0.01 em | `--mid` |
| Eyebrow / 徽章 | 11–12 px | 700 | +0.18–0.24 em | 全大写，配 ✦ 三角作前缀 |
| 卡片标题 | 28 px | 700 | −0.01 em | |
| 正文 / 列表 | 16 px | 500 | 默认 | 行高 1.5–1.6 |
| 表格 / 数据 | 13–14 px | 600 | +0.1 em | 全大写表头 |
| 说明 / 元信息 | 12–13 px | 600 | +0.14 em | 绝不低于 12 px |

> 注：MiSans Latin 不附 900 黑体字重（最重为 700 Bold）。模板里的"900 字重"在所有地方都映射到 MiSans 的 700。如果同时混排 PingFang SC，PingFang Bold 与 MiSans Bold 视觉权重一致。

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

## 4. 小米 Logo <!-- BRAND-VARIABLE: SVG payload is brand-specific; surrounding pattern + multi-format support is ENGINEERING-DNA -->

### 定义（每份 HTML 一次）

Logo 必须是真实的品牌身份资产，**完整内嵌**到 HTML 中（不依赖外部网络）。Xiaomi 的 canonical logo 来自 JSON-LD `Organization.logo` 声明：`https://i01.appmifile.com/webfile/globalimg/mobile/logo/mi.png` —— 196×196 RGBA PNG 的橙色 squircle + 白色「mi」wordmark。这是 **C 档（raster）**。

> ⚠️ **不要用 `<symbol> + <use> + <image href>` 模式装载 raster logo** <!-- ENGINEERING-DNA: tier-c-img-not-symbol -->
> deckify 早期把 raster logo base64 进 `<image href>` 再包到 `<symbol id="brand-wm">`，slides 用 `<svg class="logo"><use href="#brand-wm"/></svg>` 引用。**这个模式在某些 Chromium 版本下会静默失败** —— `<image>` 在 `<symbol>` 实例化为 `<use>` 时进入 shadow DOM，data-URI 解码或图片加载在 shadow tree 里有时不会触发，**logo 完全看不见但 byte 检查全过**。这是 deckify 命中过的 stealth bug。
>
> Xiaomi DS 的 raster logo **必须用直接 `<img>` 元素**，src 是 base64 PNG data URI。这绕开 SVG/symbol/use 的所有 shadow-DOM 渲染陷阱。

#### C 档 — `raster`（直接 `<img>` 模式，推荐）

每张 slide 直接放一个 `<img class="logo W lg" src="data:image/png;base64,…" alt="Xiaomi">`：

```html
<!-- 封面（深底白色变体，44 px） -->
<img class="logo W lg" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMQAAADECA…(略，完整 base64 见 source/assets/logo.png 的 base64 编码)" alt="Xiaomi">

<!-- 内容页（浅底品牌深色变体，36 px） -->
<img class="logo L" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMQAAADECA…" alt="Xiaomi">
```

> 注：每张 slide 都要重复完整 base64 字符串。9 张 slide × 6 KB ≈ 54 KB 额外字节。完全可接受 —— 比 `<symbol>+<use>` 模式 16% 文件膨胀换 100% 渲染可靠性。

#### 已废弃 — B 档 `<symbol> + <image href>` 模式

> ⚠️ **历史教训** <!-- ENGINEERING-DNA: tier-b-symbol-image-deprecated -->
> 早期 `embed_logo.py` 默认输出这个：
>
> ```html
> <svg style="display:none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
>   <symbol id="brand-wm" viewBox="0 0 196 196">
>     <image href="data:image/png;base64,..." width="196" height="196"/>
>   </symbol>
> </svg>
> ```
> 然后用 `<svg class="logo"><use href="#brand-wm"/></svg>` 引用。在某些 Chromium 版本（包括 agent-browser bundled Chromium 当前版本）下，`<image>` 在 shadow DOM 中**完全不渲染**，但 `logo_renders` byte-level check 看到合法 SVG 结构 + `logo_visible_pixels` 看到非透明像素（broken-image placeholder）就 PASS。
>
> **永远用直接 `<img>`。** raster 不需要 `<symbol>` 跨 slide 复用 —— `<img>` 已经是最轻量的图片元素。

#### A 档 — `mono`（单色 wordmark / silhouette，Xiaomi 当前不适用）

A 档保留给未来 Xiaomi 切换到单色 wordmark 的场景。当前正式 logo 是双色（橙 + 白），不是单色 silhouette。如果未来切换：

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 W H" fill="currentColor">
    <path d="..."/>  <!-- 内层 fill 必须 strip; 任何 fill="none" 也算 -->
  </symbol>
</svg>
```

```css
.logo   { height: 36px; width: auto; flex-shrink: 0; fill: currentColor; }
.logo.W { color: #fff; }
.logo.L { color: var(--accent); }
```

A 档 inner fill 级联陷阱依然适用 —— 详见上方"⚠️ A 档 fill 级联陷阱"块。

<details><summary>已废弃的 B 档 base64 SVG image 模式（点击展开 —— 不要再用）</summary>

> 早期 `embed_logo.py` 默认输出 `<symbol>` + `<image href="data:image/svg+xml;base64,...">` —— 在某些 Chromium 下 base64 SVG **缺 `xmlns="http://www.w3.org/2000/svg"`** 时直接失效（浏览器把它当 XML 而非 SVG），渲染成 broken-image placeholder。即使 xmlns 正确，`<image>` 在 `<symbol>` shadow DOM 中的 data-URI 解码也时常失败。**已统一切到直接 `<img>` 模式。**

</details>

<!-- 历史 base64 fragment 已 strip，详见 source/assets/logo.png（PNG 字节）以及上方 §4 C 档 <img src="data:image/png;base64,..."> 直注模式。 -->

> ⚠️ **A 档 fill 级联陷阱（Xiaomi 不适用，但保留约束以备未来切换）** <!-- ENGINEERING-DNA: logo-inner-fill -->
> 如果未来 Xiaomi 切换到单色 wordmark / silhouette logo（A 档），那时 `<symbol id="brand-wm" fill="currentColor">` 内任何 `<path>/<g>` 上的 `fill` 属性（包括 `fill="none"`）都会**赢过**父级 currentColor 级联，wordmark 渲染出来 100% 不可见 —— 而 byte 级检查（path d 长度、viewBox、`visible_on_cover`）全都会显示 PASS。**A 档下所有内层 `fill` 必须被 strip。** Xiaomi 当前是 C 档（raster `<img>`），inner fill 完全不适用；`logo_renders` hard check 在 raster 档下跳过 `hasInnerFill` 规则。

> ⚠️ **禁止用文字 placeholder 伪装 logo**：用 `<text>X</text>` 假冒 logo（如字母圆盘）属于构建失败。`logo_renders` hard check 会拒绝只含 `<text>` 的 `<symbol>` 块。如果你的 logo 不显示，**停下来**回到 §4 选官方 PNG（JSON-LD `Organization.logo`）+ 直接 `<img>` 模式，永远不要编造 placeholder。

#### 多色 cover 处理（C 档默认）<!-- ENGINEERING-DNA: logo-multicolor-cover -->

Xiaomi 的 squircle 自身已经有强对比（橙底 + 白色内 mi）。**默认裸 logo 直接放上 cover，不加 chip**。三种 cover 背景下都成立：

1. **白底 cover (`--surface`)**：橙色 squircle 直接置于白底，对比强烈（小米全球站 about / mobile / smart-home 全是这个用法）。
2. **黑底 stage cover (`--stage`)**：橙色 squircle 直接置于纯黑，对比同样强烈，是 hero 大片（Leica banner、17 Ultra）的默认处理。
3. **深炭 cover (`--primary`)**：同上，#191919 与橙色形成自然对比。

**只有当 cover bg 与橙色色相过近**（如假想的橙色满版 cover）时，才用 `.logo-chip` 包白底（`padding: 0`）做不可见对比层。Xiaomi 实际不会出现这种情况（橙色不做满版 bg），所以 chip 在 Xiaomi DS 中**几乎用不到**。

### 用法

```html
<!-- 直接 <img>，每张 slide 一份完整 base64 -->
<img class="logo W lg" src="data:image/png;base64,iVBORw0KGgoAAAA…" alt="Xiaomi">
```

```css
/* C 档（raster） — <img> + base64 PNG。<!-- ENGINEERING-DNA: tier-b-no-css-fill -->
   不要给 .logo 设 fill 或 color —— 那些只对 SVG 内 path 有效，对 raster 无效；
   且如果未来切回 SVG <symbol>+<use> 模式，CSS fill 会通过 shadow DOM 级联
   把图层压成单色（B 档历史教训）。保留 .W / .L 作为空类，让相同的
   `<img class="logo W">` 标记可以在不同品牌之间复用，不需要下游模板做
   条件分支。 */
.logo {
  display: inline-block;
  flex-shrink: 0;
  height: 36px; width: 36px;
  object-fit: contain;
  user-select: none;
  -webkit-user-drag: none;
}
.logo.W, .logo.L    { /* 故意留空 — 见上方注释 */ }
.logo.lg            { height: 44px; width: 44px; }
```

### 摆放规则 <!-- ENGINEERING-DNA -->
- **每张 slide** 都必须有 logo — 封面与所有内容页。
- **封面**：`.cov-top` flex 行的右上角。
- **内容页**：`.shd` 页头条的右端（左 = 标题 eyebrow / slide 编号，右 = logo）。
- Logo 周围最小留白 = logo 高度（36 px）四周都留。
- 不要拉伸、不要重新着色、不要把 logo 叠在带图案的区域上 —— 找一块净色衬底。

> Xiaomi squircle 是 1:1 方形，宽高都按 36px 默认渲染。在 cover 上可以放大到 48px；在 `.shd` 上保持 36px。不要超过 60px，否则视觉过于沉重。

---

## 5. 幻灯片架构 <!-- ENGINEERING-DNA — the entire section, invariant -->

### 脚手架
```
#wrap — fixed fullscreen, flex-centre, background: var(--ink)
  #deck — 1280 × 720, position:relative, overflow:hidden (hard contract)
    .slide × N — absolute inset, opacity show/hide, overflow:hidden (hard contract)
```

`#wrap` 与 `body` 的 background **必须用 `var(--ink)`**，不能写死 `#000` / `#1A1A1A` / `#1F1F22` — 这些会被 `token_only_colors` hard check 抓到。Xiaomi 的 `--ink` 是 #191919（深炭舞台），letterbox 跟随它就是对的。

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

**Anti-pattern**: shipping a deck without `scaleDeck()` lets `#wrap`'s flex-centre place a 1280×720 deck inside a 1920×1080 viewport with 320 px / 180 px of dark border — the deck looks unfinished even when content is correct. Every Xiaomi deck must wire scale-to-fit into the verification deck.

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
.shd-num { font-size: 11px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: var(--accent); }
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

Default `.sc` padding is symmetric `32 80 32 96`. Xiaomi 的产品页是高呼吸感的，建议默认就用非对称：

```css
.sw .sc { padding: 24px 80px 40px 96px; }   /* 24 top / 40 bottom — Xiaomi 默认 */
```

The extra bottom padding creates deliberate visible breathing — roughly half a section-gap worth — between the last content block and the deck edge. This reads as "composed" rather than "crammed."

#### 编写前清单（写 HTML 之前做）

1. **List your sections** and assign each a role: `absorber` (exactly one) or `natural`.
2. **Estimate natural heights** using the type scale. A card with head (28) + label (13) + 5 single-line 13 px bullets (~125) + V-padding (34) = ~200 px.
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

> **Emphasis for Xiaomi**: 重点四类 —— Type A 戏剧性 hero 封面、Type F 图文左右分栏（产品摄影 + spec 数字大字）、Type H 数据表 / 性能图表、Type J 大 pull-quote 价值主张。
> Foreground these types when designing decks: **Type A, Type F, Type H, Type J**。
> Use sparingly: Type G 交互演示（小米 deck 不需要交互 prototype；产品摄影本身就是 demo）。

### Type A — 封面
- 背景：`var(--stage)` (#000) 或 `var(--primary)` (#191919) —— Xiaomi 默认 cinematic 黑底
- 结构：Logo 右上角（橙 squircle）→ Eyebrow（橙色 ✦ + 全大写小字）→ 巨型标题（白色 700 weight）→ 副标（300 weight，70% 白）→ Meta 行
- **不允许任何装饰线** — 不要 hairline、不要 accent line、不要渐变边框。背景就是表面（产品摄影或纯色舞台）。
- Xiaomi 偏爱：产品摄影满版 hero（17 Ultra 拿绿色相机 silhouette、SU7 黄色车身），前景配大字标题；或纯黑 stage + 单个橙色 mark + 大标。

#### 封面垂直构图规则 <!-- ENGINEERING-DNA: cover-vertical-anchor -->

**封面内容默认居中、不要 flex-end 贴底。** 封面是一张固定 720 px 的画布，但 hero 标题应当**视觉上锚定在画面中线偏上**位置 —— 这是产品页 hero 的通用节奏（参考 mi.com/global 主页：title + subtitle 大约在 viewport 40–55% 区间）。

```css
.cov          { display: flex; flex-direction: column; }
.cov-top      { flex: 0 0 auto; padding: 36px 48px 0 96px; }    /* eyebrow + logo 行，不参与 absorber */
.cov-sc       { flex: 1 1 0; min-height: 0; overflow: hidden;   /* 这是封面 absorber */
                display: flex; flex-direction: column; justify-content: center;
                padding: 0 96px; gap: 22px; }
.cov-bot      { position: absolute; bottom: 28px; left: 96px; right: 96px;   /* meta 行绝对定位到底，不抢 absorber */
                display: flex; justify-content: space-between; align-items: center; }
```

**反模式（已知失败）：**
- `.cov-sc { justify-content: flex-end; padding: 0 96px 28px 96px; }` —— 把 title + sub 钉死在 cover 底部，视觉上"贴底"，meta 行又紧挨着，整张封面下半部塞满、上半部完全空。视觉权重严重失衡。
- 把 meta 行（"SOURCE · ... · N SLIDES · ..."）放进 `.cov-sc` 内部用 flex `gap` 排列，结果 meta 行参与了 absorber 的高度计算，把 title + sub 顶得更靠下。**meta 行必须脱离 flex 流（绝对定位）**或放进独立的 `flex: 0 0 auto` 带子。

**封面副标的换行控制：**
- 副标 `max-width: 640px`（不要满宽，否则中文长句在词中切断难看）
- 文案保持 ≤ 2 行（中文 ~32 字 / 行 × 2 = ~64 字上限）
- 不要写跨多个分句的长 subtitle —— 用一句陈述 + 一句注脚的结构

### Type B — 双栏内容
对比、特性列表、指标。`grid-template-columns: 1fr 1fr; gap: 20px`。移动端会折叠为单栏。

### Type C — 全宽叙事
单栏、大字号、配 pull-quote。用于上下文、摘要、推荐建议页。

### Type D — 翻面卡片
两张卡片并排。正面 = `--primary` (#191919)，背面 = `var(--accent)` (#FF6700) 柔化版本（用 `rgba(255,103,0,0.92)` 避免过饱和）。**Hover + 点击翻面** — JS `onclick` 切换 `.on` class（移动端必需）。正面有 ghost 罗马数字。背面留白宽（32 px padding，≤ 4 个内容元素）。

**字体 — 必须大而有力（MiSans 没有 900，全部映射到 700）：**

| 元素 | Class | 字号 | 字重 |
|---|---|---|---|
| 正面标题 | `.cnm` | **28px** | 700 |
| 正面正文 | `.cbd` | **17px** | 500 |
| 正面提示 | `.ht` | 13px | 700 |
| 背面标签 | `.bkl` | 13px | 700 |
| 背面标题 | `.bkt` | **22px** | 700 |
| 对比标签 | `.vs .vt` | 13px | 700 |
| 对比正文 | `.vs .vb` | **16px** | 600 |
| 结论 | `.ccl` | **15px** | 500 |

**不要用 inline style 覆盖** 把 flip card 文字缩到这些字号以下。装不下就减项数 — 不要减字号。

### Type E — 数据/对比页
以表格或结构化数据网格为主体的 slide。用于 Xiaomi 17 Ultra vs 17 Pro 规格对比、各代手机配置 diff、HyperOS 跨设备特性矩阵。表格组件规范（§7.7）定义元素级设计；本类型定义何时用、以及如何在它周围布局。

**原则：** 表格是主角 — 标题 + 表格 + 底部可选一行 callout。不要有侧栏抢戏。如果表格有 6 列以上，让它占满整宽。

**Row-count rule** <!-- ENGINEERING-DNA: type-e-row-count -->
- 5 行是标准 14 px 行内边距（单元格 `padding: 14px 18px`）下的舒适行数。
- 6 行以上要么 (a) 把单元格内边距收紧到 `padding: 10px 16px`，要么 (b) 把数据拆到两张 slide。不要让 absorber 剪裁 — `text_layout_safe` hard check 会捕获。
- 如果表格既要 6 行以上 AND absorber 里又要侧栏 callout，那就拆开 — 不要硬塞。

#### 表格在移动端必须横向滚动 <!-- ENGINEERING-DNA: type-e-mobile-scroll -->

**问题**：表格不像 grid / flex，**不会**自动折叠成单列。一张 6 列表格在 375 px 视口里每列只有 ~55 px，"Snapdragon 8 Elite Gen 5"、"75–100mm telephoto" 这种内容会**横向溢出 deck 或挤成不可读的字符堆**。`mobile_collapse` hard check 抓不到这种 case（它只看 `body.scrollWidth`，但表格在 absorber 里 overflow:hidden 时不会推大 body）—— 视觉上是坏的，自动检查全过。

**强制规则**：每张 Type E 的 slide 都必须在 mobile media query 里把 `.dt-wrap` 切到横滚模式：

```css
@media (max-width: 768px) {
  .dt-wrap {
    overflow-x: auto !important;
    overflow-y: visible !important;
    -webkit-overflow-scrolling: touch;
  }
  .dt {
    min-width: 560px;          /* below this trigger horizontal scroll */
    font-size: 13px;
  }
  .dt th, .dt td {
    padding: 8px 12px;
    white-space: nowrap;        /* prevent narrow columns from line-wrapping cells */
  }
  .dt th:first-child, .dt td:first-child { padding-left: 16px; }
  .dt th:last-child,  .dt td:last-child  { padding-right: 16px; }
  .dt-foot { flex-wrap: wrap; gap: 8px; }
}
```

**为什么 `min-width: 560px`**：560 ≈ "6 列 × 平均 90 px"，足以让表头大写标签和 spec 内容（"200MP · 75–100mm"、"Snapdragon 8 Elite Gen 5"）单行渲染。具体数字按列数调：3 列用 360、4 列 440、5 列 500、6 列 560、7+ 列 ≥ 640。

**反模式：**
- 不要在 mobile 里把 `.dt` 字体缩到 11 px 以下塞下原始列宽 —— 违反 §3 12 px 下限。
- 不要在 mobile 里 `display: grid` 重排 table 单元格 —— 破坏表格 a11y（屏幕阅读器靠 `<th>`/`<td>` 关系导航）。
- 不要把表格转成"卡片视图"（每行变一张 card with label-value 对）—— 这种重排会丢列对比关系，且实现成本高。横滚是最克制的方案。

`.dt-wrap` 在桌面端**仍然**要保持 `overflow: hidden`（fit contract 三层安全网之一）。Mobile 切换通过 `@media` 选择器隔离，互不干扰。

### Type F — 图像页
**Xiaomi DS 的招牌类型之一。** 一张产品摄影或截图占据 slide 主体，文字锚定在安静区域。用于展示真实产品 hero、UI 截图、Leica 联名摄影、SU7 车身照片。

**原则：**
- 图像必须服务于理解 — 不要装饰性 stock photo。优先：Xiaomi 官方产品摄影（mi.com 资源）、HyperOS UI 截图、真实数据可视化、Leica 镜头测试照。
- 构建 deck 时，**主动从 mi.com 找配图**（产品 hero、规格图、UI 截图）来支撑叙事。
- 图像处理：`border-radius: 4px`，浅色背景上可选 `1px solid var(--rule)` 边框。深色背景不需要边框。
- 布局：图像占 slide 区域 50–70%。文字放在旁边或叠在带 tint 的区域上。绝不在繁忙图片上直接放文字而不加 scrim。
- 图下说明：`.cap` 样式（13 px、字重 700、全大写、`--mid`）。

**Xiaomi-specific Type F 配方**（左图右数字）：
```
┌──────────────────────────┬──────────────────┐
│                          │  EYEBROW · IMAGING│
│                          │                   │
│   产品摄影 (60% 宽)       │  200MP            │
│   border-radius: 4px      │  ──────           │
│                          │  Leica Summilux   │
│                          │  徕卡光学          │
└──────────────────────────┴──────────────────┘
```
左侧图占 60-65% 宽，右侧大字号数字（48-72 px、700）+ 解释行（13-14 px、`--mid`）。每条配一个 hairline ruler 分隔。

### Type G — 交互演示
嵌在 slide 内的自包含、点击推进的微体验。**Xiaomi DS 中 use sparingly** —— 产品摄影本身已经是最好的 demo，不需要 interactive prototype。除非演示 HyperOS 跨设备流转之类必须动态展示的场景，否则跳过。

### Type H — 图表/数据洞察
**Xiaomi DS 的招牌类型之一。** 由一个或多个数据可视化主导的 slide。用于跑分对比、能耗曲线、Sales 增长、Market share。图表组件规范（§7.8）定义元素级设计；本类型定义 slide 级原则。

**原则：**
- 每张 slide 一个主图。次要小图可接受 — 但必须直接支撑主图。
- 标题陈述洞察，不是图表类型。好："Xiaomi 全球出货量连续四个季度增长"。坏："柱状图对比"。
- 图表占 slide 区域 50–70%。剩余空间：标题 + 一段解读或一个 callout。
- 入场动效以增强叙事冲击力。
- Xiaomi chart 规范：主条 `--accent` 橙、对比条 `--mid` 灰、grid `--rule` —— **永远不要** 拿 `--green/--red/--teal` 当图表色，那些专给语义状态用。

### Type I — 标签页
多个内容视图通过标签切换。当内容有自然分类时（例如 Mobile / Wearables / Smart Home / Lifestyle 四大产品线），能在一张 slide 上容纳更多信息。Tab 组件规范见 §7.9。

**原则：** 最多 4 个标签。每个 tab panel 都是自包含的"slide-中-slide" — 可以用 §7 任何组件。不要把标签当成 slide 内容塞太满的拐杖；如果 2 个标签各自都显稀疏，就合并成一个视图。

### Type J — 引言/抽词
**Xiaomi DS 的招牌类型之一。** 一句强烈的话锚定叙事时刻 ——「Innovation for everyone」「为发烧而生」「Engineered to be loved」 这种品牌价值宣言。

**结构（标准版）：** 大号引用文字（28–36 px、字重 700、`--ink`）居中或左对齐。可选下方署名（14 px、`--mid`）。左边 accent 边线（`3px solid --accent`）或无。

**结构（满屏 bespoke 变体 —— Xiaomi 推荐）：** 整张满屏 `--stage`（黑）或 `--primary`（深炭）+ 多行海报型大字（如 4-5 行 MiSans Latin 700，部分关键词用 `--accent` 橙染色）。这种 slide：

1. **构图依然必须包在 `.sw + .sc` 里。** 用 `.sw`（覆写 `background: var(--stage)`）+ 一个 `.sc` 装自定义布局。**不要**自创平级 shell class（`.fpwrap`、`.poster-wrap` 等）—— bespoke shell 会**静默绕过** `fit_contract_intact`（没有 `.sc` = absorber 数 0 = `bad_slides: [{absorbers: 0}]`）。
2. **`.sc` 内必须恰好一个 absorber**，带 `flex: 1 1 0; min-height: 0; overflow: hidden` —— 通常是装大字的中间带。顶部 header 带和底部署名带都 `flex: 0 0 auto`。
3. **按行数反推字号上限。** absorber 的 `clientH` ≈ `(720 − 54 header − 24 top − 40 bottom) − 顶部带 − 底部带`。例如 5 行排版下顶部带约 120 px、底部带约 30 px，absorber ≈ 452 px —— 每行字号 ≤ `floor((452 − 4×gap) / 5) ≈ 84 px`。**字号来自预算，不是反过来。**
4. **满屏 Type J 不用 `.shd` 页头条。** Logo + slide-eyebrow 直接写在 `.sc` 顶部一行。

### Type K — 时间线/路线图
横向或纵向的里程碑序列。用于 Xiaomi 公司发展（2010 创立 → 2014 进入印度 → 2018 港交所上市 → 2024 SU7 量产 → 2026 当前）、产品代际演化、HyperOS 版本路线图。组件规范见 §7.12。

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
.panel.orange { border-top-color: var(--accent); }
.panel.dark { background: var(--primary); color: #fff; border: none; border-top: 3px solid rgba(255,103,0,.4); }
```

内部结构：`.cap` eyebrow → 标题（18–22 px 700）→ 行（`.panel-row`：surface 底色、8 px 12 px 内边距）→ 可选 callout。

### 7.2 Showcase Card (Tier 2 — "block card")

整洁、优雅的内容分组块。白底、细色 top accent、内容优先。**不要厚重的彩色 header 条** — 卡片应像优质文具，而不是仪表盘小部件。

**设计处理：**
- 背景：`var(--white)`，配 `1px solid var(--rule)` 边框
- **顶部 accent 线**：`3px solid var(--accent)`（默认橙）。可按上下文换成 `--primary`、`--green`。是一条细而优雅的线 — 不是填充的 header 块。
- **没有强制 label 条。** 标题在卡片正文里，作为内容的一部分。
- 标题：20 px 字重 700 `--ink`
- 内容：15–16 px 字重 500 `--mid`，慷慨的 12 px+ 间距
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
.show-card .show-title { font-size: 20px; font-weight: 700; color: var(--ink); line-height: 1.15; }
.show-card .show-desc { font-size: 15px; font-weight: 500; color: var(--mid); line-height: 1.5; }
.show-card.accent-carbon { border-top-color: var(--primary); }
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
- **Ghost 数字**（默认）：`20px 700, --accent, opacity .4` — 用于顺序列表（`01`、`02`、`03`）
- **图标圆**：小圆（24 px）+ 符号（`!`、`✓`、`→`）— 用于发现项、告警。配语义背景色。
- **字母 / 标签**：单字母或短标签，同样的 ghost 样式 — 用于分类条目。

### 7.4 Stat Card (Tier 4 — "number card")

紧凑指标展示。`stat-num`（48 px 700 `--ink`）+ `stat-label`（12 px 700 全大写 `--mid`）。Xiaomi 的数字风格是大、克制、单色 —— 不要给 stat-num 染橙色（保留橙色给 eyebrow 的小三角）。

### 7.5 Callout / Note

**轻量**（内嵌备注）：
```css
.snote { border-left: 3px solid var(--accent); padding: 10px 18px; background: var(--tint); font-size: 14px; font-weight: 600; }
```

**深色**（结论 / 建议条）：
用于 slide 末尾 takeaway 的全宽 carbon 块（`var(--primary)`）。文字：13–16 px 600–700，`rgba(255,255,255,.85)`。关键词加粗用 `color: #fff`。不要 border-left — 实心 carbon 填充本身就是强调。

### 7.6 Marks, Badges & Chips

**状态标记**：
```css
.mark::before { display: inline-block; width: 18px; height: 18px; border-radius: 50%; text-align: center; line-height: 18px; font-size: 11px; font-weight: 700; margin-right: 8px; }
.mark.yes::before { content: '✓'; background: var(--green); color: #fff; }
.mark.no::before  { content: '−'; background: var(--red); color: #fff; }
```

**徽章** — 小型标签胶囊（`.bg-g`、`.bg-r`、`.bg-o`）用于行内状态。12–13 px、字重 700、全大写。`.bg-o` 是 Xiaomi 橙背景胶囊，但**整张 slide 最多用一个橙徽章**。

**技术 chip** — 紧凑的行内标签，用于技术 / 特性名（"Snapdragon 8 Gen 5"、"Leica Summilux"）。13 px 600，`min-height: 26px`。

### 7.7 Table (`.dt`)

```css
.dt { width: 100%; border-collapse: collapse; font-size: 14px; font-weight: 500; }
.dt th { background: var(--primary); color: #fff; font-size: 13px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; text-align: left; padding: 10px 14px; }
.dt td { padding: 10px 14px; color: var(--ink); border-bottom: 1px solid var(--rule); }
.dt tr.hi td { background: var(--tint); }
.dt .pos { color: var(--green); font-weight: 700; }
.dt .neg { color: var(--red); font-weight: 700; }
.dt .neu { color: var(--mid); font-weight: 500; }
```

**规则：**
- Carbon 表头行（`var(--primary)`）是唯一的色块。所有数据单元格：白底、`--ink` 文字。
- **`<table>` 单元格里不要彩色徽章** — 用字重 / 颜色强调。
- 可选一行 `--tint` 高亮，仅给最重要的那一行（"highlight Xiaomi" 行）。
- "整洁网格"测试：眯眼看表格。看到一堆彩色方块拼贴，就是设计失败了。

### 7.8 Charts

| Type | Primary colour | Secondary | Neutral | Notes |
|---|---|---|---|---|
| Bar (H / V) | `--accent` | `--mid` | `--rule` | Animated grow on entrance |
| Progress / gauge | `--accent` fill | — | `--rule` track | 8px height, 4px radius |
| Pie / donut | `--primary` | `--accent` | `--rule` | Max 3 segments |
| Timeline | `--accent` dots | — | `--rule` line | Key nodes: `--tint` ring |

每张图最多 2 种颜色（+ `--rule` 中性色）。入场动效：bar 增长、计数器累加。Xiaomi chart 永远不用 `--green/--red/--teal` 作为图表色 —— 那些保留给语义状态。

### 7.9 Tabs

```css
.tabs { display: flex; gap: 6px; margin-bottom: 14px; }
.tb { padding: 7px 16px; border: 1px solid var(--rule); background: transparent; font: 700 12px/1 'PingFang SC', 'MiSans Latin', sans-serif; letter-spacing: .06em; color: var(--mid); cursor: pointer; }
.tb:hover { border-color: var(--accent); color: var(--accent); }
.tb.on { background: var(--primary); border-color: var(--primary); color: #fff; }
.tc { display: none; } .tc.on { display: block; }
```

最多 4 个标签。

### 7.10 Sequential steps / barriers
用 monospace-weight span 的数字标签 `01` `02` `03`、`--accent` 色，而不是 bullet 或装饰 emoji。

### 7.11 Decision questions
前缀用 `Q.1` / `Q.2` 的 span，`--accent` 色、字重 700、字距 0.12 em。

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
  font-size: 22px; font-weight: 700; letter-spacing: -.01em; color: var(--accent);
  min-height: 48px; margin-bottom: 16px;
  display: flex; align-items: flex-end; justify-content: center;
}
.tl-dot2 { width: 18px; height: 18px; border-radius: 50%; background: var(--rule); margin-bottom: 12px; flex-shrink: 0; transition: transform .3s ease; }
.tl-dot2.active { background: var(--accent); transform: scale(1.2); }
.tl-name { font-size: 18px; font-weight: 700; color: var(--ink); line-height: 1.2; margin-bottom: 4px; }
.tl-detail { font-size: 14px; font-weight: 500; color: var(--mid); line-height: 1.3; }
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

Xiaomi 的视觉语言**严重依赖产品摄影**。设计 deck 时，不要用插图、emoji、stock 渐变占位 —— 找真实的 Xiaomi 产品照、UI 截图、或 CSS 自绘几何图形。从 mi.com / Xiaomi Newsroom / Mi Community 抓官方素材，永远不要 AI 生成假产品图。

### 何时加入图像

- **产品 UI 截图**：当讨论 HyperOS / 米家 App / Mi Home 的某具体功能时，展示它的真实界面。
- **数据可视化**：当某个数字或趋势是核心时，建一张图（Type H）。
- **环境照片**：Leica 联名摄影、SU7 实景、米家场景照 —— 当某场景需要视觉锚点时。
- **图示**：当某概念具有结构（层级、流程、对比）时，用 CSS/SVG 画出来，而不是用文字描述。

### 如何获取图像

1. **从 mi.com 抓**：用 web search 找产品 hero（如 https://i02.appmifile.com/... 域名下的官方素材）。优先选 Xiaomi 官方资源。
2. **CSS 绘制替代品**：柱状图、进度条、时间线图 — 数据简单时优于外部图片。
3. **绝不用**：装饰性 stock photo、抽象渐变、AI 生成的占位艺术、与 slide 主旨无关的图片。

### 图像处理

- `border-radius: 4px`。浅色背景上可选 `1px solid var(--rule)` 边框。
- 深色背景上的图：不要边框。
- 说明文字：图下方使用 `.cap` 样式（`.cap { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: .14em; color: var(--mid); }`）。
- 绝不在繁忙图像上直接放文字而不加 scrim（最少 `rgba(0,0,0,.5)`）。

---

## 9. 导航 <!-- ENGINEERING-DNA -->

### 圆点导航 — 底部居中，横向

```css
#nav { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 7px; z-index: 99; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,.25); cursor: pointer; transition: all .22s ease; }
.dot.on { width: 20px; border-radius: 3px; background: var(--accent); }
```

> 注意：active dot 用 `--accent`（橙），不用半透明白 —— 这是 Xiaomi 把橙色作为唯一签名色的一致性表达。

### Slide 计数器 — 右下角
`SLIDE N / TOTAL` — 12 px、字重 600、35% 白。

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

**"橙块"陷阱**：右下角的橙色 callout = 视觉失衡。改成全宽底部、用 `.snote` 替代、或把橙色 callout 放在顶部。

**"橙叠 carbon"陷阱**：在深色 slide（`--primary` bg）上，永远不要把橙色 `--accent` 当大块文字背景或大块 fill —— 会产生刺眼、廉价感的对比。在深色背景上，橙色只用作小尺寸 mark / eyebrow / 单行 hairline accent。大块强调用白色（`#fff`）或半透明白（`rgba(255,255,255,.85)`）。

**"深色堆叠"陷阱**：当一个深色元素直接放在另一个深色元素下方时，它们在视觉上合并。深色元素之间至少留 12 px `--surface` 或 `--tint` 间距。

**Header-内容去重**：`.shd-n` 条已经承载了 slide 的章节标签。不要在内容区里再重复同样的文字作为单独的 eyebrow/标题。

### 间距

| Token | 值 |
|---|---|
| 左水平内边距 | 96 px |
| 右水平内边距 | 80 px |
| 上下内边距 | 24 / 40 px (Xiaomi 默认非对称) |
| 页头高度 | 54 px |
| 卡片间距 | 20 px |
| 卡片内边距 | 22 px (Tier 2) / 32 px (Tier 1) |
| 圆角 | 4 px (cards / images) / pill (buttons) |
| 分隔线粗细 | 1 px |
| Accent 边线 | 3 px |

---

## 13. 上线前检查清单 <!-- ENGINEERING-DNA: pre-ship-checklist -->

分享 deck 之前，逐项核对。

### 品牌与 Token
- [ ] 每张 slide 都有 logo（封面右上、内容页 `.shd` 右端）
- [ ] **Logo 在封面肉眼可见** —— 打开 deck，看 slide 1 右上角。"内嵌成功但不可见"是最常见的失败模式（见 §4）。`has_real_vector_path: true` 单独并不能保证视觉上看得见。
- [ ] Logo 使用 `<image href="data:image/svg+xml;base64,...">` 形式（B 档），CSS `.logo` 上**没有** `fill:` 属性
- [ ] **封面 logo 周围没有非预期的白色 halo** —— Xiaomi 默认不加 chip。
- [ ] **每张 slide 内容都包在 `.sc` 容器内** —— 包括 bespoke 满屏 Type J / Type A。不能用平级 shell 如 `.fpwrap` / `.poster-wrap`（这种自定义 shell 会**静默绕过** `fit_contract_intact`）
- [ ] 颜色：只用系统 token — 不用临时 hex
- [ ] 所有 bespoke 元素都仅基于系统 token 构造（见 §1 约束 vs 自由）
- [ ] 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 可用
- [ ] MiSans Latin 300-700 已加载（通过 Xiaomi CDN `@import`）；CJK 链含 PingFang SC / Microsoft YaHei；不用 serif / display 字体
- [ ] 封面副标：仅用 MiSans Latin 300（MiSans 没有斜体；仅靠字重区分层级）

### 字体与可读性
- [ ] 没有低于 12 px 的文字 — 特别注意徽章 / 标签列
- [ ] Slide 标题 ≥ 50 px（仅在密集多行例外时降到 38 px）
- [ ] 非表格 slide 的正文 ≥ 16 px（仅在数据密集表格上用 14 px）
- [ ] 副标 ≥ 20 px
- [ ] 中文与对应英文字号 / 字重一致（混排时）；中文标题用 700，正文用 500

### 幻灯片结构
- [ ] 每张内容页都有 `.shd` 页头条 + slide 编号 + logo
- [ ] 封面没有装饰线 — 不要 hairline、不要 accent line、不要渐变边框
- [ ] 每张 slide 都在 720 px 内 — 没有内容剪裁或溢出
- [ ] 没有"橙块"陷阱 — 橙色 callout 不孤立在双栏布局的右下角
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
- [ ] 图像服务于理解 — 不用装饰性 stock photo（Xiaomi 用真实产品摄影）
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
