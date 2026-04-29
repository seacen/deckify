# Mars-PPT-Design-System

> 为 Mars, Incorporated 制作的所有 deck 共用的视觉语言。请严格遵循，让每一份新 deck 都一眼被识别为同一家族。

---

## 1. 设计理念

**Mars 的视觉语言是把家族企业的乐观主义、工业级的生产规模、以及 Five Principles（Quality / Responsibility / Mutuality / Efficiency / Freedom）这套秩序感，翻译成几何上极度自信的色块拼贴。深玛氏蓝（Mars Blue #0000A0）是不可动摇的主导和弦；它旁边按业务部门并排展开高饱和原色：Petcare 的纯红、Food 的草绿、Wrigley 的金黄、糖果黄、可持续 fresh-green。零圆角、零阴影、零渐变 —— 表面就是颜色本身，像 1970 年代 IBM 的彩色印刷品或 Bauhaus 海报，不是 SaaS dashboard。这套 DS 的目标是：每一张 slide 第一眼就能被认出是 Mars 出品 —— 不是又一份得体的 corporate 演示。**

**两种模式：**
- **桌面端 (≥ 769 px)**：1280 × 720 px 画布，运行时 scale-to-fit (§5)，键盘/点击导航。
- **移动端 (≤ 768 px)**：所有 slide 垂直堆叠成一张可滚动的长页；单栏布局。

### 设计品味 <!-- ENGINEERING-DNA: design-taste -->

**承诺一个清晰的审美立场。** 本 DS 是品牌工具，不是 SaaS 通用模板。基于它做的每一份 deck 第一眼就该让人认出这是 *Mars* — 不是"又一份得体的商务演示"。极致繁复与极致简约都能成立；失败模式是中庸。

**反 AI 套路规则**（每张 slide、每个组件、每个变体都适用）：

- **不用通用字体默认值。** 品牌字体在 §3 已指定（Inter 作为 MarsCentra 的合法替身），必须使用并按字重梯度排布；不要把 Arial / system-ui 当做"设计选择"。
- **不用陈词滥调的配色。** 纯白底 + 一个紫/蓝色 accent + 板岩灰字 = AI 套路签名。Mars 的语言是 mars-blue 主导和弦 + 多色业务部门口袋 — 按层级使用，不要扁平化成"白+灰+一种 accent"。
- **不用等权重的多色装饰网格。** Mars 的多色调色板是按业务部门 *分类语义*（Petcare 红、Food 绿、Wrigley 金、Snacking 黄）排布的，不是装饰性矩阵。一张 slide 最多用一个装饰性品牌色；多色并列只在「业务部门 tile」这种语义场景下出现。
- **不用现成 SaaS 仪表盘 chrome。** 每个组件都 8 px 圆角 + 柔和 drop-shadow + 整齐间距，会把 Mars 做成一个无名 SaaS。Mars 是 **零圆角、零阴影、平面几何**（§2 / §12）—— 偏离这一点就背离了品牌真实视觉。
- **不用空洞的氛围词。** "现代、简洁、大胆"什么都形容因此什么都不形容。Slide 标题和段落文案应该具体、具象（"全球 100+ 国家、80,000 名 Associates"，不是"全球化、规模化"）。
- **一个编排好的入场动效，而非分散的小动画。** 大部分 slide 只需要一次激活时的内容错时显现；不要给每张卡都加 hover 抖动。

### 约束 vs 自由 <!-- ENGINEERING-DNA framing; bullet contents are BRAND-VARIABLE -->

本 Design System 定义了 **硬约束**（永远不能破的）与 **可复用组件**（按需选用的）。它不定义现成配方 — 每张 slide 都应为它自己的内容构图，而不是从模板拼接。

**硬约束（锁死）：**
- Colour palette (§2 tokens only — no ad-hoc colours)
- Inter typeface（作为 MarsCentra 的合法替身），no serif/display fonts；中文走 PingFang SC 优先回退链
- 12 px 可读性下限
- 每一张 slide 都必须有 logo
- **每张 slide 的内容必须包在一个 `.sc` 容器里**（即使是 bespoke 满屏的 Type J / Type A 也是）。`.sc` 是 `fit_contract_intact` 唯一扫描的位置 — bespoke 布局如果直接画在自定义 shell 里（`.fpwrap` / `.poster-wrap` 之类），会**静默绕过** absorber 检测、移动端 catch-all、602 px 预算这三道保险。没有 `.sc`，就没有契约。
- **Logo `<symbol>` 内部不能含任何 `fill` 属性**（包括 wrapper `<g>` 上的 `fill="none"`）。任何内层 fill 都会盖过 `currentColor` 级联，使 wordmark 完全不可见 —— 而 byte 级检查（path d 长度、viewBox、visible_on_cover）会一切显示 PASS。`embed_logo.py` 在物化时已 strip 这些；`logo_renders` hard check 会拒绝任何漏网的。
- 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 和几何指示符允许
- 不用装饰性 stock photography
- `.shd` header strip on content slides
- `.sw` border-left accent
- **零圆角（border-radius: 0）**：所有卡片、按钮、表格单元格 — Mars 实际站点上每个组件 radius 都是 0，不是 4 px、不是 8 px。
- **零阴影**：盒子靠边线和颜色对比表达层级，不要 box-shadow（hover 状态下的轻微 lift 是唯一例外）。

**可复用组件（按需选用，不强制）：**
- §7 组件库提供卡片、表格、图表、标签、标记 — 适合时用，不适合时跳过用 bespoke 布局。

