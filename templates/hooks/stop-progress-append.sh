#!/bin/bash
# Stop hook：每轮回答后，把"用户这轮的请求"增量追加到项目进度文件的「增量流水」区。
# 纯文本、不调 LLM、扛关电脑（每轮即落盘，崩溃最多丢正在进行的一轮）。
# 进度文件优先 $cwd/M1/PROGRESS.md，回退 $cwd/STATUS.md；都没有就静默退出。

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty'); [ -z "$CWD" ] && CWD="$(pwd)"
SID=$(echo "$INPUT" | jq -r '.session_id // "x"')
TP=$(echo "$INPUT" | jq -r '.transcript_path // empty')

PF=""
for c in "$CWD/M1/PROGRESS.md" "$CWD/STATUS.md"; do
  [ -f "$c" ] && PF="$c" && break
done
[ -z "$PF" ] && exit 0
[ -z "$TP" ] && exit 0
[ ! -f "$TP" ] && exit 0

# 取最后一条 user 文本消息（兼容 content 为 string / array 两种格式）
LAST=$(jq -r 'select(.type=="user") | .message
  | if type=="object" and .content!=null then
      (if (.content|type)=="string" then .content
       elif (.content|type)=="array" then ([.content[]|select(.type=="text")|.text]|join(" "))
       else empty end)
    elif type=="string" then .
    else empty end' "$TP" 2>/dev/null \
  | grep -v '^$' | grep -v '^<' | tail -1)
[ -z "$LAST" ] && exit 0

# 按 session 去重，避免 Stop 同一轮多次触发重复写
MARK="/tmp/.stopprog-${SID}"
HASH=$(printf '%s' "$LAST" | cksum | cut -d' ' -f1)
[ -f "$MARK" ] && [ "$(cat "$MARK")" = "$HASH" ] && exit 0
echo "$HASH" > "$MARK"

EXCERPT=$(printf '%s' "$LAST" | tr '\n' ' ' | cut -c1-100)
TS=$(date '+%Y-%m-%d %H:%M')
grep -q "^## 🤖 增量流水（待整理）" "$PF" 2>/dev/null \
  || printf '\n## 🤖 增量流水（待整理）\n' >> "$PF"
printf -- '- [%s] %s\n' "$TS" "$EXCERPT" >> "$PF"
exit 0
