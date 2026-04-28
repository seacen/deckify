# Apple-PPT-Design-System

> 为 Apple 制作的所有 deck 共用的视觉语言。请严格遵循，让每一份新 deck 都一眼被识别为同一家族。

---

<!--
  TEMPLATE NOTES (delete this comment block in the generated output):

  Sections marked <!-- BRAND-VARIABLE --> must be filled with brand-specific content.
  Sections marked <!-- ENGINEERING-DNA --> must be copied verbatim. They came from
  real, painful bugs in production decks. Do NOT "simplify" or "trim" them — every
  line earns its place.

  Placeholder syntax: --primary. Replace each from $WS/decisions.json.
-->

## 1. 设计理念

<!-- BRAND-VARIABLE: 1-2 paragraphs capturing the brand's mood + a "Constraints vs Freedom" block -->

****Premium reductive restraint。** Apple 的视觉语言是「白底黑字 + 大字 + 紧排版」。SF Pro Display 80 px 标题贴近 billboard，#1D1D1F 正文，#86868B 次级，蓝色 `#1B9CF7` 仅作 accent 出现在 CTA 链接 / 选中状态。决不允许多余装饰。**

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
- SF Pro Display / SF Pro Text typeface, no serif/display fonts - SF Pro Display 用于 ≥ 28 px 标题、billboard 大字
- SF Pro Text 用于 ≤ 22 px 正文、UI、表格
- 绝不混入第三种字体
- 12 px 可读性下限
- 每一张 slide 都必须有 logo
- 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 和几何指示符允许
- 不用装饰性 stock photography
- `.shd` header strip on content slides
- `.sw` border-left accent

**可复用组件（按需选用，不强制）：**
- §7 组件库提供卡片、表格、图表、标签、标记 — 适合时用，不适合时跳过用 bespoke 布局。

**Bespoke 元素（鼓励）：**
- **在调色板内自由发挥。** 封面用纯白 + 大黑字标题（SF Pro Display 80 px Semibold）+ 18 px 副标 — 不加任何装饰元素，Apple logo 是唯一品牌标记。内容页同样白底，标题 50 px，正文 17 px，蓝色出现在 CTA 链接处一处即可。封面、产品 hero、billboard 时刻可反转为纯黑底 + 白字。
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
  --primary:  #000000;   /* Dominant brand chord — cover bg, primary mark colour */
  --accent:   #1B9CF7;   /* CTA / link / single saturated highlight */
  /* ── Neutrals ── */
  --surface:  #FFFFFF;   /* Paper / slide bg */
  --white:    #FFFFFF;
  --ink:      #1D1D1F;   /* Body text on light surfaces */
  --mid:      #86868B;   /* Secondary text / muted labels */
  --rule:     #D2D2D7;   /* Dividers / hairlines */
  --tint:     #F5F5F7;   /* Subtle row / section bg */
  /* ── Semantic (invariant names; values may map to brand-palette colours) ── */
  --green:    #0E9F6E;   /* Positive */
  --green-bg: #D1FAE5;
  --red:      #FF3B30;   /* Negative */
  --red-bg:   #FEE4E2;
  --warn:     #F59E0B;   /* Warning / caution */
  --warn-bg:  #FEF3C7;
  --teal:     #1B9CF7;   /* Informational / neutral highlight */
  --teal-bg:  #D6EBFF;
  /* ── Brand palette (brand-specific names; expanded from brand.json accents+neutrals) ── */
  --mist:        #F5F5F7;
  --mute:        #86868B;
  --violet:      #960AE9;
  --graphite:    #1F1F22;
  --rule:        #D2D2D7;
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

**SF Pro Display / SF Pro Text** — 唯一字体。字重 300, 400, 500, 600, 700；不使用斜体（Apple 风格中斜体只用于品牌名引用 / 媒体标题）。`'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', system-ui, -apple-system, sans-serif` 作为 完整字体栈（标题用 SF Pro Display，正文用 SF Pro Text — Apple 系统字体在生产现场可通过 system-ui 自动获取）。

