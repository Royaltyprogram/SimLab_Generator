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
        """Add a new section."""
        self.sections.append({
            "type": "section",
            "title": title,
            "content": content,
            "level": level
        })
        
    def add_code_block(self, code, language="javascript"):
        """Add a code block."""
        self.sections.append({
            "type": "code",
            "content": code,
            "language": language
        })
        
    def add_api_response(self, title, response, is_code=False):
        """Add an API response."""
        if is_code:
            self.add_section(title, "")
            self.add_code_block(response)
        else:
            self.add_section(title, response)
            
    def save_markdown(self):
        """Save as a markdown file."""
        if not os.path.exists("results"):
            os.makedirs("results")
            
        with open(self.md_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Simulation Generation Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
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
    """Display API keys input form."""
    st.title("AI-Based Scientific Simulation Code Generator")
    
    with st.form("api_keys_form"):
        st.write("Please enter your API keys before starting.")
        claude_api_key = st.text_input("Claude API Key", type="password")
        hf_token = st.text_input("Huggingface Token", type="password")
        
        submit_button = st.form_submit_button("Submit API Keys")
        
        if submit_button and claude_api_key and hf_token:
            st.session_state.claude_api_key = claude_api_key
            st.session_state.hf_token = hf_token
            st.session_state.api_keys_submitted = True
            st.rerun()

def main_app():
    """Display main app interface."""
    st.title("AI-Based Scientific Simulation Code Generator")
    
    with st.sidebar:
        st.markdown("### Example Requests:")
        st.markdown("""
        - Simple Pendulum Simulation (adjustable length and initial angle)
        - Ideal Gas Law Simulation (visualization of pressure, volume, temperature relationships)
        - Projectile Motion Simulation (adjustable initial velocity and angle)
        """)
        
        if st.button("Re-enter API Keys"):
            st.session_state.api_keys_submitted = False
            st.rerun()
    
    user_request = st.text_area("Please describe the simulation you want", height=100, placeholder="Please describe your desired simulation in as much detail as possible.")
    
    if st.button("Generate Simulation Code"):
        if not user_request.strip():
            st.error("Please enter a simulation description!")
            return
            
        with st.spinner("Generating simulation code..."):
            logger = StreamlitLogger()
            logger.add_section("User Request", user_request, level=2)
            
            # Progress bar
            progress_bar = st.progress(0)
            
            # Step 1: Qwen's Initial Research
            st.subheader("1. Qwen's Initial Research")
            research = ask_qwen(st.session_state.hf_token, 
                              f'Please conduct preliminary research on {user_request} and create a plan for simulating this concept. Tell me which libraries to use and how to create the simulation. Do not write code yet.')
            logger.add_api_response("Qwen's Initial Research", research)
            st.write(research)
            progress_bar.progress(25)
            
            # Step 2: Claude's Initial Simulation Code Draft
            st.subheader("2. Claude's Initial Simulation Code Draft")
            claude_response = get_claude_response(st.session_state.claude_api_key, user_request)
            
            with st.expander("View Code"):
                st.code(claude_response['code'], language='javascript')
            with st.expander("View Explanation"):
                st.write(claude_response['explanation'])
            with st.expander("View Improvements"):
                st.write(claude_response['improvements'])
                
            logger.add_api_response("Claude's Initial Simulation Code Draft (Code)", claude_response['code'], is_code=True)
            logger.add_api_response("Claude's Initial Simulation Code Draft (Explanation)", claude_response['explanation'])
            logger.add_api_response("Claude's Initial Simulation Code Draft (Improvements)", claude_response['improvements'])
            progress_bar.progress(50)
            
            # Step 3: Qwen's Simulation Refinement
            st.subheader("3. Qwen's Simulation Refinement")
            for i in range(1, 4):
                qwen_response = get_qwen_improvements(st.session_state.hf_token, 
                                                    code_info=claude_response, iteration=i)
                
                with st.expander(f"Iteration {i} - View Code"):
                    st.code(qwen_response['code'], language='javascript')
                with st.expander(f"Iteration {i} - View Explanation"):
                    st.write(qwen_response['explanation'])
                with st.expander(f"Iteration {i} - View Improvements"):
                    st.write(qwen_response['improvements'])
                    
                logger.add_api_response(f"Qwen's Simulation Refinement (Code)(Iteration {i})", qwen_response['code'], is_code=True)
                logger.add_api_response(f"Qwen's Simulation Refinement (Explanation)(Iteration {i})", qwen_response['explanation'])
                logger.add_api_response(f"Qwen's Simulation Refinement (Improvements)(Iteration {i})", qwen_response['improvements'])
                progress_bar.progress(50 + (i * 10))
            
            # Step 4: Claude's Final Review
            st.subheader("4. Claude's Final Review")
            prompt = f'{qwen_response} Please perform a final review of this code. Identify and fix any potential error-prone areas.'
            claude_final = get_claude_response(st.session_state.claude_api_key, prompt)
            
            with st.expander("View Final Code"):
                st.code(claude_final['code'], language='javascript')
            with st.expander("View Final Explanation"):
                st.write(claude_final['explanation'])
            with st.expander("View Final Improvements"):
                st.write(claude_final['improvements'])
                
            logger.add_api_response("Claude's Final Review (Code)", claude_final['code'], is_code=True)
            logger.add_api_response("Claude's Final Review (Explanation)", claude_final['explanation'])
            logger.add_api_response("Claude's Final Review (Improvements)", claude_final['improvements'])
            progress_bar.progress(100)
            
            # Error Reporting and Fixes
            st.subheader("Error Reporting and Fixes")
            st.session_state.current_code = claude_final
            
            # Display previous fixes
            if st.session_state.error_fixes:
                st.write("Previous Fixes:")
                for i, fix in enumerate(st.session_state.error_fixes, 1):
                    with st.expander(f"Fix #{i}"):
                        st.text("Error Description:")
                        st.code(fix["error"])
                        st.text("Fixed Code:")
                        st.code(fix["code"])
            
            error_message = st.text_area("If you encountered any errors, please enter them here")
            if st.button("Request Error Fix") and error_message:
                with st.spinner("Fixing errors..."):
                    fix_result = get_claude_response(
                        st.session_state.claude_api_key,
                        create_error_fix_prompts(st.session_state.current_code, error_message)
                    )
                    
                    if fix_result:
                        st.success("Errors have been fixed!")
                        st.session_state.error_fixes.append({
                            "error": error_message,
                            "code": fix_result["code"],
                            "explanation": fix_result["explanation"],
                            "improvements": fix_result.get("improvements", "")
                        })
                        st.session_state.current_code = fix_result
                        
                        with st.expander("View Fixed Code"):
                            st.code(fix_result["code"], language='javascript')
                        with st.expander("View Fix Explanation"):
                            st.write(fix_result["explanation"])
                        if "fix_notes" in fix_result:
                            with st.expander("View Fix Notes"):
                                st.write(fix_result["improvements"])
                    else:
                        st.error("Failed to fix errors.")
            
            # Code Q&A Section
            st.markdown("---")
            st.subheader("Ask Questions About the Code")
            
            code_question = st.text_area(
                "Ask any questions about the code",
                placeholder="Example: How does this specific part work? Or how can I modify this section?"
            )
            
            if st.button("Ask Question") and code_question:
                with st.spinner("Generating answer..."):
                    # Create prompt with current code and question
                    question_prompt = f"""Please answer the following question about this code:

Code:
{st.session_state.current_code['code']}

Question:
{code_question}

Please provide a detailed and clear explanation."""

                    # Generate answer through Claude
                    response = get_claude_response(
                        st.session_state.claude_api_key,
                        question_prompt
                    )
                    
                    if response:
                        st.write("### Answer")
                        st.write(response.get('improvements', 'Failed to generate answer.'))
                        
                        # If code example is included
                        if 'code' in response and response['code']:
                            with st.expander("Related Code Example"):
                                st.code(response['code'], language='javascript')
                        if 'explanation' in response and response['explanation']:
                            with st.expander("Modification/Query Explanation"):
                                st.write(response['explanation'])
                        if 'improvements' in response and response['improvements']:
                            with st.expander("Additional Improvements"):
                                st.write(response['improvements'])
                    else:
                        st.error("Failed to generate answer.")

def main():
    init_session_state()
    
    if not st.session_state.api_keys_submitted:
        api_keys_form()
    else:
        main_app()

if __name__ == "__main__":
    main()