# Kimu Skills

Kimu 工具箱是一组可组合的 Agent Skills。统一入口是 `kimu`，日常使用不依赖某个 Agent 的专用斜杠或美元符号语法。

## 包含模块

| 模块 | 用途 |
|---|---|
| `kimu` | 理解当前任务并路由到合适模块 |
| `kimu-chatroom` | 多专家视角讨论；教培话题优先选择历史教育家 |
| `kimu-learning-coach` | 连续、自适应的主题学习与读书共学 |
| `kimu-concept-clarifier` | 通用概念拆解，重点澄清教培与知识付费中的模糊用语 |
| `kimu-teacher-business-diagnosis` | 教师、教培与知识付费商业模式诊断 |
| `kimu-case-bank` | 公共可核验案例与本机私有案例的分层管理 |
| `kimu-viewpoint-script` | 课程材料转观点提词稿 |

## 一句话安装

仓库访问者已登录 GitHub 且具备本私有仓库权限时，在终端运行：

```bash
npx -y skills add kimuxuezhang/kimu-skills -g --all
```

如果已下载到电脑，也可以从本地目录安装：

```bash
npx -y skills add /你的绝对路径/kimu-skills -g --all
```

以上方式需要 Node.js、网络和终端执行权限。`--all` 会把全部 Skill 安装到 Skills CLI 当前支持并检测到的 Agent；它不保证覆盖未被该 CLI 支持的 Agent。

### WorkBuddy

如果 Skills CLI 没有识别 WorkBuddy，请在 WorkBuddy 的「技能」页面选择「添加技能」，分别上传 `skills/` 下包含 `SKILL.md` 的模块文件夹或 ZIP。

## 统一使用方式

安装并启用后，直接用自然语言输入：

```text
Kimu：帮我判断现在该用哪个工具处理这个问题。
```

也可以直达模块：

```text
Kimu 聊天室：请让三位合适的历史教育家讨论“线上课程能否替代线下教学”。
Kimu 学习教练：请带我学习《纳瓦尔宝典》这本书。
Kimu 概念澄清：拆解“个人品牌”这个概念。
Kimu 教师商业模式诊断：我的线下授课产能已经占用一半，帮我判断下一阶段该验证什么。
Kimu 案例库：为这个观点找一个可核验案例。
Kimu 观点提词稿：把这份课程材料提炼成授课观点大纲。
```

Codex、Claude Code 等宿主可能额外提供 `$技能名` 或斜杠命令，但这些只是宿主快捷方式，不是 Kimu 的跨平台使用前提。

## 更新

仓库发布新版本后，已通过 Skills CLI 安装的用户可运行：

```bash
npx -y skills update kimu kimu-chatroom kimu-learning-coach kimu-concept-clarifier kimu-teacher-business-diagnosis kimu-case-bank kimu-viewpoint-script -g -y
```

通过 WorkBuddy 手动上传的用户需要重新下载并覆盖旧版本。

## 许可证

当前版本为 `0.3.0`，采用 [CC BY-NC 4.0](LICENSE) 非商业许可。

- 可以下载、使用、分享和修改；
- 使用或修改后发布时必须署名 Kimu，并说明是否改动；
- 不允许商业使用。

完整条款以仓库中的 `LICENSE` 为准。