**Bespoke 元素（鼓励）：**
- **在调色板内自由发挥。** Mars 的强项是把一整张 slide 涂成 mars-blue，叠满屏 Inter Black 900 的标语，标语中的关键词用 mars-green 或 snack-yellow 染色（参考 Five Principles 页：白色 *Quality* 旁边一行 mars-green 的 *Responsibility*，再一行白色 *Mutuality*，再一行 snack-yellow 的 *Efficiency*）。这种排版即海报的处理就是 Mars 最具识别度的 bespoke 模式。
- 判定标准是：该元素是否只用了定义过的颜色 token、品牌字体、并尊重可读性下限？如果是，即便不匹配任何具名组件也算"在系统内"。
- **不要自我限制在具名组件里。** 如果某 slide 需要 §7 不存在的东西，就从 token 出发自己造。最好的 slide 都是从系统 token 出发的 bespoke 构图。

---

## 2. 颜色令牌 <!-- BRAND-VARIABLE: hex values + brand-palette names; core role token names are invariant -->

颜色 token 系统有三层：

1. **核心角色 token** — 所有品牌之间名字不变。它们标识颜色 *扮演什么角色*，而不是 *它是什么颜色*。红色品牌的 `--primary` 是红色；蓝色品牌的 `--primary` 是蓝色。
2. **语义 token** — 所有品牌之间名字不变；编码含义（正向 / 负向 / 警告 / 信息）而不是颜色身份。
3. **品牌调色 token** — 品牌特有的名字 + hex。Mars 的命名照搬其内部 `--ssa-color-palette-*` 系统：`--mars-blue`、`--mars-green`、`--mars-edge`、`--petcare-red`、`--food-green`、`--wrigley-gold`、`--snack-yellow`、`--fresh-green`、`--spicy-red`。

```css
:root {
  /* ── Core role tokens (invariant names) ── */
  --primary:  #0000A0;   /* Mars Blue — Dominant brand chord; cover bg, primary mark colour, footer */
  --accent:   #00D7B9;   /* Mars Green — CTA / link / single saturated highlight on dark surfaces */
  /* ── Neutrals ── */
  --surface:  #FFFFFF;   /* Paper / slide bg */
  --white:    #FFFFFF;
  --ink:      #3C3C3C;   /* Body text on light surfaces (matches --ssa-color-palette-dark-grey) */
  --mid:      #6B6B6B;   /* Secondary text / muted labels */
  --rule:     #E1E1E1;   /* Dividers / hairlines */
  --tint:     #F4F4F4;   /* Subtle row / section bg (matches --ssa-color-palette-background-gray) */
  /* ── Semantic (invariant names; values may map to brand-palette colours) ── */
  --green:    #00D7B9;   /* Positive — maps to mars-green */
  --green-bg: #E5FAF6;
  --red:      #FF1414;   /* Negative — maps to petcare-red */
  --red-bg:   #FFEBEB;
  --warn:     #E6A000;   /* Warning / caution — maps to wrigley-gold */
  --warn-bg:  #FFF6E0;
  --teal:     #0099FF;   /* Informational / neutral highlight — maps to mars-edge */
  --teal-bg:  #E0F2FF;
  /* ── Brand palette (Mars-specific names; from --ssa-color-palette-*) ── */
  --mars-blue:     #0000A0;   /* Primary chord; same as --primary */
  --mars-green:    #00D7B9;   /* Cool mint accent on Mars Blue surfaces */
  --mars-edge:     #0099FF;   /* Sky blue — science / innovation contexts */
  --petcare-red:   #FF1414;   /* Petcare division (Pedigree / Whiskas / Royal Canin) */
  --food-green:    #61A020;   /* Food & Nutrition (Ben's Original / Dolmio) */
  --wrigley-gold:  #E6A000;   /* Mars Wrigley confectionery (Orbit / Extra) */
  --snack-yellow:  #FFDC00;   /* M&M's / Snickers signature yellow */
  --fresh-green:   #A6DB00;   /* Sustainability narratives */
  --spicy-red:     #FF3C14;   /* Energy / urgency accent */
  --light-gray:    #A3A3A3;   /* Disabled state / inactive icons */
}
```

**规则：** <!-- ENGINEERING-DNA -->
- **Token 名是角色抽象，不是颜色名。** `--primary` 是品牌的主导和弦，对 Mars 就是 mars-blue。Slide CSS 读 `var(--primary)` 就能拿到正确颜色，业务 slide 代码不需要知道 hex。
- **每张 slide 只有 *一个* 主导 accent 颜色。** 用 `--accent` 做 slide 的标志性高亮（CTA、callout 边线、chart 主条）。品牌调色 token（如 `var(--snack-yellow)`、`var(--petcare-red)`）是按需取用的装饰，不是并行 accent — 一张 slide 最多用一个装饰性品牌色。**例外**：当 slide 主旨 *就是* "多业务部门并列"时（业务版图 tile slide），可以同时使用 4 个部门色 — 这是语义网格不是装饰。
- **语义颜色仅在含义彼此独立、相对时才同时出现** — 例如一张对比 slide 的 ✓ (`--green`) / ✗ (`--red`)。否则只取一种。
- **`--tint` 用于行底色，不用于卡片填充。**
- **永远不用纯黑。** `--primary` 是品牌真实的深色（mars-blue #0000A0）；要做"近黑"基调用 `--ink` (#3C3C3C)，那是 Mars body 文字的真实颜色。
- **永远不在 slide CSS 里写临时 hex。** 每个颜色都必须来自 token。`token_only_colors` hard check 会强制执行。

---

## 3. 字体 <!-- BRAND-VARIABLE: font family + fallback; the scale below is mostly invariant -->

**Inter** — 唯一字体（作为 Mars 自有付费字 MarsCentra 的合法替身）。字重 400 / 500 / 600 / 700 / 800 / 900。`system-ui` 作为系统兜底。

