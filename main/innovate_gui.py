import streamlit as st
import json
import os
from datetime import datetime
from api_calls import ClaudeAPI, QwenAPI, ask_qwen, create_error_fix_prompts, get_claude_response, get_qwen_improvements

class StreamlitLogger:
    def __init__(self):
        self.sections = []
        self.md_filename = os.path.join(
            "results", 
            f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
    def add_section(self, title, content, level=2):
        """새로운 섹션을 추가합니다."""
        self.sections.append({
            "type": "section",
            "title": title,
            "content": content,
            "level": level
        })
        
    def add_code_block(self, code, language="javascript"):
        """코드 블록을 추가합니다."""
        self.sections.append({
            "type": "code",
            "content": code,
            "language": language
        })
        
    def add_api_response(self, title, response, is_code=False):
        """API 응답을 추가합니다."""
        if is_code:
            self.add_section(title, "")
            self.add_code_block(response)
        else:
            self.add_section(title, response)
            
    def save_markdown(self):
        """마크다운 파일로 저장합니다."""
        if not os.path.exists("results"):
            os.makedirs("results")
            
        with open(self.md_filename, 'w', encoding='utf-8') as f:
            f.write(f"# 시뮬레이션 생성 로그 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for section in self.sections:
                if section["type"] == "section":
                    f.write(f"\n{'#' * section['level']} {section['title']}\n\n{section['content']}\n")
                elif section["type"] == "code":
                    f.write(f"\n```{section['language']}\n{section['content']}\n```\n")
        
        return self.md_filename

def init_session_state():
    """Initialize session state variables"""
    if "api_keys_submitted" not in st.session_state:
        st.session_state.api_keys_submitted = False
    if "error_fixes" not in st.session_state:
        st.session_state.error_fixes = []
    if "current_code" not in st.session_state:
        st.session_state.current_code = None

def api_keys_form():
    """API 키 입력 폼을 표시합니다."""
    st.title("AI 기반 과학 시뮬레이션 코드 생성기")
    
    with st.form("api_keys_form"):
        st.write("시작하기 전에 API 키를 입력해주세요.")
        claude_api_key = st.text_input("Claude API Key", type="password")
        hf_token = st.text_input("Huggingface Token", type="password")
        
        submit_button = st.form_submit_button("API 키 제출")
        
        if submit_button and claude_api_key and hf_token:
            st.session_state.claude_api_key = claude_api_key
            st.session_state.hf_token = hf_token
            st.session_state.api_keys_submitted = True
            st.rerun()

def main_app():
    """메인 앱 인터페이스를 표시합니다."""
    st.title("AI 기반 과학 시뮬레이션 코드 생성기")
    
    with st.sidebar:
        st.markdown("### 예시 요청:")
        st.markdown("""
        - 단진자 운동 시뮬레이션 (진자의 길이와 초기각을 조절 가능)
        - 이상기체 상태방정식 시뮬레이션 (압력, 부피, 온도 관계 시각화)
        - 포물선 운동 시뮬레이션 (초기 속도와 각도 조절 가능)
        """)
        
        if st.button("API 키 재입력"):
            st.session_state.api_keys_submitted = False
            st.rerun()
    
    user_request = st.text_area("원하는 시뮬레이션을 설명해주세요", height=100, placeholder="최대한 구체적으로 원하는 시뮬레이션을 묘사해주세요.")
    
    if st.button("시뮬레이션 코드 생성"):
        if not user_request.strip():
            st.error("시뮬레이션 설명을 입력해주세요!")
            return
            
        with st.spinner("시뮬레이션 코드를 생성하고 있습니다..."):
            logger = StreamlitLogger()
            logger.add_section("사용자 요청", user_request, level=2)
            
            # Progress bar
            progress_bar = st.progress(0)
            
            # Step 1: Qwen의 사전조사
            st.subheader("1. Qwen의 사전조사")
            research = ask_qwen(st.session_state.hf_token, 
                              f'{user_request}에 대해 사전조사를 진행하고 이 개념을 시뮬레이션을 하기 위한 계획을 세워줘. 어떤 라이브러리를 어떻게 활용해서 어떤 시뮬레이션을 만들 지 알려줘. 코드 작성은 하지마.')
            logger.add_api_response("Qwen의 사전조사", research)
            st.write(research)
            progress_bar.progress(25)
            
            # Step 2: Claude의 시뮬레이션 코드 초안 생성
            st.subheader("2. Claude의 시뮬레이션 코드 초안 생성")
            claude_response = get_claude_response(st.session_state.claude_api_key, user_request)
            
            with st.expander("코드 보기"):
                st.code(claude_response['code'], language='javascript')
            with st.expander("설명 보기"):
                st.write(claude_response['explanation'])
            with st.expander("개선사항 보기"):
                st.write(claude_response['improvements'])
                
            logger.add_api_response("Claude의 시뮬레이션 코드 초안 생성 (코드)", claude_response['code'], is_code=True)
            logger.add_api_response("Claude의 시뮬레이션 코드 초안 생성 (설명)", claude_response['explanation'])
            logger.add_api_response("Claude의 시뮬레이션 코드 초안 생성 (개선사항)", claude_response['improvements'])
            progress_bar.progress(50)
            
            # Step 3: Qwen의 시뮬레이션 구체화
            st.subheader("3. Qwen의 시뮬레이션 구체화")
            for i in range(1, 4):
                qwen_response = get_qwen_improvements(st.session_state.hf_token, 
                                                    code_info=claude_response, iteration=i)
                
                with st.expander(f"반복 {i} - 코드 보기"):
                    st.code(qwen_response['code'], language='javascript')
                with st.expander(f"반복 {i} - 설명 보기"):
                    st.write(qwen_response['explanation'])
                with st.expander(f"반복 {i} - 개선사항 보기"):
                    st.write(qwen_response['improvements'])
                    
                logger.add_api_response(f"Qwen의 시뮬레이션 구체화 (코드)(반복 {i})", qwen_response['code'], is_code=True)
                logger.add_api_response(f"Qwen의 시뮬레이션 구체화 (설명)(반복 {i})", qwen_response['explanation'])
                logger.add_api_response(f"Qwen의 시뮬레이션 구체화 (개선사항)(반복 {i})", qwen_response['improvements'])
                progress_bar.progress(50 + (i * 10))
            
            # Step 4: Claude의 최종점검
            st.subheader("4. Claude의 최종점검")
            prompt = f'{qwen_response} 이 코드에 대한 최종 점검해. 이 코드에서 오류 발생이 예상되는 부분을 수정해.'
            claude_final = get_claude_response(st.session_state.claude_api_key, prompt)
            
            with st.expander("최종 코드 보기"):
                st.code(claude_final['code'], language='javascript')
            with st.expander("최종 설명 보기"):
                st.write(claude_final['explanation'])
            with st.expander("최종 개선사항 보기"):
                st.write(claude_final['improvements'])
                
            logger.add_api_response("Claude의 최종점검 (코드)", claude_final['code'], is_code=True)
            logger.add_api_response("Claude의 최종점검 (설명)", claude_final['explanation'])
            logger.add_api_response("Claude의 최종점검 (개선사항)", claude_final['improvements'])
            progress_bar.progress(100)
            
            # 오류 보고 및 수정
            st.subheader("오류 보고 및 수정")
            st.session_state.current_code = claude_final
            
            # 이전 수정 내역 표시
            if st.session_state.error_fixes:
                st.write("이전 수정 내역:")
                for i, fix in enumerate(st.session_state.error_fixes, 1):
                    with st.expander(f"수정 #{i}"):
                        st.text("오류 내용:")
                        st.code(fix["error"])
                        st.text("수정된 코드:")
                        st.code(fix["code"])
            
            error_message = st.text_area("발생한 오류가 있다면 여기에 입력해주세요")
            if st.button("오류 수정 요청") and error_message:
                with st.spinner("오류를 수정하고 있습니다..."):
                    fix_result = get_claude_response(
                        st.session_state.claude_api_key,
                        create_error_fix_prompts(st.session_state.current_code, error_message)
                    )
                    
                    if fix_result:
                        st.success("오류가 수정되었습니다!")
                        st.session_state.error_fixes.append({
                            "error": error_message,
                            "code": fix_result["code"],
                            "explanation": fix_result["explanation"],
                            "improvements": fix_result.get("improvements", "")
                        })
                        st.session_state.current_code = fix_result
                        
                        with st.expander("수정된 코드 보기"):
                            st.code(fix_result["code"], language='javascript')
                        with st.expander("수정 설명 보기"):
                            st.write(fix_result["explanation"])
                        if "fix_notes" in fix_result:
                            with st.expander("수정 내용 보기"):
                                st.write(fix_result["improvements"])
                    else:
                        st.error("오류 수정에 실패했습니다.")
            
            # 코드 질의응답 섹션
            st.markdown("---")
            st.subheader("코드 관련 질문하기")
            
            code_question = st.text_area(
                "코드에 대해 궁금한 점을 질문해주세요",
                placeholder="예: 이 코드의 특정 부분이 어떻게 작동하나요? 또는 이 부분을 어떻게 수정할 수 있나요?"
            )
            
            if st.button("질문하기") and code_question:
                with st.spinner("답변을 생성하고 있습니다..."):
                    # 현재 코드와 질문을 포함한 프롬프트 생성
                    question_prompt = f"""다음 코드에 대한 질문에 답변해주세요:

코드:
{st.session_state.current_code['code']}

질문:
{code_question}

자세하고 명확한 설명을 제공해주세요."""

                    # Claude를 통한 답변 생성
                    response = get_claude_response(
                        st.session_state.claude_api_key,
                        question_prompt
                    )
                    
                    if response:
                        st.write("### 답변")
                        st.write(response.get('improvements', '답변을 생성하는 데 실패했습니다.'))
                        
                        # 코드 예시가 포함된 경우
                        if 'code' in response and response['code']:
                            with st.expander("관련 코드 예시"):
                                st.code(response['code'], language='javascript')
                        if 'explanation' in response and response['explanation']:
                            with st.expander("수정/질의에 대한 설명"):
                                st.write(response['explanation'])
                        if 'improvements' in response and response['improvements']:
                            with st.expander("추가 개선사항"):
                                st.write(response['improvements'])
                    else:
                        st.error("답변을 생성하는 데 실패했습니다.")

def main():
    init_session_state()
    
    if not st.session_state.api_keys_submitted:
        api_keys_form()
    else:
        main_app()

if __name__ == "__main__":
    main()