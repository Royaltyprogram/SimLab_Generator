import json
import os
from datetime import datetime
from api_calls import ClaudeAPI, QwenAPI, ask_qwen, create_error_fix_prompts, get_claude_response, get_qwen_improvements, save_results

def create_markdown_log(base_filename):
	"""시뮬레이션 생성 과정의 로그를 마크다운 파일로 생성합니다."""
	results_dir = "results"
	if not os.path.exists(results_dir):
		os.makedirs(results_dir)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	md_filename = os.path.join(results_dir, f"{base_filename}_{timestamp}.md")
	
	class MarkdownLogger:
		def __init__(self, filename):
			self.filename = filename
			self.sections = []
			self.current_section = []
			
		def add_section(self, title, content, level=2):
			"""새로운 섹션을 추가합니다."""
			section = f"\n{'#' * level} {title}\n\n{content}\n"
			self.sections.append(section)
			
		def add_code_block(self, code, language="javascript"):
			"""코드 블록을 추가합니다."""
			self.sections.append(f"\n```{language}\n{code}\n```\n")
			
		def add_api_response(self, title, response, is_code=False):
			"""API 응답을 추가합니다."""
			if is_code:
				self.add_section(title, "")
				self.add_code_block(response)
			else:
				self.add_section(title, response)
				
		def save(self):
			"""마크다운 파일을 저장합니다."""
			with open(self.filename, 'w', encoding='utf-8') as f:
				# 헤더 추가
				f.write(f"# 시뮬레이션 생성 로그 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
				# 모든 섹션 작성
				for section in self.sections:
					f.write(section)
			print(f"로그가 {self.filename}에 저장되었습니다.")
	
	return MarkdownLogger(md_filename)

def main():
	print("=== AI 기반 과학 시뮬레이션 코드 생성기 ===")
	print("\n예시 요청:")
	print("- 단진자 운동 시뮬레이션 (진자의 길이와 초기각을 조절 가능)")
	print("- 이상기체 상태방정식 시뮬레이션 (압력, 부피, 온도 관계 시각화)")
	print("- 포물선 운동 시뮬레이션 (초기 속도와 각도 조절 가능)")
	# API 토큰 로드
	with open("gravity_simul/api_keys.json") as f:
		api_keys = json.load(f)
		claude_api_key = api_keys["claude_api_key"]
		qwen_api_key = api_keys["hf_token"]
	while True:
		print("\n원하는 시뮬레이션을 설명해주세요 (종료하려면 'q' 입력)")
		user_request = input(">>> ").strip()
		
		if user_request.lower() == 'q':
			print("프로그램을 종료합니다.")
			break
			
		if not user_request:
			print("올바른 시뮬레이션 설명을 입력해주세요!")
			continue
		
		# 마크다운 로거 생성
		logger = create_markdown_log(f"simulation_{user_request[:30]}")
		logger.add_section("사용자 요청", user_request, level=2)
		
		# API 호출
		claude_api = ClaudeAPI(claude_api_key)
		qwen_api = QwenAPI(qwen_api_key)
		
		# step 1: qwen의 사전조사
		logger.add_section("Qwen의 사전조사", "")
		research = ask_qwen(qwen_api_key, f'{user_request}에 대해 사전조사를 진행하고 이 개념을 시뮬레이션을 하기 위한 계획을 세워줘. 어떤 라이브러리를 어떻게 활용해서 어떤 시뮬레이션을 만들 지 알려줘. 코드 작성은 하지마.')
		logger.add_api_response("Qwen의 사전조사", research)
		
		# step 2: claude의 시뮬레이션 코드 초안 생성
		logger.add_section("Claude의 시뮬레이션 코드 초안 생성", "")
		claude_response = get_claude_response(claude_api_key, user_request)
		# return {
		#     "code": code,
		#     "explanation": explanation,
		#     "improvements": improvements
		# }
		logger.add_api_response(f"claude의 시뮬레이션 초안생성 (코드)", claude_response['code'], is_code=True)
		logger.add_api_response(f"claude의 시뮬레이션 초안생성 (설명)", claude_response['explanation'])
		logger.add_api_response(f"claude의 시뮬레이션 초안생성 (개선사항)", claude_response['improvements'])
		
		# step 3: qwen의 시뮬레이션 구체화
		logger.add_section("Qwen의 시뮬레이션 구체화", "")
		for i in range(1, 4):           
			qwen_response = get_qwen_improvements(qwen_api_key, code_info=claude_response, iteration=i)
			logger.add_api_response(f"Qwen의 시뮬레이션 구체화 (코드)(반복 {i})", qwen_response['code'], is_code=True)
			logger.add_api_response(f"Qwen의 시뮬레이션 구체화 (설명)(반복 {i})", qwen_response['explanation'])
			logger.add_api_response(f"Qwen의 시뮬레이션 구체화 (개선사항)(반복 {i})", qwen_response['improvements'])
		
		# step 4: claude의 최종점검
		logger.add_section("Claude의 최종점검", "")
		prompt = f'{qwen_response} 이 코드에 대한 최종 점검해. 이 코드에서 오류 발생이 예상되는 부분을 수정해.'
		claude_final = get_claude_response(claude_api_key, prompt)
		logger.add_api_response(f"claude의 시뮬레이션 초안생성 (코드)", claude_final['code'], is_code=True)
		logger.add_api_response(f"claude의 시뮬레이션 초안생성 (설명)", claude_final['explanation'])
		logger.add_api_response(f"claude의 시뮬레이션 초안생성 (개선사항)", claude_final['improvements'])

		while True:
			save_option = input("\n결과물을 저장하시겠습니까? (y/n): ").strip().lower()
			if save_option in ['y', 'n']:
				if save_option == 'y':
					base_filename = input("저장할 파일의 기본 이름을 입력하세요: ").strip()
					if base_filename:
						save_results(claude_final, base_filename)
						
				# 오류 입력 및 수정 프로세스
				while True:
					error_check = input("\n코드 실행 중 오류가 발생했나요? (y/n): ").strip().lower()
					if error_check == 'n':
						break
					elif error_check == 'y':
						print("\n발생한 오류 내용을 입력해주세요 (여러 줄 입력 가능, 입력 완료 시 빈 줄에서 Enter):")
						error_lines = []
						while True:
							line = input()
							if not line:
								break
							error_lines.append(line)
						error_message = "\n".join(error_lines)
						logger.add_section("실행 중 발생한 오류", error_message)
						
						# Claude에게 오류 수정 요청
						print("\nClaude에게 오류 수정을 요청합니다...")
						fix_result = get_claude_response(claude_api_key, create_error_fix_prompts(claude_final, error_message))
						
						if fix_result:
							claude_final = fix_result
							print("\n=== 오류 수정 결과 ===")
							print("\n[수정된 코드]")
							print(claude_final["code"])
							print("\n[수정 설명]")
							print(claude_final["explanation"])
							if "fix_notes" in claude_final:
								print("\n[수정 내용]")
								print(claude_final["improvements"])
							
							logger.add_section("오류 수정 결과", "")
							logger.add_code_block(claude_final["code"])
							logger.add_section("수정 설명", claude_final["explanation"])
							if "fix_notes" in claude_final:
								logger.add_section("수정 내용", claude_final["improvements"])
							
							# 수정된 코드 저장
							save_option = input("\n수정된 코드를 저장하시겠습니까? (y/n): ").strip().lower()
							if save_option == 'y':
								new_filename = f"{base_filename}_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
								save_results(claude_final, new_filename)
						else:
							print("오류 수정에 실패했습니다.")
							logger.add_section("오류", "Claude를 통한 오류 수정 실패")
					else:
						print("'y' 또는 'n'을 입력해주세요.")
				break
			else:
				print("'y' 또는 'n'을 입력해주세요.")
		logger.save()
if __name__ == "__main__":
	main()