> Apple 字体系统的关键 — billboard scale 标题（80–96 px SF Pro Display Semibold），细密正文（17 px SF Pro Text Regular）。字距非常紧（−0.04 em），行高同样紧 (0.95–1.05) — 这是 Apple 的 hallmark：大字 + 紧排版 + 大量留白。

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

## 4. Apple Logo <!-- BRAND-VARIABLE: SVG payload is brand-specific; surrounding pattern + multi-format support is ENGINEERING-DNA -->

### 定义（每份 HTML 一次）

Logo 必须是真实的品牌身份资产，**完整内嵌**到 HTML 中（不依赖外部网络）。允许两种内嵌路径；`embed_logo.py` 自动选择：

**A. SVG 矢量路径**（首选） — 当能从品牌站点、Wikipedia 或品牌素材页拿到 SVG 源时使用：

```html
<svg style="display:none" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 302 302" fill="currentColor">
    <image href="data:image/png;base64,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Z2VSZWFkeXHJZTwAAAOGaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA1LjYtYzExMSA3OS4xNTgzMjUsIDIwMTUvMDkvMTAtMDE6MTA6MjAgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZjAyODJiMTQtMTk5MC00N2Y2LWE3MjMtMjE1ZjYxMWE3MWI5IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjBEMzc0NzEzMEJFNTExRTZCMTA3OUQ2MjY2NjM3NkJEIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjBEMzc0NzEyMEJFNTExRTZCMTA3OUQ2MjY2NjM3NkJEIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE1IChNYWNpbnRvc2gpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6ZDI2OGQ5YWUtYmEzMS00YTllLWFjOTQtNGU3NDAxMTVlOWRiIiBzdFJlZjpkb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6Mzc2ZDJlMjQtNTQ1Yy0xMTc5LTk5MGQtZmNiNGVkODNhNmY3Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRh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" width="302" height="302"/>  <!-- inner <path>/<g> carry no explicit fill, so currentColor cascades in -->
  </symbol>
</svg>
```

**B. PNG/JPG/WebP base64 内嵌**（位图 fallback） — 仅有位图 logo 时（最小 64×64），base64 编码后通过 `<image href>` 包进同一个 `<symbol>`：

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 670 670">
    <image href="data:image/png;base64,{{LOGO_BASE64}}" width="670" height="670"/>
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
<svg class="logo W" viewBox="0 0 302 302" aria-label="Apple">
  <use href="#brand-wm"/>
</svg>

<!-- 品牌深色（浅色 slide 上） -->
<svg class="logo L" viewBox="0 0 302 302" aria-label="Apple">
  <use href="#brand-wm"/>
</svg>
```

```css
/* fill: currentColor 必须放在 .logo 上 — 不要放在 .logo path 上。
   CSS 选择器无法穿透 SVG <use> 的 shadow DOM。
   外层 <svg> 上的继承 fill 才能正确级联进去。 */
