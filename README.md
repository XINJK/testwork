# testwork：五个独立测试子代理

五个互不联通、各自自带审查能力的测试子代理。你手动投放文件、用 `@` 点名调用、手动把产物喂给下一个环节。

## 目录结构

```
testwork\
├─ .opencode\agent\            # 五个子代理定义（重启 opencode 后生效）
│   ├─ prd-analyst.md          # 代理1：PRD 业务分析 + 疑点排查
│   ├─ testpoint-designer.md   # 代理2：测试点/功能点（XMind 可导入）
│   ├─ func-case-writer.md     # 代理3：功能测试用例（md + xlsx）
│   ├─ api-case-writer.md      # 代理4：接口测试用例（md + xlsx）
│   └─ automation-case-writer.md # 代理5：接口自动化用例（md + xlsx）
├─ tools\
│   ├─ extract_input.py        # 多格式文件 → Markdown（带锚点）
│   └─ export_xlsx.py          # 用例 Markdown → Excel
├─ input\                      # 你投放原始文件的地方
│   └─ extracted\              # 自动生成的提取文本（可随时重建）
├─ output\<代理名>\            # 各代理产物（带时间戳，不覆盖历史）
├─ frameworks\                 # 自动化框架样本（代理5 使用）
│   ├─ 接口自动化进阶1\
│   └─ 接口自动化3\
└─ README.md
```

## 五个代理速查

| 代理 | 输入 | 产物 |
|---|---|---|
| `prd-analyst` | PRD 文件路径 | `output\prd-analyst\PRD分析-<需求名>-<时间戳>.md` |
| `testpoint-designer` | PRD 文件路径 | `output\testpoint-designer\测试点-<需求名>-<时间戳>.xmind.md` + 同名 `.review.md` |
| `func-case-writer` | 测试点 md（可选加 PRD） | `output\func-case-writer\功能用例-<需求名>-<时间戳>.md` + `.xlsx` |
| `api-case-writer` | 接口文档（可选加测试点 md） | `output\api-case-writer\接口用例-<系统名>-<时间戳>.md` + `.xlsx` |
| `automation-case-writer` | 框架路径 + 接口文档（可选） | `output\automation-case-writer\自动化用例-<框架名>-<主题>-<时间戳>.md` + `.xlsx` |

## 使用流程

1. **投放文件**：把 PRD / 接口文档 / 测试点文件拷入 `input\`（也支持在调用时直接给项目内的其他路径）。
2. **@ 调用代理**（在 opencode 对话里）：
   ```
   @prd-analyst 分析 input\题库小程序2.0_PRD初稿.pdf
   @testpoint-designer 基于 input\题库小程序2.0_PRD初稿.pdf 输出测试大纲
   @func-case-writer 用 output\testpoint-designer\测试点-xxx.xmind.md 生成功能用例
   @api-case-writer 用 input\电商交易系统接口文档.md 生成接口用例
   @automation-case-writer 基于 frameworks\接口自动化3，接口文档 input\xxx.md
   ```
   不给路径时代理会扫描 `input\`；候选不唯一或输入不足时会主动问你。
3. **查看产物**：打开 `output\<代理名>\` 下最新时间戳文件；md 末尾有「自检与审查记录」。

## 文件格式支持

| 格式 | 处理方式 |
|---|---|
| `.md` `.txt` `.json` `.yaml` `.yml` | 直接读取 |
| `.pdf` `.docx` `.xlsx` `.csv` `.html` | 代理自动执行 `python tools/extract_input.py "<文件>"`，读取 `input\extracted\<同名>.md` |
| `.xls` `.doc` `.ppt` `.pptx` | 不支持：先用 WPS/Office 另存为 `.xlsx`/`.docx` |
| 图片 / 扫描件 PDF | 不支持（无 OCR）：请提供文字版 |

手动转换命令示例：

```
python tools\extract_input.py "input\需求文档.docx"
python tools\extract_input.py --force "input\需求文档.docx"   # 覆盖重提取
```

## 关键规则

- **不联通**：五个代理互不调用、互不读取对方产物，串联只靠你手动投喂。
- **自带审查**：每个代理产出后强制自审（来源可追溯 / 覆盖完整 / 格式合规 / 无编造），产物内附审查记录（代理2 写在伴生 `.review.md`，保持 XMind 文件干净）。
- **来源引用**：产物中的事实必须能指回原文 `路径#锚点 | "原文摘录"`；推不出的内容标 `<TBD>`。
- **降级策略（仅代理5）**：A=框架+接口文档（全量生成）；B=仅框架代码（只对已有实证的接口生成扩展用例，逐字段引用证据）；C=框架内无依据（只输出规范报告+空白模板）。
- **修订**：新需求产生新时间戳文件，历史不覆盖。

## 框架样本说明

`frameworks\` 内置两个自动化框架样本，供代理5（automation-case-writer）演示"基于现有框架生成扩展用例"：

- `接口自动化3`：本人独立实现的 pytest 数据驱动接口自动化框架（完整版见独立仓库 `practice_api_auto_framework`）
- `接口自动化进阶1`：学习跟练项目，作为对照样本

## 常见问题

- **改动后什么时候生效？** 代理/配置在 opencode 启动时加载，修改后需退出并重启 opencode。
- **文件在桌面上不想拷贝？** 代理只能读 `testwork\` 内文件（外部目录权限已禁用），请先拷入 `input\`。
- **公司有固定用例模板？** 后续把模板样例给我，修改对应代理的字段定义即可。
- **XMind 导入**：打开 XMind → 文件 → 导入 → Markdown → 选择 `.xmind.md` 文件（不要改文件格式，不要加 frontmatter）。

## 上线验证清单（重启 opencode 后）

1. `@testpoint-designer`：投喂 `题库小程序2.0_PRD初稿 副本.pdf`（可从 `Desktop\prd_to_xmind\input\` 拷入），确认生成 `.xmind.md` 并用 XMind 试导入。
2. `@prd-analyst`：投喂同一个 PDF，检查疑点清单是否带原文位置。
3. `@func-case-writer`：投喂第 1 步产物，确认生成 md + xlsx，xlsx 可打开。
4. `@api-case-writer`：投喂 `Desktop\testflow.0.1\artifacts\00-input\电商交易系统接口文档-v1.0.md`，确认 md + xlsx。
5. `@automation-case-writer`：先指定 `frameworks\接口自动化3` + 接口文档（A 级）；再试仅框架代码（B 级降级）。
