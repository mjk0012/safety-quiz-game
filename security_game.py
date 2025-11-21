import streamlit as st
import random
import time
import base64
from pathlib import Path


# ------------------- 页面背景设置 -------------------
def set_background(image_file):
    """设置背景并优化内容区域显示"""
    try:
        # 读取图片文件
        image_path = Path(__file__).parent / image_file
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        # 设置背景和内容区域样式（提高对比度）
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url('data:image/jpeg;base64,{encoded_string}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            /* 内容容器 - 提高不透明度和对比度 */
            .stApp > div:first-child {{
                background-color: rgba(255, 255, 255, 0.95);  /* 更不透明的白色背景 */
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 6px 16px rgba(0,0,0,0.2);  /* 更深的阴影增强层次感 */
                max-width: 800px;
                margin: 30px auto;
            }}
            /* 文字颜色加深，确保可读性 */
            .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp div {{
                color: #333333 !important;
            }}
            /* 按钮样式优化 */
            .stButton > button {{
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 16px;
            }}
            /* 钥匙动画 */
            .key-animation {{
                animation: spin 1s linear;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); opacity: 0; }}
                50% {{ transform: rotate(180deg); opacity: 1; }}
                100% {{ transform: rotate(360deg); }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"未找到背景图片 '{image_file}'，请确保图片与脚本在同一文件夹")
    except Exception as e:
        st.error(f"加载背景出错: {e}")


# ------------------- 游戏核心数据 -------------------
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
st.set_page_config(
    page_title="安全知识闯关游戏",
    page_icon="🔑",
    layout="centered"
)

# 设置背景（确保background.jpg与脚本在同一文件夹）
set_background('background.jpg')

# 初始化会话状态
if 'keys_collected' not in st.session_state:
    st.session_state.keys_collected = 0
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = random.sample(safety_questions, len(safety_questions))
if 'user_answer_submitted' not in st.session_state:
    st.session_state.user_answer_submitted = False
if 'user_choice' not in st.session_state:
    st.session_state.user_choice = None


# ------------------- 辅助函数 -------------------
def reset_game():
    """重置游戏状态"""
    st.session_state.keys_collected = 0
    st.session_state.current_question_index = 0
    st.session_state.shuffled_questions = random.sample(safety_questions, len(safety_questions))
    st.session_state.user_answer_submitted = False
    st.session_state.user_choice = None


# ------------------- 主页面显示 -------------------
# 强制设置文字颜色为深色，确保可读性
st.markdown("""<style>
    .big-font { font-size: 24px !important; color: #333333; }
    .normal-font { color: #333333; }
</style>""", unsafe_allow_html=True)

st.markdown('<h1 class="big-font">🔒 安全知识闯关游戏 🔒</h1>', unsafe_allow_html=True)
st.markdown("---")

# 显示钥匙收集进度
st.subheader("当前进度: {} 把钥匙 / 共 5 把".format(st.session_state.keys_collected))
keys_display = "🔑" * st.session_state.keys_collected + "🔒" * (5 - st.session_state.keys_collected)
st.markdown(f"<div style='text-align: center; font-size: 2em; color: #333333;'>{keys_display}</div>",
            unsafe_allow_html=True)

st.markdown("---")

current_index = st.session_state.current_question_index
total_questions = len(st.session_state.shuffled_questions)

if current_index < total_questions:
    current_question = st.session_state.shuffled_questions[current_index]
    st.markdown(f"### 🚪 第 {current_index + 1} 关")
    st.markdown(f"<p class='normal-font'><strong>{current_question['question']}</strong></p>", unsafe_allow_html=True)

    st.markdown("---")

    st.write("**请选择你的答案：**")
    for option in current_question['options']:
        if st.button(option, key=option):
            st.session_state.user_choice = option[0]
            st.session_state.user_answer_submitted = True

    st.markdown("---")

    if st.session_state.user_answer_submitted and st.session_state.user_choice:
        user_answer = st.session_state.user_choice
        correct_answer = current_question['answer']

        if user_answer == correct_answer:
            st.success("✅ 回答正确！")

            # 显示钥匙动画
            st.markdown("""
            <div class="key-animation" style="text-align: center; font-size: 3em;">
            🔑
            </div>
            """, unsafe_allow_html=True)
            st.success("恭喜获得一把安全钥匙！")

            st.session_state.keys_collected += 1

            # 短暂延迟后继续
            time.sleep(1.5)
        else:
            st.error(f"❌ 回答错误！正确答案是：**{correct_answer}**")

        st.info(f"💡 知识拓展：{current_question['explanation']}")

        st.markdown("---")

        # 下一关按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("👉 进入下一关"):
                st.session_state.current_question_index += 1
                st.session_state.user_answer_submitted = False
                st.session_state.user_choice = None
                st.rerun()

else:
    # 游戏结束
    st.markdown("### 🎉 恭喜通关！ 🎉")
    st.write(f"你成功收集了所有 5 把安全钥匙！")

    if st.session_state.keys_collected == 5:
        st.markdown("""
        <div style="text-align: center; font-size: 3em;">
        🏆🔑🔑🔑🔑🔑🏆
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**你成为了真正的网络安全专家！**")
    else:
        st.markdown("**继续努力，争取收集所有钥匙！**")

    st.markdown("---")

    # 重新开始按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 重新开始游戏"):
            reset_game()
            st.rerun()