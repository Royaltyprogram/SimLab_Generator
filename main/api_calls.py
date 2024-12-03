from datetime import datetime
import json
import os
from anthropic import Anthropic
from openai import OpenAI

CLAUDE_SYSTEM_PROMPT = """You are a specialist in creating React-based scientific simulation components. Follow these guidelines:

1. React Component Structure:
   - Use functional components with hooks (useState, useEffect, useRef)
   - Implement proper cleanup in useEffect hooks
   - Use React refs for canvas/WebGL context management
   - Follow React best practices for state management and rendering optimization

2. Core Visualization Libraries:
   - Three.js with React Three Fiber for 3D simulations
   - P5.js with react-p5 for 2D creative coding
   - D3.js for data visualization
   - Matter.js for 2D physics
   - Chart.js with react-chartjs-2 for interactive charts
   - Paper.js for vector graphics

3. Component Integration:
   - Components should be self-contained and reusable
   - Use JavaScript (not TypeScript)
   - Use Tailwind CSS for styling (core utilities only, no arbitrary values)
   - Support responsive layouts
   - Implement proper event cleanup

4. Animation & Performance:
   - Use requestAnimationFrame for smooth animations
   - Implement proper canvas resize handlers
   - Optimize re-renders using useMemo and useCallback
   - Handle component unmount cleanup
   - Proper memory management with useRef

5. Scientific Accuracy:
   - Accurate physics calculations
   - Proper unit conversions
   - Clear visual feedback
   - Educational value in visualizations
   - Real-time parameter updates

6. State Management:
   - Clear separation of simulation state and UI state
   - Controlled inputs for simulation parameters
   - Proper state update batching
   - Error handling for calculations

Available Libraries (Already Installed):
- Three.js with React Three Fiber: 3D graphics/WebGL
- P5.js with react-p5: 2D creative coding
- D3.js: Data visualization
- Matter.js: 2D physics engine
- Chart.js with react-chartjs-2: Interactive charts
- Paper.js: Vector graphics

Component Template:
```jsx
const SimulationComponent = () => {
  const [simState, setSimState] = useState(initialState);
  const canvasRef = useRef(null);
  const frameRef = useRef(0);
  const animationRef = useRef(null);

  useEffect(() => {
    // Setup simulation
    const setup = () => {
      if (!canvasRef.current) return;
      // Initialize visualization
    };

    setup();
    animationRef.current = requestAnimationFrame(animate);

    return () => {
      // Cleanup
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  const animate = () => {
    if (!canvasRef.current) return;
    // Update simulation state
    // Render visualization
    animationRef.current = requestAnimationFrame(animate);
  };

  return (
    <div className="flex flex-col items-center w-full p-4">
      <div className="w-full max-w-4xl">
        <canvas ref={canvasRef} className="w-full aspect-video bg-white shadow-lg rounded-lg" />
      </div>
      {/* Controls */}
    </div>
  );
};

export default SimulationComponent;
Focus on:

Clean, maintainable JavaScript code
Proper memory and resource management
Smooth animations and visual feedback
Scientific accuracy in calculations
Educational value and interactivity
Responsive design using Tailwind core utilities only
Error handling and validation
"""

