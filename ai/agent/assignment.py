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
            if the content in the pictures has no student homework, plear just return an empty value \
            here is a json exmaple that is the data item you will use for each problem review\
            {
                "no": "", 
                "question": "",
                "chart": "",
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
            no, 是指题目的编号, 
            question: 及其说明\
                1. question是指题目的内容. \
                2. 题目边上的图有两个作用， \
                    2.1. 补充题目内容，即题目的部分内容是通过图进行描述的， 
                    2.2. 对题目的内容进一步说明，\
                    2.3. 如果是第一种情况，在解题过程一中需要结合图的题目才完整. \
                    2.4. 示例，题目中提到了茄子，图片中正好也有对茄子的描述，那么此图应该与此题目关联。
                3. 题干中通常就包含了多个问题，以括号的形式进行提问，或者留有空格供填空 \
            chart: 若有关联图，请用TikZ描述图的内容，若无关联图，则将值设为'无' \
            options: 如果是选择题目,需要将题目中提供可选项加到options中 \
            ans_student: \
                1. 指学生的答案 \
                2. 对于填空题或选择题，通常答案包含在括号内. \
                3. 简答题需要学生写出多个演算步骤，其答案可能散落在非即定位置，需要根据学生的计算过程去查找，
                4. 学生的答案为手写字体，请仔细识别其内容，特别是对于最终答案的判断，如有些学生将最终答案写在"答"后面.\
            reason:
                1. 若学生答案错误,需要分析错误产生的简单原因,如计算错误,概念不清 \
            knowlege: 指本题涉及到的知识点，如果有多个知识点，用英文逗号(comma)隔开
            solution: 
                1. 你的详细解题过程，如果有推导过程，需要一步一步地推导出答案, 注意根据需要增加换行符 \
                2. 有时候你会遇到没有标准答案的实践性问题，\
                3. 如一个一分钟可以步行多远, 如果答案是10公里, 明显不太可能, \
                4. 所以在分析此类问题答案时，需要结合生活，工作中的实际情况，用客观合理的答案去判断学生作答正确与否. \
            an_ai, 通过你的详细解题过程计算后，得到的答案，此答案需要与你的解题结果完全一致. \
            conlusion: \
                1. 判断学生的答案是否正确，取值范围为(0, 1, -1), 0表示学生未作答,或你也无法判断是否正确， 1表示正确,-1表示错误. \
                2. 在遇到选择题时, 你需要了解答案代号, 如A,B,C,D所代表的含义,后再作正确与否判断 \
            suggestion: 若学生作答错误，需要提醒学生的一些注意事项 \
            level: \
                1. 指题目难度，\
                2. 注意这个难度只是针对此其知识点构建的题目产生的难度 \
                3. 通常这些知识点会对应一定的年级,如小学3年级,中学8年级(初中2年级) \
            最后，你需要对本次作业进行总结,json格式如下: \
            {
                "subject": "",
                "summary": "",
                "startTime": "",
                "endTime": "",
                "problems": [],
                "total": 0,
                "correct": 0,
                "incorrect": 0,
                "uncertain": 0,
            } \
            subject: 指作业所属哪个科目，如语文，数学，历史，地理，政治，英语，物理，化学
            summary: 你对本次作业完成情况的总结， 总结需要结合每道题目是否正确与建议，如果所有题目都对，不应该给出任何负面的总结.
            problems: 检查后产生题目列表
            startTime: 是你开始思考时间，要精确到秒
            endTime: 是你完成思考时间,要精确到秒,
            total: 指题目总数
            correct: 答对的题目总数
            incorrect: 答错的题目总数
            uncertain: 未作答的题目总数
        """


prompt_template_assignment = """\
    知识点列表: {knowledge_points}
    您是一位{grade}年级{subject}老师，\
        您给学生布置的家庭作业中，某个学生在这些知识点上出了错，\
        你需要生成与出错知识点两倍数量的练习题，供此学生巩固他们还没有掌握的知识,要求如下: \
    1. 题目为选择题,提供4个答案,只有一个答案是正确的, 这个选项合并成一个字符串,中间用Comma与换行符隔开 \
    2. 如果是科学类的学科，题目的内容需要以现实生活中的{subject}现象为基础 \
       2.1. 题目难度分三级: 简单、中等与困难 \
       2.2. 简单只包含一个知识点，题目通常不需要多步骤的计算 \
       2.2. 如果知识点大于1个,中等难度需要包含两个知识点,需要学生进行2-3步的步骤计算 \
       2.4. 困难等级的题目可以使用大于等于2个知识点,通常需要3步以上的计算步骤 \
       2.5. 简单与困难的题目各占20%,剩下的为中等难度题目
    4. 如果是文科类的题目，目前我没有明确的规则，具体内容由你决定. \
    5. 以下面Json格式输出:
    {
        "no": 题目编号
        "question": 问题
        "options" : 答案选项
        "level" : 题目难度, easy用1表示， medium用2表示， hard用3表示
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
        prompt = template.format(grade=grade, subject=subject,knowledge_points=points.split(","))
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

