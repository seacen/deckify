# Coca-Cola-PPT-Design-System

> 为 Coca-Cola 制作的所有 deck 共用的视觉语言。请严格遵循，让每一份新 deck 都一眼被识别为同一家族。

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

****编辑性的红色宣言。** 每张 slide 都是 Coca-Cola Red (#EA0000) 上的一句话 — 白字 Spencerian wordmark 锚定品牌，editorial-register 的标题承担信息。0-radius 的锐利矩形、慷慨的留白、Georgia serif headline 配 Helvetica Neue 正文。色彩节制：红是唯一的饱和色，黑 / 白 / 灰承担其余。**

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
- Georgia typeface, no serif/display fonts - Georgia + Helvetica Neue — 不引入第三种字体
- 标题、pullquote、品牌时刻用 Georgia
- 正文、UI、表格用 Helvetica Neue
- 绝不使用 condensed / 装饰 / script 字体
- 12 px 可读性下限
- 每一张 slide 都必须有 logo
- 不用 emoji (👍🎉 等) — 排版符号 (✓ − ! ×) 和几何指示符允许
- 不用装饰性 stock photography
- `.shd` header strip on content slides
- `.sw` border-left accent

**可复用组件（按需选用，不强制）：**
- §7 组件库提供卡片、表格、图表、标签、标记 — 适合时用，不适合时跳过用 bespoke 布局。

**Bespoke 元素（鼓励）：**
- **在调色板内自由发挥。** 封面用 Red bg + 白 wordmark + Georgia 80 px 大字标题，副标 Helvetica Neue 22 px。内容页白底黑字，Georgia 50 px 标题，正文 Helvetica Neue 17 px，红色仅出现在 CTA 链接、chart 主条、或 pullquote 的边线 — 一张 slide 一处足矣。绝不出现 4 种以上颜色同时存在的画面。
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
  --primary:  #EA0000;   /* Dominant brand chord — cover bg, primary mark colour */
  --accent:   #EA0000;   /* CTA / link / single saturated highlight */
  /* ── Neutrals ── */
  --surface:  #EEEEEE;   /* Paper / slide bg */
  --white:    #FFFFFF;
  --ink:      #000000;   /* Body text on light surfaces */
  --mid:      #4F4F4F;   /* Secondary text / muted labels */
  --rule:     #BDBDBD;   /* Dividers / hairlines */
  --tint:     #F8F8F8;   /* Subtle row / section bg */
  /* ── Semantic (invariant names; values may map to brand-palette colours) ── */
  --green:    #0E9F6E;   /* Positive */
  --green-bg: #D1FAE5;
  --red:      #BF1004;   /* Negative */
  --red-bg:   #FFE9E2;
  --warn:     #F59E0B;   /* Warning / caution */
  --warn-bg:  #FEF3C7;
  --teal:     #1F96DB;   /* Informational / neutral highlight */
  --teal-bg:  #D6EBFF;
  /* ── Brand palette (brand-specific names; expanded from brand.json accents+neutrals) ── */
  --red-deep:    #BF1004;   /* Deeper red — input critical / shadow-mode of brand red */
  --red-pale:    #FFE9E2;   /* Pale red wash — soft callout / row tint */
  --coral:       #FFA68F;   /* Warm coral — soft CTA / hover transition */
  --paper-pure:  #FFFFFF;   /* Pure white — on-black surface, inverse paper */
  --graphite:    #4F4F4F;   /* Mid-tone grey — secondary text / disabled */
  --stone:       #BDBDBD;   /* Light grey — divider / on-brand-disabled */
  --coal:        #353535;   /* Near-black — hover on dark surfaces */
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

**Georgia** — 唯一字体。字重 400, 700（Georgia）+ 300, 400, 600, 700（Helvetica Neue）；允许斜体 — Georgia italic 是 editorial register 的标志。`'Helvetica Neue', system-ui, -apple-system, sans-serif` 作为 正文与 UI 字体（编辑性 serif headline + 经典 grotesque 正文 — 1960 年代杂志广告搭配）。

> Coca-Cola 1886 年品牌史适配 editorial serif headline。Georgia 56–82 px 标题（serif，可斜体），Helvetica Neue 16–17 px 正文。绝不用 condensed、装饰、script 字体（spencerian script 已在 logo 里）。TCCC-UnityText 不可分发，回退到 Georgia。

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

## 4. Coca-Cola Logo <!-- BRAND-VARIABLE: SVG payload is brand-specific; surrounding pattern + multi-format support is ENGINEERING-DNA -->

### 定义（每份 HTML 一次）

Logo 必须是真实的品牌身份资产，**完整内嵌**到 HTML 中（不依赖外部网络）。允许两种内嵌路径；`embed_logo.py` 自动选择：

**A. SVG 矢量路径**（首选） — 当能从品牌站点、Wikipedia 或品牌素材页拿到 SVG 源时使用：

```html
<svg style="display:none" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 125 20" fill="currentColor">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M72.5852 4.29205L72.5813 4.29009C73.0478 3.78076 73.5646 3.23983 74.1055 2.71938C73.4473 2.39854 72.8394 2.03485 72.2513 1.68303C70.977 0.920686 69.7957 0.214018 68.3976 0.119447C67.3132 0.0523276 66.2276 0.231767 65.2224 0.644291C65.2224 0.644291 64.6789 -0.0934786 63.0054 0.145596C61.3318 0.384671 56.1768 2.53821 51.7838 9.56103C47.8129 15.9096 49.6788 19.5499 52.5309 19.5106C55.6221 19.4677 58.5619 16.031 59.5593 13.1976C60.5567 10.3642 59.38 9.59652 58.476 9.66936C57.4768 9.75341 55.7117 10.6425 54.7405 12.6074C53.7692 14.5723 53.7692 15.7826 53.7692 15.7826C54.1662 15.3661 54.5979 14.9843 55.0599 14.6414C55.4756 14.3167 55.9337 14.0503 56.4215 13.8494C56.5356 13.3417 56.7054 12.8482 56.9276 12.3776C57.2788 11.6455 57.8354 10.8834 58.5227 10.7116C59.9179 10.3623 59.2493 12.9062 58.2239 14.5648C57.6729 15.4501 55.7173 18.0108 54.0382 18.0108C52.3591 18.0108 52.0378 16.3933 52.3908 14.8748C52.7438 13.3563 53.235 11.4363 55.6893 7.9398C58.1436 4.44334 60.7976 2.37011 62.3348 1.5016C63.9131 0.606936 64.5556 0.999167 64.5556 0.999167C64.5556 0.999167 62.5403 2.23563 61.3935 3.72985C60.299 5.15683 59.6434 6.76124 60.1514 7.54757C60.637 8.29655 62.3423 8.31149 64.2231 5.59949C66.0797 2.9211 65.6128 1.3279 65.6128 1.3279C65.735 1.28816 65.8598 1.25695 65.9863 1.23451C66.8922 1.1131 67.6169 1.35404 68.7375 1.92932C69.2841 2.20997 69.8205 2.56943 70.3934 2.95338C71.0511 3.39406 71.757 3.8671 72.5813 4.29009L72.5796 4.29205H72.5852ZM64.9777 1.53522C64.9777 1.53522 63.7823 2.0115 62.3927 3.54307C61.0031 5.07464 60.1925 6.7986 60.792 7.25433C61.0218 7.42803 61.5522 7.45792 62.516 6.59127C63.4046 5.81947 64.1021 4.85216 64.5537 3.76534C65.1402 2.33537 64.9977 1.63432 64.9795 1.54479C64.9784 1.53936 64.9777 1.53618 64.9777 1.53522Z"/>
<path d="M75.0066 5.15959L75.0058 5.16056C78.2706 5.80681 81.1302 3.78401 82.6506 2.06193C83.2054 1.44566 83.6827 0.763843 84.0719 0.031662C83.3795 0.752537 82.6046 1.38946 81.7634 1.92932L81.754 1.92745C80.3383 2.83519 78.379 3.65887 76.4963 3.4777C76.02 3.97079 75.5101 4.54046 75.0021 5.15869L75.0066 5.15959Z"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M76.1563 16.7632C75.8855 17.1965 75.5773 18.0276 76.472 17.5103C77.5609 16.8808 79.113 14.5218 79.113 14.5218H79.8153C79.1753 15.5077 78.4623 16.4442 77.6823 17.3235C76.5785 18.5469 75.2318 19.6582 74.283 19.548C73.1754 19.4191 73.5228 17.9641 73.5228 17.9641C73.5228 17.9641 71.9314 19.6451 70.8388 19.5312C69.3576 19.3668 69.8096 17.5364 69.8096 17.5364C69.8096 17.5364 68.1286 19.591 66.993 19.5293C65.2037 19.4266 65.6539 17.2432 66.1507 15.7153C66.4178 14.8954 66.6643 14.251 66.6643 14.251C66.6643 14.251 66.4869 14.2977 66.104 14.3537C65.9041 14.3817 65.5437 14.4023 65.5437 14.4023C65.133 15.1265 64.6854 15.829 64.2026 16.5073C63.6068 17.2992 61.076 20.0205 59.5817 19.4752C58.2033 18.9709 58.659 16.8603 59.4622 15.1793C60.6333 12.7344 63.928 9.2211 65.8276 9.68243C67.7981 10.1606 65.8724 13.7542 65.8724 13.7542C65.8724 13.7542 65.8724 13.7672 65.8929 13.7766C66.0173 13.799 66.1453 13.792 66.2665 13.756C66.5128 13.7062 66.754 13.6343 66.9874 13.5412C66.9874 13.5412 68.9673 9.3948 71.1544 6.68279C73.3416 3.97079 77.7103 -0.694901 79.4231 0.435101C79.8414 0.713398 79.6509 1.6697 79.0869 2.83145C78.8327 2.91184 78.5746 2.97917 78.3136 3.03317C78.6264 2.51439 78.8629 1.95329 79.0159 1.36712C79.2736 -0.0337099 76.0013 2.91924 73.6629 6.09818C72.2565 8.01326 71.0072 10.0389 69.9273 12.1554C70.3498 11.8986 70.7531 11.6114 71.1339 11.2962C72.1771 10.4311 73.1687 9.50555 74.1037 8.52442C75.0007 7.60023 75.8421 6.62353 76.6233 5.59949C76.8735 5.58772 77.1229 5.56216 77.3704 5.52291C76.5155 6.68225 75.5839 7.78297 74.5818 8.81766C74.4992 8.90021 74.4161 8.98347 74.3325 9.06717C73.4706 9.93029 72.5617 10.8405 71.7615 11.5147C70.9802 12.183 70.156 12.7995 69.2941 13.3601C69.2941 13.3601 67.2396 17.4841 68.3603 17.7493C69.014 17.9062 70.3065 15.9171 70.3065 15.9171C70.3065 15.9171 71.9875 13.3451 73.0073 12.1815C74.3857 10.6126 75.5792 9.70858 76.7652 9.6843C77.46 9.67123 77.8691 10.4127 77.8691 10.4127L78.1959 9.90657H80.2075C80.2075 9.90657 76.4514 16.2794 76.1507 16.7594L76.1563 16.7632ZM77.4171 11.1262C77.4416 11.0829 77.4616 11.0372 77.4768 10.9899C77.4673 10.9152 77.4324 10.8461 77.378 10.7941C77.3236 10.7421 77.253 10.7103 77.178 10.7041C76.868 10.6892 76.4421 10.7489 75.3308 11.9798C74.4073 12.999 73.6131 14.1282 72.9662 15.3418C72.3293 16.5054 72.0715 17.372 72.4376 17.5962C72.5563 17.6572 72.6937 17.6712 72.8224 17.6354C73.0708 17.5756 73.3509 17.344 73.7787 16.8491C73.9387 16.6636 74.1131 16.4158 74.3125 16.1326L74.3144 16.1299C74.3634 16.0604 74.4139 15.9886 74.466 15.9152C75.2019 14.9141 77.051 11.7613 77.4171 11.1244V11.1262ZM65.863 12.4635C66.0498 11.9779 66.2852 11.0254 65.7939 10.6518C65.2654 10.254 63.9262 11.186 63.9131 12.146C63.9 13.1061 64.8601 13.5674 65.0898 13.629C65.2205 13.6645 65.2654 13.6589 65.3289 13.5543C65.532 13.2048 65.7105 12.8416 65.863 12.4673V12.4635ZM64.8451 14.2473C64.5117 14.0931 64.2007 13.8946 63.9206 13.6571C63.6385 13.4215 63.4023 13.1359 63.2239 12.8147C63.2084 12.7884 63.193 12.8056 63.1765 12.8239C63.173 12.8278 63.1695 12.8317 63.166 12.8352L63.1656 12.8356C63.1445 12.8567 63.0612 12.94 62.3442 13.9895C61.6232 15.0448 60.525 17.2189 61.5223 17.5906C62.1611 17.8278 63.2239 16.709 63.8066 15.9675C64.2011 15.4503 64.5587 14.9061 64.8769 14.3388C64.9068 14.2753 64.8769 14.2603 64.8451 14.2473Z"/>
<path d="M53.5208 5.05597H51.6082L50.5268 6.8042H52.4394L53.5208 5.05597Z"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M49.0307 9.83933H49.7255C49.7255 9.83933 46.2141 14.9141 44.2287 14.6825C43.1211 14.5536 43.4498 13.1882 43.4498 13.1882C43.4498 13.1882 41.8902 15.0093 40.4614 14.6451C39.1651 14.3126 40.0019 12.1591 40.0019 12.1591C39.9798 12.168 39.8983 12.2463 39.7691 12.3705C39.0344 13.0765 36.7561 15.2657 35.0803 14.6208C33.0258 13.8252 34.0885 11.1785 34.4808 10.3828C34.8132 9.71232 35.1812 9.0586 35.1812 9.0586C35.1812 9.0586 34.8655 9.14825 34.6675 9.19308C34.4696 9.2379 34.1726 9.29581 34.1726 9.29581C34.1726 9.29581 33.1976 10.8815 32.6018 11.6716C32.006 12.4617 29.4714 15.1812 27.979 14.6395C26.4867 14.0978 26.8584 12.0097 27.6951 10.3436C29.0549 7.65404 32.2824 4.34808 34.2323 4.84491C36.1823 5.34173 34.5704 8.53002 34.5704 8.53002C34.5704 8.53002 34.9608 8.58045 35.8965 7.94167C36.283 7.67868 36.7043 7.28842 37.1539 6.87205C38.2751 5.83354 39.5716 4.63265 40.9395 4.8393C41.8435 4.97565 42.6859 5.90393 41.5335 7.66524C41.1599 8.22557 40.5454 8.73734 40.071 8.23678C39.7759 7.9286 40.0336 7.35893 40.3437 6.97043C40.4649 6.81211 40.6232 6.68604 40.8046 6.60331C40.986 6.52058 41.185 6.48373 41.384 6.49602C41.384 6.49602 41.7016 5.76572 40.8928 5.78066C40.2372 5.79373 38.5786 7.3197 37.6429 8.86248C36.7949 10.2839 35.4968 12.697 36.7949 13.2237C37.9922 13.7075 40.2708 11.0029 41.3261 9.58531C42.3814 8.16767 44.7834 4.95511 46.8006 4.82623C47.4954 4.7814 47.9082 5.41458 47.9082 5.41458L48.1416 5.04102H50.1551C50.1551 5.04102 46.3635 11.3896 46.0665 11.8659C45.8331 12.2394 45.523 13.0855 46.3822 12.613C47.2414 12.1404 49.0307 9.83933 49.0307 9.83933ZM44.464 11.1038C45.2783 9.98315 47.5234 6.0795 47.5234 6.0795C47.5138 6.00486 47.4789 5.93576 47.4245 5.88375C47.3701 5.83174 47.2996 5.79996 47.2246 5.79374C46.9145 5.77879 46.399 5.88339 45.3568 7.17215C44.3146 8.46091 43.5376 9.48632 42.9586 10.5528C42.3198 11.7164 42.0415 12.5383 42.4076 12.7605C42.5266 12.8207 42.6636 12.8346 42.7923 12.7997C43.0314 12.74 43.3433 12.5009 43.7711 12.0078C43.9728 11.7781 44.2006 11.468 44.4677 11.1038H44.464ZM34.2043 5.81802C33.6757 5.41831 32.3366 6.3522 32.3235 7.31223C32.3104 8.27227 33.5375 8.57111 33.6963 8.57858C33.7317 8.58792 33.7692 8.58528 33.803 8.5711C33.8368 8.55691 33.8649 8.53197 33.8831 8.50014C34.0267 8.21872 34.1558 7.93008 34.2697 7.63536C34.4565 7.14974 34.6899 6.19717 34.1987 5.82362L34.2043 5.81802ZM33.4012 9.18561C33.0368 9.07164 32.6884 8.91159 32.3646 8.70933C32.0487 8.50534 31.7913 8.22279 31.6175 7.88937C31.6012 7.8617 31.5835 7.88226 31.5668 7.90161C31.5644 7.90446 31.562 7.90728 31.5596 7.90992C31.5409 7.93047 31.4326 8.07242 30.7135 9.12771C29.9944 10.183 28.9279 12.3421 29.9271 12.712C30.5659 12.9492 31.6399 11.8266 32.2208 11.0851C32.6585 10.5064 33.0632 9.90335 33.4329 9.279C33.4572 9.21549 33.4329 9.20055 33.3974 9.18934L33.4012 9.18561Z"/>
<path d="M47.9324 20C46.447 18.972 44.6685 18.4529 42.8633 18.5207C42.3747 18.5339 41.896 18.6622 41.4663 18.8953C41.0366 19.1283 40.668 19.4594 40.3904 19.8618C39.6209 18.5189 38.1005 17.6952 35.749 17.7138C33.758 17.7364 31.7748 18.2283 29.9086 18.6911C28.2139 19.1114 26.6157 19.5078 25.1961 19.5069C22.3309 19.5069 20.2446 17.7064 20.3137 14.5106C20.437 8.90731 25.1699 3.86433 28.7187 1.58938C30.7527 0.281943 32.4542 -0.102817 33.5749 0.0223232C34.3874 0.111976 35.3642 1.05147 34.7478 2.43548C33.842 4.46202 32.5906 4.29205 32.6373 3.32454C32.6567 3.07215 32.7358 2.82797 32.8679 2.61206C33.0001 2.39614 33.1816 2.21465 33.3974 2.08247C33.6266 1.95775 33.8837 1.89347 34.1446 1.8957C34.3313 1.74441 34.4602 0.63682 33.0033 1.00104C31.5465 1.36525 29.7721 2.79783 28.0986 4.64692C26.4251 6.49602 23.8214 9.98875 23.177 13.6571C22.8763 15.3586 23.0761 18.461 27.0993 18.4273C28.6505 18.4146 30.5377 17.944 32.5699 17.4373C35.0134 16.8281 37.6663 16.1666 40.1961 16.186C41.8098 16.1792 43.3946 16.6132 44.7796 17.4412C45.9788 18.1883 47.4151 19.2566 47.925 19.9925L47.9324 20Z"/>
<path d="M11.2776 12.7344H15.3157L15.1831 11.8154H12.3273V10.6948H14.2511V9.76088H12.3273V8.80831H15.1289L15.2634 7.88937H11.2795L11.2776 12.7344Z"/>
<path d="M5.30073 12.7344H6.35042V10.592H8.82335V12.7325H9.87677V7.90431H8.82522V9.65441H6.35042V7.90244H5.30634L5.30073 12.7344Z"/>
<path d="M0 8.84567H1.61002V12.7288H2.66344V8.84567H4.27346V7.90058H0V8.84567Z"/>
<path d="M123.234 7.91552H124.394L122.483 11.1206V12.7437H121.43V11.1412L119.5 7.91365H120.686L121.966 10.1737L123.234 7.91552Z"/>
<path d="M117.647 11.1841V7.91552L118.673 7.90991V12.7381H117.614L115.27 9.4116V12.7381H114.244V7.90991H115.335L117.647 11.1841Z"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M113.322 12.74H112.214L111.812 11.6623H109.692L109.291 12.7344H108.191L110.113 7.90805H111.407L113.322 12.74ZM110.759 8.84006L110.036 10.7545L111.476 10.7527L110.759 8.84006Z"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M104.001 7.90618H106.484C106.806 7.89576 107.127 7.9637 107.418 8.10416C107.66 8.22403 107.86 8.41408 107.993 8.64955C108.121 8.89159 108.188 9.1612 108.188 9.43495C108.188 9.7087 108.121 9.97831 107.993 10.2203C107.859 10.4561 107.659 10.6471 107.418 10.7695C107.127 10.9106 106.807 10.9792 106.484 10.9693H105.055V12.7325H104.001V7.90618ZM105.062 10.0373H106.465C106.642 10.0488 106.816 9.99201 106.952 9.87854C107.065 9.75818 107.127 9.59963 107.127 9.43495C107.127 9.27027 107.065 9.11172 106.952 8.99135C106.814 8.88092 106.64 8.82568 106.463 8.83633H105.062V10.0373Z"/>
<path d="M101.187 7.90618H102.601L102.602 12.7362H101.583V9.18747L100.1 12.6615H99.3955L97.9293 9.27526V12.7288H96.9095V7.90618H98.3234L99.769 11.2682L101.187 7.90618Z"/>
<path d="M93.1822 11.8603C93.1825 11.8603 93.1829 11.8603 93.1833 11.8602H93.1814C93.1816 11.8603 93.1819 11.8603 93.1822 11.8603Z"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M94.5131 12.4953C94.103 12.7114 93.6449 12.8206 93.1814 12.8128L93.1758 12.8147C92.7123 12.822 92.2544 12.7128 91.8441 12.4972C91.4612 12.2925 91.1435 11.9844 90.927 11.6081C90.7089 11.2115 90.5945 10.7663 90.5945 10.3137C90.5945 9.86116 90.7089 9.41592 90.927 9.01937C91.1442 8.64297 91.4626 8.33497 91.8459 8.13031C92.2586 7.92095 92.7149 7.81184 93.1777 7.81184C93.6404 7.81184 94.0967 7.92095 94.5094 8.13031C94.8983 8.33271 95.222 8.64091 95.4433 9.01937C95.6607 9.4158 95.7747 9.86065 95.7747 10.3128C95.7747 10.7649 95.6607 11.2098 95.4433 11.6062C95.223 11.9842 94.9006 12.2923 94.5131 12.4953ZM92.4156 11.6623C92.6487 11.796 92.9135 11.8644 93.1822 11.8603C93.4512 11.8662 93.7165 11.7976 93.949 11.6623C94.1731 11.533 94.3563 11.3434 94.4776 11.115C94.6029 10.8665 94.6682 10.5921 94.6682 10.3137C94.6682 10.0354 94.6029 9.76098 94.4776 9.51246C94.3574 9.28227 94.174 9.09113 93.949 8.96147C93.7145 8.8323 93.451 8.76457 93.1833 8.76457C92.9155 8.76457 92.652 8.8323 92.4175 8.96147C92.1933 9.0876 92.0089 9.27393 91.8852 9.49939C91.7554 9.74612 91.6911 10.022 91.6984 10.3007C91.6922 10.5792 91.7564 10.8548 91.8852 11.1019C92.0058 11.3349 92.1896 11.5291 92.4156 11.6623Z"/>
<path d="M89.2105 12.6279C88.8567 12.7556 88.4828 12.8188 88.1067 12.8147L88.1123 12.8203C87.6243 12.8289 87.1417 12.7166 86.7077 12.4934C86.3078 12.2878 85.9723 11.9759 85.738 11.592C85.5038 11.2082 85.3798 10.7672 85.3798 10.3175C85.3798 9.86777 85.5038 9.42678 85.738 9.04291C85.9723 8.65905 86.3078 8.34716 86.7077 8.14152C87.1365 7.92063 87.6132 7.809 88.0955 7.81653C88.4718 7.8098 88.8461 7.87313 89.1993 8.0033C89.5189 8.12009 89.8036 8.3161 90.0267 8.57297L89.3711 9.3014C89.2041 9.1268 89.005 8.98602 88.7847 8.88676C88.5753 8.79899 88.3504 8.75451 88.1235 8.75602C87.8322 8.75215 87.5448 8.82288 87.2886 8.96147C87.0462 9.09207 86.8436 9.28565 86.7021 9.5218C86.5542 9.75996 86.4771 10.0353 86.4798 10.3156C86.476 10.5919 86.5488 10.8639 86.6903 11.1013C86.8317 11.3387 87.0362 11.5323 87.2811 11.6604C87.5416 11.8001 87.8335 11.8709 88.1291 11.8659C88.3652 11.8698 88.5996 11.8249 88.8175 11.7339C89.0354 11.643 89.2322 11.5079 89.3954 11.3373L90.0529 12.0545C89.826 12.3148 89.5359 12.5122 89.2105 12.6279Z"/>  <!-- inner <path>/<g> carry no explicit fill, so currentColor cascades in -->
  </symbol>
</svg>
```

**B. PNG/JPG/WebP base64 内嵌**（位图 fallback） — 仅有位图 logo 时（最小 64×64），base64 编码后通过 `<image href>` 包进同一个 `<symbol>`：

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 125 20">
    <image href="data:image/png;base64,{{LOGO_BASE64}}" width="125" height="20"/>
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
<svg class="logo W" viewBox="0 0 125 20" aria-label="Coca-Cola">
  <use href="#brand-wm"/>
</svg>

<!-- 品牌深色（浅色 slide 上） -->
<svg class="logo L" viewBox="0 0 125 20" aria-label="Coca-Cola">
  <use href="#brand-wm"/>
</svg>
```

```css
/* fill: currentColor 必须放在 .logo 上 — 不要放在 .logo path 上。
   CSS 选择器无法穿透 SVG <use> 的 shadow DOM。
   外层 <svg> 上的继承 fill 才能正确级联进去。 */
.logo   { height: 34px; width: auto; flex-shrink: 0; fill: currentColor; }
.logo.W { color: #fff; }
.logo.L { color: var(--primary); }
```

### 摆放规则 <!-- ENGINEERING-DNA -->
- **每张 slide** 都必须有 logo — 封面与所有内容页。
- **封面**：`.cov-top` flex 行的右上角。
- **内容页**：`.shd` 页头条的右端（左 = 标题 eyebrow / slide 编号，右 = logo）。
- Logo 周围最小留白 = logo 高度（34px）四周都留。
- 不要拉伸、不要在 `W`/`L` 之外重新着色、不要把 logo 叠在带图案的区域上。

> Coca-Cola Spencerian wordmark 是品牌的全部 — 不可与其他元素组合、不变形、不重新着色到红 / 白以外。深色 / 红色模式 fill: var(--white)；白色模式 fill: var(--primary)。Spencerian script 不可被替代字体替换。

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

> **Emphasis for Coca-Cola**: **Coca-Cola 强调**：Coca-Cola 是 brand-as-feeling 公司 — 每张 slide 都该让观众离场后只记住一句话和一个画面。空白比内容更重要。Wordmark 是锚点，不是装饰。
> Foreground these types when designing decks: Type J（pull-quote — Coca-Cola 1886 品牌声音的最佳载体）、Type C（全宽叙事 — manifesto 散文）、Type F（图像页 — 产品 / 人物 hero）、Type H（图表 — 公司业绩或品牌指标）.
> Use sparingly: Type D（flip cards — Coca-Cola 不爱用花哨交互）、Type I（标签页）.

### Type A — 封面
- 背景：`Coca-Cola Red `#EA0000` — manifesto / 品牌时刻；White `#FFFFFF` — 数据 / 对比 / 编辑内容时刻`
- 结构：Logo 右上角 → Eyebrow → 巨型标题 → 斜体副标 → Meta 行
- **不允许任何装饰线** — 不要 hairline、不要 accent line、不要渐变边框。背景就是表面。

### Type B — 双栏内容
对比、特性列表、指标。`grid-template-columns: 1fr 1fr; gap: 20px`。移动端会折叠为单栏。

### Type C — 全宽叙事
单栏、大字号、配 pull-quote。用于上下文、摘要、推荐建议页。

### Type D — 翻面卡片
两张卡片并排。正面 = `--primary`，背面 = `var(--primary)`（比 `--accent` 柔和）。**Hover + 点击翻面** — JS `onclick` 切换 `.on` class（移动端必需）。正面有 ghost 罗马数字。背面留白宽（32 px padding，≤ 4 个内容元素）。

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
- 标题陈述洞察，不是图表类型。好："Coca-Cola 在三项维度都领先"。坏："柱状图对比"。
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
.tb { padding: 7px 16px; border: 1px solid var(--rule); background: transparent; font: 800 12px/1 'Georgia'; letter-spacing: .06em; color: var(--mid); cursor: pointer; }
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

Coca-Cola 的图像是 1）产品照片（罐 / 瓶 / 杯）2）人物的真实瞬间——分享 / 庆祝 / 群聚的镜头。绝不用 stock photo。每张图都应是真实场景或精心摆拍的产品。circle-cropped 不适合 Coca-Cola — 保持矩形 framing。

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
| 圆角 | 0 px 锐利矩形为主；CTA 按钮例外可用 9999 px (full pill)，与 coca-cola.com 当前样式一致 |
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
- [ ] Georgia 400, 700（Georgia）+ 300, 400, 600, 700（Helvetica Neue）允许斜体（Georgia italic） 已加载；不用 serif / display 字体
- [ ] 封面副标：仅用 Georgia 300 斜体（如果 300 italic 不可用，用品牌等价值）

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