> Inter 为什么是合理替身：MarsCentra 是几何 grotesque、字重 400→900 全梯度、x-height 较高、字距偏紧 — Inter 在所有这些维度都最接近，且 Extrabold/Black 都厚重到能撑得住 Mars 标志性的"满屏粗体标语"。Helvetica 太瑞士、太冷；Roboto 太软；Arial 直接掉档次。Inter 是这个生态里最贴 MarsCentra 的免费选择。

### CJK 字体回退链 <!-- ENGINEERING-DNA: cjk-fallback -->

中文 deck 不能直接用拉丁字体当 body font。Inter / Helvetica Neue / SF Pro / Stripe Sans / Georgia 等都不含 CJK 字形，浏览器对 CJK 字符自动回退到系统默认（macOS 上是 STHeiti 细体，Windows 是微软雅黑 Light），**视觉上立刻显得廉价**。

**最低要求**：font-family 链里**必须至少出现一个 CJK 字体名**（PingFang SC / Hiragino Sans GB / Microsoft YaHei / Source Han Sans 等），否则 CJK 字符 100% 落到 OS 默认。`cjk_font_quality` hard check 会强制执行这一条。

**两种合理的字体顺序**（按 deck 的语言比例选）：

1. **CJK-first**（推荐用于中文密度高的 deck）：CJK 字体放最前，拉丁 brand 字体兜底。中英混排时 PingFang 的拉丁补丁会渲染英文，整体风格最统一，中文不会因为字重不匹配显得瘦弱。
2. **Latin-first**（适用于 brand 拉丁字面强、deck 大量英文术语的场景）：拉丁 brand 字体放前，CJK 字体跟在后面。CJK 字符会走 CJK 字体，但拉丁部分保留 brand 表达。`cjk_font_quality` 在这种情况下会带 `warning`（不阻断），由 vision judge 决定视觉是否可接受。

```css
/* Mars 中文 deck 推荐字体链 — CJK 优先，Inter 兜底 */
font-family:
  /* macOS / iOS 中文（最高优先级） */
  'PingFang SC', '苹方-简',
  /* macOS 较旧 */
  'Hiragino Sans GB', '冬青黑体简体中文',
  /* Windows 中文 */
  'Microsoft YaHei', '微软雅黑',
  /* Linux / Android / 通用 */
  'Source Han Sans SC', 'Noto Sans SC', 'Noto Sans CJK SC',
  /* Brand 拉丁字体 (MarsCentra 替身) */
  'Inter',
  /* 系统通用 */
  system-ui, -apple-system, sans-serif;
```

**Mars 是 sans-serif brand**（MarsCentra 几何 grotesque）→ 配 PingFang SC / Microsoft YaHei / Source Han Sans 这类 sans CJK 字体，绝不要用 Songti / 宋体（serif 与 Inter 配会跳戏）。

**字重提升（CJK-first 时尤其重要）**：PingFang SC 的 Regular（400）较细 — 大字标题用 700（Semibold/Bold），正文用 500（Medium）以上，避免"中文显瘦"的廉价感。Mars 的视觉自信很大程度依赖 Extrabold / Black 字重撑得住 — 中文回退链里务必把 weight 推高。

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
   - 然后，**改布局**(去掉一项、拆分 slide、把列表改成双栏网格)。
   - **永远不要** 通过把字号缩到 12 px 以下或允许截断来"塞下"。

---

## 4. Mars Logo <!-- BRAND-VARIABLE: SVG payload is brand-specific; surrounding pattern + multi-format support is ENGINEERING-DNA -->

### 定义（每份 HTML 一次）