QWEN_SYSTEM_PROMPT = """You are a specialist in creating React-based scientific simulation components. Follow these guidelines:

1. React Component Structure:
   - Use functional components with hooks (useState, useEffect, useRef)
   - Implement proper cleanup in useEffect hooks
   - Use React refs for canvas/WebGL context management
   - Follow React best practices for state management and rendering optimization

2. Core Visualization Libraries:
   - Three.js with React Three Fiber for 3D simulations
   - P5.js with react-p5 for 2D creative coding
   - D3.js for data visualization
   - Matter.js for 2D physics
   - Chart.js with react-chartjs-2 for interactive charts
   - Paper.js for vector graphics

3. Component Integration:
   - Components should be self-contained and reusable
   - Use JavaScript (not TypeScript)
   - Use Tailwind CSS for styling (core utilities only, no arbitrary values)
   - Support responsive layouts
   - Implement proper event cleanup

4. Animation & Performance:
   - Use requestAnimationFrame for smooth animations
   - Implement proper canvas resize handlers
   - Optimize re-renders using useMemo and useCallback
   - Handle component unmount cleanup
   - Proper memory management with useRef

5. Scientific Accuracy:
   - Accurate physics calculations
   - Proper unit conversions
   - Clear visual feedback
   - Educational value in visualizations
   - Real-time parameter updates

6. State Management:
   - Clear separation of simulation state and UI state
   - Controlled inputs for simulation parameters
   - Proper state update batching
   - Error handling for calculations

Available Libraries (Already Installed):
- Three.js with React Three Fiber: 3D graphics/WebGL
- P5.js with react-p5: 2D creative coding
- D3.js: Data visualization
- Matter.js: 2D physics engine
- Chart.js with react-chartjs-2: Interactive charts
- Paper.js: Vector graphics

Component Template:
```jsx
const SimulationComponent = () => {
  const [simState, setSimState] = useState(initialState);
  const canvasRef = useRef(null);
  const frameRef = useRef(0);
  const animationRef = useRef(null);

  useEffect(() => {
    // Setup simulation
    const setup = () => {
      if (!canvasRef.current) return;
      // Initialize visualization
    };

    setup();
    animationRef.current = requestAnimationFrame(animate);

    return () => {
      // Cleanup
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  const animate = () => {
    if (!canvasRef.current) return;
    // Update simulation state
    // Render visualization
    animationRef.current = requestAnimationFrame(animate);
  };

  return (
    <div className="flex flex-col items-center w-full p-4">
      <div className="w-full max-w-4xl">
        <canvas ref={canvasRef} className="w-full aspect-video bg-white shadow-lg rounded-lg" />
      </div>
      {/* Controls */}
    </div>
  );
};

export default SimulationComponent;
Focus on:

Clean, maintainable JavaScript code
Proper memory and resource management
Smooth animations and visual feedback
Scientific accuracy in calculations
Educational value and interactivity
Responsive design using Tailwind core utilities only
Error handling and validation
"""


