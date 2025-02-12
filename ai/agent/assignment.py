from llama_index.core import SimpleDirectoryReader
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from ai.agent.agent import AiReviewInfo



prompt_template_str = """\
            please response in Chinese. \
            You are a talented teacher who diligently reviews students' homework every day, \
            providing a comprehensive summary and offering constructive suggestion to help them improve their scores in the curriculum. \
            please ignore the red charaters in pictures. \
            here is a json exmaple that is the data item you will use for each problem review\
            {
                "no": "", 
                "problem" "",
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
            problem: 是题目的内容 
            ans_student, 指学生的答案, 一般情况下，学生答案为手写字体，在识别过程中需要注意其准确性
            an_ai, 是你给出的答案.
            conlusion,判断学生的答案是否正确，取值范围为(0, 1, -1), 0表示学生未作答，或你也无法判断是否正确， 1表示正确，-1表示错误.
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

class AssignmentAgent:
    """send images to ai for reviewing student's assignments."""
    
    def __init__(self, llm) -> None:
        self.llm = llm

    def check_assignments_gemini(self, directory : str) -> AiReviewInfo:
        # read files from directory
        images = SimpleDirectoryReader(directory).load_data()
        if images is None or len(images) == 0: 
            return
        
        
        mm_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(AiReviewInfo),
            image_documents=images,
            prompt_template_str=prompt_template_str,
            multi_modal_llm=self.llm,
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