Logo 必须是真实的品牌身份资产，**完整内嵌**到 HTML 中（不依赖外部网络）。Mars 的 wordmark 来自其官方站点 `themes/custom/mars_acss/assets/images/logo-main.svg`（138×40 viewBox，单 path d 长度 3723 字符），由 `embed_logo.py` 物化并通过 `<symbol>` 内嵌：

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 138 40" fill="currentColor">
    <g fill="none" fill-rule="evenodd">
      <g><g><g>
        <path d="M125.73.148c.413.098.821.217 1.238.29 3.345.586 6.317 1.967 8.848 4.288.195.18.37.382.592.615-1.635 1.895-3.414 3.6-5.074 5.493-.13-.129-.23-.22-.32-.318-1.75-1.913-3.906-3.044-6.444-3.381-.886-.118-1.793-.108-2.672.13-1.318.358-2.333 1.094-2.725 2.488-.369 1.315.116 2.64 1.2 3.46.983.743 2.093 1.222 3.237 1.633 2.05.739 4.123 1.414 6.143 2.228 2.059.83 3.982 1.918 5.491 3.638 1.39 1.583 2.288 3.385 2.583 5.507.422 3.028-.34 5.755-1.951 8.27-.987 1.542-2.354 2.677-3.935 3.539-1.987 1.084-4.111 1.704-6.366 1.83-1.014.058-2.032.139-3.045.108-2.927-.09-5.761-.66-8.409-1.977-1.98-.985-3.698-2.339-5.14-4.045-.044-.053-.07-.123-.123-.22 1.69-1.799 3.38-3.595 5.126-5.452.22.24.414.445.6.657 1.11 1.27 2.409 2.275 3.938 2.968 1.046.473 2.131.747 3.272.896 1.106.145 2.174.043 3.234-.206 1.042-.245 1.95-.778 2.56-1.695 1.191-1.79.675-3.75-.96-4.923-.8-.574-1.719-1.013-2.635-1.382-1.48-.598-3.005-1.083-4.509-1.624-1.53-.55-3.034-1.163-4.418-2.039-2.443-1.547-4.194-3.64-4.83-6.553-.574-2.626-.18-5.134 1.062-7.507 1.531-2.926 3.882-4.86 6.937-5.935.891-.314 1.804-.547 2.746-.652.082-.009.158-.084.237-.129h4.512zM50.394 28.081c.198.035.29.065.38.065 2.298-.01 4.595-.021 6.892-.035.02 0 .043-.024.059-.042.014-.017.019-.041.056-.128l-3.591-8.974h-.143l-3.653 9.114zM55.274.148c.394.301.656.695.85 1.155 1.127 2.692 2.26 5.381 3.401 8.067 1.035 2.438 2.085 4.87 3.123 7.306 1.19 2.798 2.37 5.601 3.563 8.398.885 2.076 1.783 4.147 2.676 6.219 1.067 2.478 2.136 4.955 3.202 7.433.067.155.114.317.185.52H62.33c-.397-.977-.804-1.974-1.206-2.972-.128-.318-.254-.638-.364-.962-.118-.348-.321-.507-.705-.487-.604.03-1.212.009-1.818.009h-9.675c-.145 0-.291.01-.436-.003-.305-.025-.477.087-.596.4-.41 1.077-.853 2.141-1.286 3.21-.11.27-.228.536-.347.816h-8.36c.041-.195.05-.36.112-.503 1.606-3.742 3.223-7.479 4.827-11.222 1.97-4.599 3.933-9.202 5.895-13.805 1.192-2.797 2.377-5.596 3.563-8.396.555-1.31 1.11-2.62 1.653-3.934.21-.51.484-.957.96-1.249h.728zM0 .606c.699.108 1.196.43 1.634.876 1.832 1.87 3.668 3.737 5.503 5.604 3.138 3.194 6.277 6.388 9.416 9.58.134.137.28.262.448.42.181-.167.345-.305.495-.457 4.94-5.024 9.882-10.049 14.817-15.079.456-.464.954-.824 1.59-.928.037.032.057.046.074.064.016.016.04.035.042.055.012.097.024.195.024.293l.001 38.123c-.525.155-6.51.208-7.84.072V20.854c-.653.495-1.088 1.039-1.578 1.52-.524.513-1.032 1.044-1.547 1.567l-1.492 1.52-1.492 1.517c-.516.523-1.037 1.039-1.548 1.567-.492.509-.972 1.03-1.509 1.599L7.952 20.91c-.065.044-.085.052-.097.067-.015.018-.029.042-.032.065-.007.048-.01.098-.01.147-.005 5.974-.009 11.948-.015 17.921 0 .023-.016.044-.025.066-.502.132-6.678.173-7.773.047V.606zM84.738 7.617c-.119.972-.09 9.734.036 10.334 1.6-.038 3.221.123 4.822-.185 1.3-.25 2.4-.87 3.145-2.04.457-.719.66-1.506.754-2.353.132-1.19-.058-2.308-.638-3.333-.874-1.543-2.307-2.187-3.971-2.333-1.154-.1-2.318-.096-3.477-.131-.212-.007-.424.025-.671.04M75.71 39.198V.809c.172-.015.356-.046.54-.046 4.074-.003 8.15-.03 12.223.01 2.029.019 4.058.153 6.025.73 2.438.716 4.508 2.017 6.07 4.077 1.228 1.621 1.851 3.473 2.027 5.513.136 1.568-.02 3.087-.468 4.582-.677 2.254-2.032 4-3.902 5.357-.212.153-.425.304-.685.489.367.291.67.533.974.772 1.169.92 2.023 2.103 2.772 3.382.971 1.658 1.618 3.456 2.237 5.267.831 2.434 1.66 4.869 2.486 7.304.108.318.196.643.313 1.03h-9.268c-.145 0-.291-.004-.437 0-.228.008-.357-.096-.41-.325-.292-1.24-.568-2.484-.888-3.717-.649-2.491-1.29-4.99-2.493-7.283-.764-1.457-1.873-2.502-3.512-2.84-.495-.103-1.002-.18-1.506-.197-.92-.03-1.843-.01-2.764-.003-.092 0-.184.045-.24.06-.047.048-.066.063-.079.083-.013.02-.022.044-.03.067-.008.023-.016.046-.018.07-.004.05-.007.099-.007.148-.004 4.591-.008 9.182-.014 13.773 0 .022-.018.044-.027.065-.53.127-8.136.148-8.92.02"/>
      </g></g></g>
    </g>
  </symbol>
</svg>
```

> ⚠️ **禁止用文字 placeholder 伪装 logo**：用 `<text>MARS</text>` 假冒 wordmark 属于构建失败。`logo_renders` hard check 会拒绝只含 `<text>` 的 `<symbol>` 块。这个 logo 是从 mars.com 官方站点直接物化的真实矢量。

> ⚠️ **fill 级联陷阱** <!-- ENGINEERING-DNA: logo-inner-fill -->
> mars.com 的 logo SVG 导出器把真实字形 path 包在一个默认组里：
> `<g fill="none" fill-rule="evenodd"><g><path d="..."/></g></g>`。原样粘贴进我们的
> `<symbol fill="currentColor">` 会让内层 `fill="none"` **赢过** 父级 currentColor 级联 ——
> wordmark 渲染出来 **100% 不可见**，而 byte 级检查（path d 长度、viewBox、
> `visible_on_cover` 通过 getBoundingClientRect）全都会显示 PASS。**这就是 Mars 端到端测试中暴露的真实事故**：
> 上面这一段嵌入的 SVG 在最初一版里就因为 `<g fill="none">` wrapper 没被 strip，9 张 slide 全部 logo 不可见。
> **在 embed 前必须 strip 所有内层 `fill` 属性，包括 `fill="none"`。**
> `embed_logo.py` 现在自动 strip；`logo_renders` hard check 现在会拒绝任何不是 `fill="currentColor"` 的内层 fill。
> 如果手工粘贴 logo，肉眼检查 `<symbol>` 块内任何 `fill="..."` 都必须删掉。

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
<svg class="logo W" viewBox="0 0 138 40" aria-label="Mars">
  <use href="#brand-wm"/>
</svg>

<!-- 品牌深色（浅色 slide 上） -->
<svg class="logo L" viewBox="0 0 138 40" aria-label="Mars">
  <use href="#brand-wm"/>
</svg>
```