class ClaudeAPI:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
        
    def request_code(self, prompt):
        """코드 생성을 위한 API 요청"""
        request_prompt = f"""Create a complete, working React simulation for {prompt}. 
        The code must be immediately runnable and follow these requirements:
        - Use only installed libraries
        - Include all necessary imports
        - Provide a complete, single component
        - Include clear comments
        - Use proper cleanup and error handling
        - Follow responsive design principles
        - Include interactive controls
        
        The code must be production-ready and complete without any placeholder comments."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=4000,
                system=CLAUDE_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": request_prompt}]
            )
            return message.content[0].text.strip()
        except Exception as e:
            print(f"코드 생성 중 오류 발생: {str(e)}")
            return None

    def request_explanation(self, prompt):
        """시뮬레이션 구현 분석을 위한 API 요청"""
        analysis_prompt = f"""Analyze the implementation approach for {prompt} simulation:
        
        1. Scientific Concepts:
        - Key physics/math principles
        - Required calculations
        - Important variables
        
        2. Technical Approach:
        - Best library choice and why
        - State management strategy
        - Performance considerations
        
        3. Implementation Challenges:
        - Potential issues
        - Solutions and workarounds
        - Optimization opportunities"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=4000,
                system=CLAUDE_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            return message.content[0].text.strip()
        except Exception as e:
            print(f"설명 생성 중 오류 발생: {str(e)}")
            return None

    def request_improvements(self, prompt):
        """기존 시뮬레이션 코드 개선을 위한 API 요청"""
        improvements_prompt = f"""Review this simulation code and suggest specific improvements:

        {prompt}

        Focus on:
        1. Performance optimization
        2. Code organization
        3. Error handling
        4. User experience
        5. Scientific accuracy
        6. Visual feedback
        
        Provide specific, actionable improvements separated by commas."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=4000,
                system=CLAUDE_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": improvements_prompt}]
            )
            improvements_text = message.content[0].text.strip()
            return improvements_text.split(",")  # 쉼표로 구분된 개선사항 목록 반환
        except Exception as e:
            print(f"개선사항 생성 중 오류 발생: {str(e)}")
            return None

class QwenAPI:
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://api-inference.huggingface.co/v1/",
            api_key=api_key
        )
        
    def make_request(self, prompt, retries=3):
        """단일 API 요청 수행"""
        for attempt in range(retries):
            try:
                messages = [
                    {"role": "system", "content": QWEN_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
                
                stream = self.client.chat.completions.create(
                    model="Qwen/Qwen2.5-Coder-32B-Instruct",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=4000,
                    top_p=0.7,
                    stream=True
                )
                
                full_response = ""
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        print(content, end='', flush=True)
                
                return full_response.strip()
                
            except Exception as e:
                print(f"\n시도 {attempt + 1} 실패: {str(e)}")
                if attempt < retries - 1:
                    print("5초 후 재시도...")
                    import time
                    time.sleep(5)
                else:
                    print("모든 재시도 실패")
                    return None
        return None

    def request_code_improvements(self, code, improvements, iteration):
        """코드 개선을 위한 API 요청"""
        prompt = f"""
        개선된 코드만 제공해주세요. 개선된 코드는 당장 실행가능한 형태여야 하며 다른 설명이나 주석은 필요하지 않습니다.
        
        현재 코드:
        {code}
        
        현재 개선점:
        {improvements}
        
        (개선 iteration {iteration}/3)
        """
        return self.make_request(prompt)
        
    def request_explanation(self, code, prev_explanation):
        """설명 생성을 위한 API 요청"""
        prompt = f"""
        다음 코드에 대한 설명을 작성해주세요.
        
        코드:
        {code}
        
        이전 설명:
        {prev_explanation}
        """
        return self.make_request(prompt)
        
    def request_improvements_list(self, code, prev_improvements):
        """개선사항 목록 생성을 위한 API 요청"""
        prompt = f"""
        다음 코드에 대한 추가 개선사항을 제안해주세요.
        
        코드:
        {code}
        
        이전 개선점:
        {prev_improvements}
        
        개선 제안사항들을 쉼표로 구분하여 리스트 형태로 제공해주세요.
        """
        return self.make_request(prompt)

# 수정된 get_claude_response 함수
def get_claude_response(api_key, prompt):
    """개별 API 호출을 통해 코드, 설명, 개선사항을 얻습니다."""
    claude = ClaudeAPI(api_key)
    
    print("\nClaude가 코드를 생성하는 중...")
    code = claude.request_code(f'{prompt}에 대해 무조건 실행 가능한 형태의 코드만을 출력해주세요.')
    if not code:
        return None
        
    print("\nClaude가 설명을 생성하는 중...")
    explanation = claude.request_explanation(f'{prompt}에 대한 설명을 제시해주세요')
    if not explanation:
        return None
        
    print("\nClaude가 개선사항을 생성하는 중...")
    improvements = claude.request_improvements(f'{prompt}에 대해 예상가능한 오류에 대해 언급하거나 이외의 추가되면 좋을 만한 개선사항을 알려주세요.')
    if not improvements:
        return None
        
    return {
        "code": code,
        "explanation": explanation,
        "improvements": improvements
    }

# 수정된 get_qwen_improvements 함수
def get_qwen_improvements(hf_token, code_info, iteration):
    """개별 API 호출을 통해 코드 개선, 설명, 개선사항을 얻습니다."""
    qwen = QwenAPI(hf_token)
    
    print(f"\nQwen이 {iteration}차 코드 개선을 진행하는 중...")
    improved_code = qwen.request_code_improvements(
        code_info["code"],
        code_info["improvements"],
        iteration
    )
    if not improved_code:
        return None
        
    print(f"\nQwen이 {iteration}차 설명을 생성하는 중...")
    new_explanation = qwen.request_explanation(
        improved_code,
        code_info["explanation"]
    )
    if not new_explanation:
        return None
        
    print(f"\nQwen이 {iteration}차 개선사항을 생성하는 중...")
    improvements_text = qwen.request_improvements_list(
        improved_code,
        code_info["improvements"]
    )
    if not improvements_text:
        return None
        
    # improvements를 리스트로 변환
    improvements_list = [
        imp.strip() 
        for imp in improvements_text.split(',') 
        if imp.strip()
    ]
    
    return {
        "code": improved_code,
        "explanation": new_explanation,
        "improvements": improvements_list
    }

def ask_qwen(hf_token, user_request, retries=3):
    """Qwen 모델을 사용하여 요청에 대한 코드를 생성합니다."""
    client = OpenAI(
        base_url="https://api-inference.huggingface.co/v1/",
        api_key=hf_token
    )
    system_prompt = "You are an expert in creating React-based scientific simulations using JavaScript libraries."
    
    prompt = f'''I want to create a simulation of {user_request}. Analyze the scientific concepts and implementation approach, then provide the implementation code.

Core Requirements:
- React functional components with hooks
- Real-time physics calculations and visualizations
- Interactive parameter controls
- Visual feedback and animations

Focus Areas:
1. Scientific Concepts
- Core physics/math principles
- Key variables and parameters
- Required calculations

2. Technical Implementation
- Visualization approach using available libraries
- State management with React hooks
- Animation and rendering logic
- Performance optimization

3. User Interface
- Parameter control components
- Visual feedback elements
- Responsive layout design

Available Libraries (Already Installed):
- Three.js with React Three Fiber: 3D graphics/WebGL
- P5.js with react-p5: 2D creative coding
- D3.js: Data visualization
- Matter.js: 2D physics engine
- Chart.js with react-chartjs-2: Interactive charts
- Paper.js: Vector graphics

Implementation Requirements:
1. Use React functional components and hooks (useState, useEffect, useRef)
2. Implement real-time calculations and updates
3. Create interactive controls for parameters
4. Add appropriate visual feedback
5. Ensure responsive layout
6. Add error handling for calculations
7. Include performance optimizations where needed

Please provide:
1. Initial analysis of the simulation requirements
2. Recommended library choice with justification
3. Component structure overview
4. Complete implementation code with comments
5. Any necessary setup or configuration notes

The code should be production-ready and include:
- Error handling
- Performance optimizations
- Responsive design considerations
- Clear commenting and documentation
'''
    for attempt in range(retries):
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            stream = client.chat.completions.create(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=messages,
                temperature=0.5,
                max_tokens=4000,
                top_p=0.7,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    print(content, end='', flush=True)
            
            return full_response.strip()
            
        except Exception as e:
            print(f"\n시도 {attempt + 1} 실패: {str(e)}")
            if attempt < retries - 1:
                print("5초 후 재시도...")
                import time
                time.sleep(5)
            else:
                print("모든 재시도 실패")
                return None
    return None

def save_results(code_info, base_filename):
    """결과물을 파일로 저장합니다."""
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 코드 추출 및 처리
    if isinstance(code_info, dict):
        code = code_info.get('code', '')
    elif isinstance(code_info, str):
        # JSON string으로 전달된 경우
        try:
            code_dict = json.loads(code_info)
            code = code_dict.get('code', '')
        except json.JSONDecodeError:
            code = code_info  # JSON이 아닌 경우 그대로 사용
    else:
        print("지원되지 않는 code_info 형식입니다.")
        return False
    
    # JSON 이스케이프 문자 제거
    code = code.replace('\\n', '\n')
    code = code.replace('\\t', '\t')
    code = code.replace('\\"', '"')
    code = code.replace('\\\\', '\\')
    
    # 코드가 따옴표로 둘러싸여 있다면 제거
    if code.startswith('"') and code.endswith('"'):
        code = code[1:-1]
    
    code_filename = os.path.join(results_dir, f"{base_filename}_{timestamp}.js")
    try:
        with open(code_filename, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"코드가 {code_filename}에 저장되었습니다.")
    except Exception as e:
        print(f"코드 파일 저장 중 오류 발생: {str(e)}")
        return False
    
def create_error_fix_prompts(code_info, error_message):
    """오류 수정을 위한 프롬프트들을 생성합니다."""
    return {
        "code_prompt": f"""Fix the following React component error:
Error:
{error_message}
Current Code:
{code_info['code']}
Requirements:

Provide only working React component code
Use functional components with hooks
Include proper error handling
Maintain scientific accuracy
Preserve existing functionality

Explain changes concisely. List improvements comma-separated."""
    }