.logo   { height: 32px; width: auto; flex-shrink: 0; fill: currentColor; }
.logo.W { color: #fff; }
.logo.L { color: var(--primary); }
```

### 摆放规则 <!-- ENGINEERING-DNA -->
- **每张 slide** 都必须有 logo — 封面与所有内容页。
- **封面**：`.cov-top` flex 行的右上角。
- **内容页**：`.shd` 页头条的右端（左 = 标题 eyebrow / slide 编号，右 = logo）。
- Logo 周围最小留白 = logo 高度（32px）四周都留。
- 不要拉伸、不要在 `W`/`L` 之外重新着色、不要把 logo 叠在带图案的区域上。

> Apple logo 受品牌使用规范严格保护。本 deck 内嵌的是 SVG 银色 / 黑色 mark — 不要变形、不要重新着色（除黑 / 白以外），不要叠在带杂色的背景上。

---

## 5. 幻灯片架构 <!-- ENGINEERING-DNA — the entire section, invariant -->

### 脚手架
```
#wrap — fixed fullscreen, flex-centre
  #deck — 1280 × 720, position:relative, overflow:hidden (hard contract)
    .slide × N — absolute inset, opacity show/hide, overflow:hidden (hard contract)
```



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

> **Emphasis for Apple**: **Apple 强调**：每张 slide 都该感觉像 Apple Event 的某一帧 — 大字、暗黑或纯白背景、产品或一句话作为唯一焦点。删减优先于增加。
> Foreground these types when designing decks: Type J（pull-quote — Tim Cook / Steve Jobs / 发布会一句话节奏）、Type F（产品 hero 图）、Type H（性能数据 / 销量图表）.
> Use sparingly: Type D（flip cards — Apple 不爱用花哨交互）、Type I（标签页 — Apple 偏好分页 anchor）.

### Type A — 封面
- 背景：``#FFFFFF` 纯白 — Apple 的标志做法；产品 / billboard 时刻可用 `#000000` 全黑反转`
- 结构：Logo 右上角 → Eyebrow → 巨型标题 → 斜体副标 → Meta 行
- **不允许任何装饰线** — 不要 hairline、不要 accent line、不要渐变边框。背景就是表面。

### Type B — 双栏内容
对比、特性列表、指标。`grid-template-columns: 1fr 1fr; gap: 20px`。移动端会折叠为单栏。

### Type C — 全宽叙事
单栏、大字号、配 pull-quote。用于上下文、摘要、推荐建议页。

### Type D — 翻面卡片
两张卡片并排。正面 = `--primary`，背面 = `#000000`（比 `--accent` 柔和）。**Hover + 点击翻面** — JS `onclick` 切换 `.on` class（移动端必需）。正面有 ghost 罗马数字。背面留白宽（32 px padding，≤ 4 个内容元素）。

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
- 标题陈述洞察，不是图表类型。好："Apple 在三项维度都领先"。坏："柱状图对比"。
- 图表占 slide 区域 50–70%。剩余空间：标题 + 一段解读或一个 callout。
- 入场动效以增强叙事冲击力。

### Type I — 标签页
多个内容视图通过标签切换。当内容有自然分类时，能在一张 slide 上容纳更多信息。Tab 组件规范见 §7.9。

**原则：** 最多 4 个标签。每个 tab panel 都是自包含的"slide-中-slide" — 可以用 §7 任何组件。不要把标签当成 slide 内容塞太满的拐杖；如果 2 个标签各自都显稀疏，就合并成一个视图。

### Type J — 引言/抽词
一句强烈的话锚定叙事时刻。用于关键 takeaway、受众重置、可记忆的金句。

**结构：** 大号引用文字（28–36 px、字重 700、`--ink`）居中或左对齐。可选下方署名（14 px、`--mid`）。左边 accent 边线（`3px solid --accent`）或无。

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
.tb { padding: 7px 16px; border: 1px solid var(--rule); background: transparent; font: 800 12px/1 'SF Pro Display / SF Pro Text'; letter-spacing: .06em; color: var(--mid); cursor: pointer; }
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

Apple 图像 = 产品 hero shot 或人物在使用产品的瞬间。永远不用 stock photo。透明背景 PNG 或纯黑 / 纯白 hero photo — 让产品成为画面的全部。

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
| 圆角 | 12 px 卡片，22–28 px 大面板（macOS / iOS 系统圆角），按钮 980 px 全 pill |
| 分隔线粗细 | 1 px |
| Accent 边线 | 3 px |

---

## 13. 上线前检查清单 <!-- ENGINEERING-DNA: pre-ship-checklist -->

分享 deck 之前，逐项核对。

### 品牌与 Token
- [ ] 每张 slide 都有 logo（封面右上、内容页 `.shd` 右端）
- [ ] 颜色：只用系统 token — 不用临时 hex
- [ ] 所有 bespoke 元素都仅基于系统 token 构造（见 §1 约束 vs 自由）
- [ ] 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 可用
- [ ] SF Pro Display / SF Pro Text 300, 400, 500, 600, 700不使用斜体 已加载；不用 serif / display 字体
- [ ] 封面副标：仅用 SF Pro Display / SF Pro Text 300 斜体（如果 300 italic 不可用，用品牌等价值）

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