```css
/* fill: currentColor 必须放在 .logo 上 — 不要放在 .logo path 上。
   CSS 选择器无法穿透 SVG <use> 的 shadow DOM。
   外层 <svg> 上的继承 fill 才能正确级联进去。 */
.logo   { height: 24px; width: auto; flex-shrink: 0; fill: currentColor; }
.logo.W { color: #fff; }
.logo.L { color: var(--primary); }
```

### 摆放规则 <!-- ENGINEERING-DNA -->
- **每张 slide** 都必须有 logo — 封面与所有内容页。
- **封面**：`.cov-top` flex 行的右上角。
- **内容页**：`.shd` 页头条的右端（左 = 标题 eyebrow / slide 编号，右 = logo）。
- Logo 周围最小留白 = logo 高度（24 px）四周都留。
- 不要拉伸、不要在 `W`/`L` 之外重新着色、不要把 logo 叠在带图案的区域上。

**Mars 商标使用注意**：Mars wordmark 是注册商标。本 DS 限定于内部 + B2B 演示用途；任何对外发布、商业推广或品牌联名须经 Mars Brand 团队授权。Pedigree、Whiskas、M&M's、Snickers、Royal Canin、Orbit 等子品牌的 logo **不在本 DS 范围内** — 演示中提到这些子品牌，用文字（Inter 800）即可，不要内嵌它们的 wordmark。

---

## 5. 幻灯片架构 <!-- ENGINEERING-DNA — the entire section, invariant -->

### 脚手架
```
#wrap — fixed fullscreen, flex-centre, background: var(--ink)
  #deck — 1280 × 720, position:relative, overflow:hidden (hard contract)
    .slide × N — absolute inset, opacity show/hide, overflow:hidden (hard contract)
```

`#wrap` 与 `body` 的 background **必须用 `var(--ink)`**，不能写死 `#000` / `#1A1A1A` / `#1F1F22` — 这些会被 `token_only_colors` hard check 抓到。每个 brand 的 `--ink` 已经是各自真实的深色基调（Mars 的 #3C3C3C 是其官方 dark-grey），letterbox 跟随它就是对的。

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

> **Emphasis for Mars**：Mars 的视觉口吻最贴合 4 种 slide type — **重点强调它们**：
> 1. **Type J — 引言/抽词**（满屏 mars-blue 底 + Inter Black 900 巨字标语，关键词用 mars-green / snack-yellow 染色，对应 Five Principles 页）
> 2. **业务部门多色 tile**（使用 Type B 双栏或 §7.2 Showcase Card 网格，每块用一个业务部门色：petcare-red / food-green / wrigley-gold / snack-yellow — 这是 Mars 唯一允许"多色并列"的语义场景）
> 3. **Type F — 图像页**（大图叠 mars-blue 半透明块 + 白字，对应 About Mars 页那种 "巨大 MARS 字母实景照 + 半透明蓝块覆盖" 的氛围）
> 4. **Type H — 数据图**（柱状/进度条用 mars-blue + mars-green，sustainability KPI 这种叙事）
> Use sparingly: 复杂交互演示 (Type G) — Mars 的 deck 通常是宣讲企业故事，不是演示软件。

