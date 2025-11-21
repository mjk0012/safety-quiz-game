import streamlit as st
import random

# ------------------- 游戏核心数据 -------------------
# 安全知识题库 (与你提供的完全一致)
safety_questions = [
    {
        "question": "以下哪种密码最安全？",
        "options": [
            "A. 使用生日作为密码",
            "B. 使用重复的字符如 '111111'",
            "C. 包含字母、数字和特殊字符的复杂密码",
            "D. 使用简单的单词如 'password'"
        ],
        "answer": "C",
        "explanation": "复杂密码能有效防止暴力破解，建议定期更换并避免重复使用。"
    },
    {
        "question": "收到陌生邮件附件应该怎么做？",
        "options": [
            "A. 立即打开查看内容",
            "B. 先扫描病毒再决定是否打开",
            "C. 直接删除邮件",
            "D. 转发给同事帮忙查看"
        ],
        "answer": "B",
        "explanation": "陌生邮件附件可能包含病毒或恶意软件，应先使用杀毒软件扫描。"
    },
    {
        "question": "在公共 Wi-Fi 环境下，以下哪些操作是安全的？",
        "options": [
            "A. 登录网上银行",
            "B. 浏览新闻网站",
            "C. 输入个人身份证信息",
            "D. 进行在线支付"
        ],
        "answer": "B",
        "explanation": "公共 Wi-Fi 存在安全风险，避免在其上进行涉及敏感信息的操作。"
    },
    {
        "question": "如何防范钓鱼网站？",
        "options": [
            "A. 点击邮件中的链接直接访问",
            "B. 仔细检查网址是否正确",
            "C. 随意下载网站上的文件",
            "D. 相信网站上的所有信息"
        ],
        "answer": "B",
        "explanation": "钓鱼网站常伪造正规网站，要注意核对网址拼写，避免上当受骗。"
    },
    {
        "question": "电脑感染病毒后，首先应该做什么？",
        "options": [
            "A. 继续使用电脑",
            "B. 立即断开网络连接",
            "C. 删除所有文件",
            "D. 重启电脑"
        ],
        "answer": "B",
        "explanation": "断开网络可以防止病毒传播和数据泄露，然后使用杀毒软件进行扫描。"
    }
]

# ------------------- Streamlit 网页逻辑 -------------------

# 设置页面配置 (必须是脚本的第一行 Streamlit 命令)
st.set_page_config(
    page_title="安全知识问答小游戏",
    page_icon="🔒",
    layout="centered"
)

# 初始化会话状态，用于存储跨页面刷新的数据（如分数、当前题目索引等）
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'shuffled_questions' not in st.session_state:
    # 游戏开始时，随机打乱题目顺序
    st.session_state.shuffled_questions = random.sample(safety_questions, len(safety_questions))
if 'user_answer_submitted' not in st.session_state:
    st.session_state.user_answer_submitted = False
if 'user_choice' not in st.session_state:
    st.session_state.user_choice = None


# ------------------- 辅助函数 -------------------

def reset_game():
    """重置游戏状态，用于重新开始"""
    st.session_state.score = 0
    st.session_state.current_question_index = 0
    st.session_state.shuffled_questions = random.sample(safety_questions, len(safety_questions))
    st.session_state.user_answer_submitted = False
    st.session_state.user_choice = None


# ------------------- 主页面显示 -------------------

# 标题和介绍
st.title("🔒 安全知识问答小游戏 🔒")
st.markdown("---")
st.subheader("测试你的网络安全知识！")
st.write("每答对一题得 10 分，共有 5 道题目。准备好了吗？")

# 游戏逻辑控制
current_index = st.session_state.current_question_index
total_questions = len(st.session_state.shuffled_questions)

if current_index < total_questions:
    # 显示当前题目
    current_question = st.session_state.shuffled_questions[current_index]
    st.markdown(f"### 第 {current_index + 1} 题 / 共 {total_questions} 题")
    st.write(f"**{current_question['question']}**")

    st.markdown("---")

    # 显示选项按钮
    st.write("**请选择你的答案：**")
    # 使用 `key` 确保每个按钮的唯一性
    for option in current_question['options']:
        if st.button(option, key=option):
            st.session_state.user_choice = option[0]  # 获取选项的第一个字符，即 A, B, C, D
            st.session_state.user_answer_submitted = True

    st.markdown("---")

    # 检查答案并显示结果
    if st.session_state.user_answer_submitted and st.session_state.user_choice:
        user_answer = st.session_state.user_choice
        correct_answer = current_question['answer']

        if user_answer == correct_answer:
            st.success("✅ 回答正确！")
            st.session_state.score += 10
        else:
            st.error(f"❌ 回答错误！正确答案是：**{correct_answer}**")

        st.info(f"💡 知识拓展：{current_question['explanation']}")

        st.markdown("---")

        # 显示当前得分
        st.write(f"**当前得分：{st.session_state.score} 分**")

        # 下一题按钮
        if st.button("👉 进入下一题"):
            st.session_state.current_question_index += 1
            st.session_state.user_answer_submitted = False  # 重置提交状态
            st.session_state.user_choice = None  # 重置用户选择
            st.rerun()  # 刷新页面以显示下一题

else:
    # 游戏结束，显示最终得分
    st.markdown("### 🎉 游戏结束！ 🎉")
    st.write(f"你的最终得分是：**{st.session_state.score}** 分")

    if st.session_state.score == 50:
        st.markdown("**🎉 太棒了！你是安全知识专家！**")
    elif st.session_state.score >= 30:
        st.markdown("**👍 不错哦！继续学习可以变得更专业！**")
    else:
        st.markdown("**💪 还需要加强学习，多了解安全知识哦！**")

    st.markdown("---")

    # 重新开始按钮
    if st.button("🔄 重新开始游戏"):
        reset_game()
        st.rerun()  # 刷新页面以重新开始