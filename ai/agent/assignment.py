from llama_index.core import SimpleDirectoryReader
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.llms.gemini import Gemini
from llama_index.core.output_parsers import PydanticOutputParser
from ai.agent.agent import AiReviewInfo
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core import PromptTemplate


prompt_template_review = """\
            please response in Chinese. \
            You are a talented teacher who diligently reviews students' homework every day, \
            providing a comprehensive summary and offering constructive suggestion to help them improve their scores in the curriculum. \
            please ignore the red charaters in pictures. \
            here is a json exmaple that is the data item you will use for each problem review\
            {
                "no": "", 
                "question": "",
                "options": [],
                "ans_student": "",
                "ans_ai": "",
                "conclusion": "", 
                "reason": "", 
                "knowledge": "",
                "solution": "",
                "suggestion": "",
                "level": 1
            }\
            no, 是指题目的编号
            question: 题目的内容
            options: 如果是选择题目，需要将题目中提供可选项加到options中
            ans_student, 指学生的答案, 一般情况下，学生答案为手写字体，在识别过程中需要注意其准确性
            conlusion:
                判断学生的答案是否正确，取值范围为(0, 1, -1), 0表示学生未作答，或你也无法判断是否正确， 1表示正确，-1表示错误.
                在遇到选择题时，你需要了解答案代号，如A,B,C,D所代表的含义,后再作正确与否判断
                学生的答案为手写字体，请仔细识别其内容，特别是对于最终答案的判断，如有些学生将最终答案写在"答"后面.
            an_ai, 是你给出的答案.
            reason，若学生答案错误，需要分析错误产生的原因
            knowlege: 指本题涉及到的知识点，如果有多个知识点，用逗号隔开
            solution: 你的详细解题过程，如果有推导过程，需要一步一步地推导出答案, 注意根据需要增加换行符
            suggestion: 若学生作答错误，需要提醒学生的一些注意事项
            level: 指题目难度，注意这个难度只是针对此其知识点构建的题目产生的难度，通常这些知识点会对应一定的年级，如小学3年级，中学8年级(初中2年级)前

            有时候你会遇到没有标准答案的实践性问题，如一个一分钟可以步行多远，如果答案是10公里，明显不太可能，所以在分析此类问题答案时，需要结合生活，工作中的实际情况，用客观合理的答案去判断学生作答正确与否.
            {
                "subject": "",
                "summary": "",
                "startTime": "",
                "endTime": "",
                "problems": []
            } 
            startTime: 是你开始思考时间，要精确到秒
            endTime: 是你完成思考时间,要精确到秒
            summary: 你对本次作业完成情况的总结， 总结需要结合每道题目是否正确与建议，如果所有题目都对，不应该给出任何负面的总结.
            subject: 指作业所属哪个科目，如语文，数学，历史，地理，政治，英语，物理，化学
            problems: 是每一道题经过你检查后产生的数据列表
        """


prompt_template_assignment = """\
    您是一位{grade}年级{subject}老师，\
        您给学生布置的家庭作业中，某个学生在这些{knowledge_points}知识点上出了错，\
        你需要生成与出错知识点两倍数量的练习题，供此学生巩固他们还没有掌握的知识, 要求如下: \
    1. 至少包含两个出错知识点 \
    2. 题目为选择题，提供4个答案，只有一个答案是正确的, 这个选项合并成一个字符串，中间用Comma与换行符隔开 \
    3. 如果是科学类的学科，题目的内容需要以现实生活中的{subject}现象为基础 \
       3.1. 题目难度分三级: 简单、中等与困难 \
       3.2. 简单的题目通常不需要多步骤的计算 \
       3.2. 中等难度题目需要学生进行2-3步的步骤计算 \
       3.4. 困难等级的题目通常需要3步以上的计算步骤 \
       3.5. 简单与困难的题目各占20%， 剩下的为中等难度题目
    4. 如果是文科类的题目，目前我没有明确的规则，具体内容由你决定. \
    5. 以下面Json格式输出:
    {
        "no": 题目编号
        "question": 问题
        "options" : 答案选项
        "level" : 题目难度
        "solution": 解题说明
        "points": 本题目用到的知识点，返回用逗号(comma)隔开的字串
        "ans" 答案，只需要你提供的答案选项的代号, 如A
     }
     6. 结果不需要markdown样式，直接是json数据
     7. Reponse in Chinese
"""
class AssignmentAgent:

    def gen_assignment(self, llm: Gemini, grade, subject, points):
        template = PromptTemplate(prompt_template_assignment)
        prompt = template.format(grade=grade, subject=subject,knowledge_points=points)
        return llm.complete(prompt=prompt)

    def check_assignments_gemini(self, llm :GeminiMultiModal,  directory : str) -> AiReviewInfo:
        """
            功能: 检查学生作业
        """
        # read files from directory
        images = SimpleDirectoryReader(directory).load_data()
        if images is None or len(images) == 0: 
            return
        
        mm_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(AiReviewInfo),
            image_documents=images,
            prompt_template_str=prompt_template_review,
            multi_modal_llm=llm,
            verbose=True,
        )

        agent_review_info = mm_program()
        problems = agent_review_info.problems

        total = len(problems)
        if total == 0:
            return

        correct = len(list(filter(lambda x: x.conclusion == 1, problems)))
        incorrect = len(list(filter(lambda x: x.conclusion == -1, problems)))
        uncertain = len(list(filter(lambda x: x.conclusion == 0, problems)))
        agent_review_info.correct = correct
        agent_review_info.total = total
        agent_review_info.incorrect = incorrect
        agent_review_info.uncertain = uncertain
        print(f'{total}, {agent_review_info.correct}, {agent_review_info.incorrect}, {agent_review_info.uncertain}')
        return agent_review_info
        # socket_client.send_assignment_review_message(ticket_id=request_id, review_info=review_info)