### Type A — 封面
- 背景：满屏 `var(--primary)` (mars-blue #0000A0)
- 结构：Logo 右上角（白色变体 `.logo.W`）→ Eyebrow → 巨型标题（Inter Black 900, 82 px, 白色）→ 斜体副标 → Meta 行
- **不允许任何装饰线** — 不要 hairline、不要 accent line、不要渐变边框。背景就是表面。Mars 的封面必须像一张 1970 年代企业年报封面：纯色块 + 大字 wordmark，没有"现代 corporate"的小细节。

### Type B — 双栏内容
对比、特性列表、指标。`grid-template-columns: 1fr 1fr; gap: 20px`。移动端会折叠为单栏。在 Mars 中，双栏特别适合"业务部门并排"叙事 — 左 Petcare 右 Snacking 这类。

### Type C — 全宽叙事
单栏、大字号、配 pull-quote。用于上下文、摘要、推荐建议页。Mars 的 Five Principles 页就是该类型的极致案例：左侧"Five Principles"标题 + 副标，右侧巨大的 5 行单词列表。

### Type D — 翻面卡片
两张卡片并排。正面 = `--primary` (mars-blue)，背面 = mars-green (`--accent`，比纯白柔和但仍鲜亮)。**Hover + 点击翻面** — JS `onclick` 切换 `.on` class（移动端必需）。正面有 ghost 罗马数字。背面留白宽（32 px padding，≤ 4 个内容元素）。

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
一张或多张图占据 slide 主体，文字锚定在安静区域。Mars 站点最招牌的视觉就是这一类（About Mars 页那张三维 MARS 字母实景）。用于展示工厂、产品、Associates、宠物 / 家庭场景照、可持续主题图。

**原则：**
- 图像必须服务于理解 — 不要装饰性 stock photo。优先：Mars 真实产品（M&M's、Snickers、Pedigree 等的产品照）、工厂 / Associates 工作场景、可持续项目实地图。
- 构建 deck 时，**主动 web 搜相关图片**（产品 logo、UI 截图、现实案例）来支撑叙事。
- 图像处理：`border-radius: 0`（Mars 是零圆角品牌，包括图像边缘），可选 `1px solid var(--rule)` 边框。深色背景不需要边框。
- 布局：图像占 slide 区域 50–70%。文字放在旁边或叠在带 mars-blue 半透明块（`rgba(0,0,160,.85)`）的区域上。绝不在繁忙图片上直接放文字而不加 scrim。
- 图下说明：`.cap` 样式（13 px、字重 800、全大写、`--mid`）。
- **Mars 招牌处理**：大图覆盖 + mars-blue 半透明色块（70%~85% 不透明度）+ 白色 Inter 900 标语叠加。这是 mars.com 上最具识别度的图像 + 文字组合。

### Type G — 交互演示
嵌在 slide 内的自包含、点击推进的微体验。目的：让观众 *看到* 概念在工作，而不只是读它。对 Mars 用得少 — 只在演示供应链可视化、可持续 KPI 走势这类才用。

**何时用：** 场景演练、前后对比、多步流程可视化。

**结构：** 一块"屏幕"区域（深色 bg `--primary` 或 `#3C3C3C`，0 px 圆角）+ 点击推进的逐步内容。控件：前后按钮或带编号的步骤。内容通过 CSS transition 出现。

**设计规则：**
- 必须像精致的产品 demo，不是 prototype。整洁字体、克制动效。
- 只用 CSS `@keyframes` — 不用 JS 动效库。每个 demo 的 CSS 不超过 50 行。
- 每一步只承载一个清晰想法。每个 demo 最多 5 步。
- 移动端：滚动时自动推进，或点击目标 ≥ 44 px。

### Type H — 图表/数据洞察
由一个或多个数据可视化主导的 slide。用于定量论证、趋势分析、性能对比 — Mars sustainability KPIs（碳减排、再生能源 %、农户增收）这类核心叙事。图表组件规范（§7.8）定义元素级设计；本类型定义 slide 级原则。

**原则：**
- 每张 slide 一个主图。次要小图可接受 — 但必须直接支撑主图。
- 标题陈述洞察，不是图表类型。好："Mars 在三大可持续维度都跑赢承诺曲线"。坏："柱状图对比"。
- 图表占 slide 区域 50–70%。剩余空间：标题 + 一段解读或一个 callout。
- 入场动效以增强叙事冲击力。
- **Mars 配色规则**：主条 `--primary` (mars-blue) + 次条 `--accent` (mars-green)，不要使用业务部门色作为图表条 — 那会把"语义颜色"和"分类颜色"混淆。

### Type I — 标签页
多个内容视图通过标签切换。当内容有自然分类时，能在一张 slide 上容纳更多信息。Tab 组件规范见 §7.9。

**原则：** 最多 4 个标签。每个 tab panel 都是自包含的"slide-中-slide" — 可以用 §7 任何组件。不要把标签当成 slide 内容塞太满的拐杖；如果 2 个标签各自都显稀疏，就合并成一个视图。

### Type J — 引言/抽词
**Mars 的招牌 slide type。** 一句强烈的话锚定叙事时刻。用于关键 takeaway、受众重置、可记忆的金句。

**结构（标准版）：** 大号引用文字（28–36 px、字重 700、`--ink`）居中或左对齐。可选下方署名（14 px、`--mid`）。左边 accent 边线（`3px solid --accent`）或无。

**结构（Mars 招牌满屏版）：** 整张 slide 满屏 `var(--primary)` (mars-blue)，5–6 行 Inter Black 900 大字垂直排列，关键词用 `--accent` (mars-green) 或 `--snack-yellow` 染色突出。这是 Five Principles 页的精确再现，是 Mars 最具识别度的 deck visual。**做这种 slide 时四条铁律：**

1. **构图必须包在 `.sw + .sc` 里。** 用 `.sw`（覆写 `background: var(--primary); border-left: none`）+ 一个 `.sc` 装大字。**禁止**自创平级 shell class（`.fpwrap`、`.poster-wrap` 之类）—— Mars 端到端测试里 slide 2 的第一版就用了 `.fpwrap`，结果 `fit_contract_intact` 报告 `bad_slides: [{absorbers: 0}]`，因为 `.sc` 之外没有契约可言。
2. **`.sc` 内必须恰好一个 absorber**，带 `flex: 1 1 0; min-height: 0; overflow: hidden` —— 通常是装大字的中间带。顶部 header 带（含 logo + eyebrow）和底部署名带都是 `flex: 0 0 auto`。
3. **按 absorber 高度反推字号上限。** absorber 的 `clientH` ≈ `(720 − 54 header − 32 top − 32 bottom) − 顶部带 − 底部带`。Mars Five Principles 页 5 行排版时，顶部带约 120 px、底部带约 30 px → absorber ≈ 420 px → 每行字号 ≤ `floor((420 − 4×4 gap) / 5) ≈ 80 px`。**第一版用 84 px × 5 行 → 实测 419 px 容器装 459 px 内容，`text_layout_safe` FAIL。** 这就是为什么字号必须从预算反推，不是反过来。当前推荐：`fp-line` 字号 ≤ 72 px、行高 1.05、行间 gap 4 px。
4. **满屏 Type J 不用 `.shd` 页头条。** Logo + slide-eyebrow 直接写在 `.sc` 顶部一行，让画面气势完整。

### Type K — 时间线/路线图
横向或纵向的里程碑序列。用于项目计划、演化叙事、阶段描述（Mars 1911 创立 → 1923 Milky Way → 1968 第一家 Pedigree → 2017 Sustainable in a Generation → ...）。组件规范见 §7.12。

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
- **顶部 accent 线**：`3px solid var(--accent)`（默认）。可按上下文换成 `--primary`、`--green`、`--red`、或某个业务部门色（`--petcare-red`、`--food-green` 等）。是一条细而优雅的线 — 不是填充的 header 块。
- **没有强制 label 条。** 标题在卡片正文里，作为内容的一部分。
- 标题：20 px 字重 900 `--ink`
- 内容：15–16 px 字重 600 `--mid`，慷慨的 12 px+ 间距
- 可选 SVG 图标：32–36 px，inline 放在标题旁或上方。
- **Hover**：微微上浮（`translateY(-2px)`）+ 阴影（这是全 DS 中唯一允许 box-shadow 的位置 — hover 状态的 lift）。

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
.show-card.accent-petcare { border-top-color: var(--petcare-red); }
.show-card.accent-food { border-top-color: var(--food-green); }
.show-card.accent-wrigley { border-top-color: var(--wrigley-gold); }
.show-card.accent-snack { border-top-color: var(--snack-yellow); }
.show-card.compact { padding: 16px 18px; gap: 8px; }
.show-card.compact .show-title { font-size: 18px; }
```

**反模式**：在 6 张以上卡片网格里每张都用填充色 header 条 — 视觉单调。改用细 top accent 线。
**Mars 专用模式**：4 张并排展示业务部门时（Petcare / Snacking / Food / 他），允许每张卡用对应业务部门色作 top accent — 这是语义网格，不是装饰。

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

紧凑指标展示。`stat-num`（36 px 900 `--primary`）+ `stat-label`（12 px 800 全大写 `--mid`）。Mars 这类常用：100+ 国家、80,000 Associates、$50B+ 年营收、Sustainable in a Generation 计划进度等。

### 7.5 Callout / Note

**轻量**（内嵌备注）：
```css
.snote { border-left: 3px solid var(--primary); padding: 10px 18px; background: var(--tint); font-size: 14px; font-weight: 700; }
```

**深色**（结论 / 建议条）：
用于 slide 末尾 takeaway 的全宽 mars-blue 块。文字：13–16 px 700–800，`rgba(255,255,255,.85)`。关键词加粗用 `color: #fff`。不要 border-left — 实心 mars-blue 填充本身就是强调。

### 7.6 Marks, Badges & Chips

**状态标记**：
```css
.mark::before { display: inline-block; width: 18px; height: 18px; border-radius: 50%; text-align: center; line-height: 18px; font-size: 11px; font-weight: 900; margin-right: 8px; }
.mark.yes::before { content: '✓'; background: var(--green); color: #fff; }
.mark.no::before  { content: '−'; background: var(--red); color: #fff; }
```

> **例外说明**：上面的 `.mark::before` 圆形指示符是全 DS 中唯一允许 `border-radius: 50%` 的元素 — 因为它是一个图标语义符号，不是容器。所有矩形容器仍然 0 圆角。

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
- mars-blue 表头行是唯一的色块。所有数据单元格：白底、`--ink` 文字。
- **`<table>` 单元格里不要彩色徽章** — 用字重 / 颜色强调。
- 可选一行 `--tint` 高亮，仅给最重要的那一行。
- "整洁网格"测试：眯眼看表格。看到一堆彩色方块拼贴，就是设计失败了。

### 7.8 Charts

| Type | Primary colour | Secondary | Neutral | Notes |
|---|---|---|---|---|
| Bar (H / V) | `--accent` (mars-green) | `--primary` (mars-blue) | `--rule` | Animated grow on entrance |
| Progress / gauge | `--accent` fill | — | `--rule` track | 8px height, 0px radius (Mars 是零圆角；进度条直角矩形) |
| Pie / donut | `--primary` | `--accent` | `--rule` | Max 3 segments |
| Timeline | `--primary` dots | — | `--rule` dots | Key nodes: `--tint` ring |

每张图最多 2 种颜色（+ `--rule` 中性色）。入场动效：bar 增长、计数器累加。

### 7.9 Tabs

```css
.tabs { display: flex; gap: 6px; margin-bottom: 14px; }
.tb { padding: 7px 16px; border: 1px solid var(--rule); background: transparent; font: 800 12px/1 'Inter'; letter-spacing: .06em; color: var(--mid); cursor: pointer; }
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

横向里程碑序列，配连接线。Mars 的应用：1911 创立 → 1923 Milky Way → 1968 Pedigree → 1986 五项原则首次成文 → 2017 Sustainable in a Generation → 当前。

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

> **例外说明**：`.tl-dot2` 是图标语义元素（圆点），允许 `border-radius: 50%`。其他容器仍然 0 圆角。

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
| 业务部门并列 | Showcase Card 多色 accent variant | 2×2 或 4 栏 |

---

## 8. 图像与视觉佐证 <!-- BRAND-VARIABLE intro; rules are ENGINEERING-DNA -->

### 原则

Mars 是一个产品 + 工厂 + 农场 + Associates + 宠物 + 家庭场景都极其具体的品牌。它的图像永远应该是 *真实可见的实体世界* —— 巧克力、宠物、收割可可豆的农场、装配线、Associates 的工作场景 —— 不是抽象渐变 / 线条插画 / 通用 stock。一张 slide 上的图像必须能回答："这是 Mars 在 [国家/工厂/项目] 真实拍到的什么？" 不能就跳过它。

### 何时加入图像

- **产品 UI 截图**：当讨论某具体工具时，展示它的真实界面（例如：MyMars 平台、Pet Insight 仪表板、可持续性追踪 app）。
- **数据可视化**：当某个数字或趋势是核心时，建一张图（Type H）。
- **环境照片**：当某场景需要视觉锚点时，搜并放一张相关图（巧克力工厂、可可农、宠物医院、M&M's 商店）。
- **图示**：当某概念具有结构（层级、流程、对比）时，用 CSS/SVG 画出来，而不是用文字描述。

### 如何获取图像

1. **主动搜索**：用 web search 找相关产品截图、图示、环境照片。优先选官方素材（mars.com newsroom、Mars Sustainability Report PDF、子品牌官网）。
2. **CSS 绘制替代品**：柱状图、进度条、时间线图 — 数据简单时优于外部图片。
3. **绝不用**：装饰性 stock photo、抽象渐变、AI 生成的占位艺术、与 slide 主旨无关的图片。

### 图像处理

- `border-radius: 0px`（Mars 是零圆角品牌，包括图像边缘）。浅色背景上可选 `1px solid var(--rule)` 边框。
- 深色背景上的图：不要边框。
- 说明文字：图下方使用 `.cap` 样式。
- 绝不在繁忙图像上直接放文字而不加 scrim — Mars 招牌 scrim 是 `rgba(0,0,160,.85)`（85% 不透明 mars-blue），而不是黑色蒙层。这样 scrim 本身也是品牌色。

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
2. **具体优于抽象**：具体场景胜过泛泛描述（"全球 80,000 名 Associates" 优于 "全球员工"）。
3. **视觉证据**：图表 > 文字、截图 > 描述、图示 > bullet 列表。
4. **截图测试**：如果没人愿意把这张 slide 截图保存，它就缺一个视觉钩子。

---

## 12. 布局规则 <!-- ENGINEERING-DNA -->

### Overflow 预防

每张 slide 装进 720 px。太密：减小间距 → 正文降到 14 px → 拆 slide。绝不剪裁或滚动。

**"蓝块"陷阱**：右下角的深色 callout = 视觉失衡。改成全宽底部、用 `.snote` 替代、或把深色卡放在顶部。

**"蓝叠 navy"陷阱**：在深色 slide（`--primary` bg）上，永远不要用 `--accent` 当文字或 accent — 会产生刺眼、廉价感的对比。用白色（`#fff`）或半透明白（`rgba(255,255,255,.85)`）做强调。深色背景上的低调 CTA：`rgba(255,255,255,.08)` bg 填充 + 白字。
**Mars 例外**：Type J 满屏 mars-blue 标语 slide 中，`--accent` (mars-green) 和 `--snack-yellow` 作为关键词染色是 *允许且鼓励的*。区别在于：那是单词级别的高对比 *诗意排版*，不是组件级别的 chrome —— 整个 Five Principles 页就是这种处理。识别要点：如果 mars-green 是覆盖几个字而不是覆盖整个按钮 / 卡片，OK。

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
| 圆角 | 0 px (Mars 是零圆角品牌) |
| 分隔线粗细 | 1 px |
| Accent 边线 | 3 px |

---

## 13. 上线前检查清单 <!-- ENGINEERING-DNA: pre-ship-checklist -->

分享 deck 之前，逐项核对。

### 品牌与 Token
- [ ] 每张 slide 都有 logo（封面右上、内容页 `.shd` 右端）
- [ ] **Logo 在封面肉眼可见** —— 打开 deck 看 slide 1 右上角。"内嵌成功但不可见"是 Mars 端到端测试里第一版踩到的真实坑（见 §4 fill 级联陷阱）。`has_real_vector_path: true` 单独不能保证视觉上看得见。
- [ ] Logo `<symbol>` 块内部不含任何 `fill` 属性（含 `<g fill="none">` wrapper）—— 只允许 `fill="currentColor"`
- [ ] **每张 slide 内容都包在 `.sc` 容器内** —— 包括 bespoke 满屏 Type J / Type A。不能用平级 shell 如 `.fpwrap` / `.poster-wrap`（Mars 测试里这种自定义 shell **静默绕过** `fit_contract_intact`）
- [ ] 颜色：只用系统 token — 不用临时 hex
- [ ] 所有 bespoke 元素都仅基于系统 token 构造（见 §1 约束 vs 自由）
- [ ] 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 可用
- [ ] Inter 字重 400/500/600/700/800/900 已加载；不用 serif / display 字体
- [ ] 封面副标：仅用 Inter 300 斜体（如果 300 italic 不可用，用 400 italic 替代）
- [ ] 所有矩形容器 `border-radius: 0`（Mars 是零圆角品牌）
- [ ] 所有容器 `box-shadow: none`（hover lift 是唯一例外）

### 字体与可读性
- [ ] 没有低于 12 px 的文字 — 特别注意徽章 / 标签列
- [ ] Slide 标题 ≥ 50 px（仅在密集多行例外时降到 38 px）
- [ ] 非表格 slide 的正文 ≥ 16 px（仅在数据密集表格上用 14 px）
- [ ] 副标 ≥ 20 px
- [ ] 中文与对应英文字号 / 字重一致（混排时）
- [ ] CJK 字体回退链：PingFang SC / Hiragino Sans GB / Microsoft YaHei / Source Han Sans 至少一个出现在 font-family 链里
- [ ] PingFang SC 字重已提升至 500/600（Regular 在 mars-blue 大色块上会显瘦）

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
- [ ] 图上文字有 scrim（≥ 50% 不透明度，且为 mars-blue 而非黑色）
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
