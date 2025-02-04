
from llama_index.core import SimpleDirectoryReader
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from model.agent import AssignmentChecking

class AssignmentAgent:

    
    def __init__(self, llm) -> None:
        self.llm = llm

    def check_assignments(self, directory):
        images = SimpleDirectoryReader(directory).load_data()
        print(len(images))
        if len(images) == 0: 
            return

        # prompt_template_str = """\
        #     here is a json exmaple that is the data item you will use for each problem review\
        #     {
        #     "no": "", 
        #     "ans_student": "",
        #     "ans_ai": "",
        #     "conclusion": "", 
        #     "reason": "", 
        #     "knowledges": "",
        #     "solution": "",
        #     "suggestions": ""
        #     }\

        #     For each item, \
        #     You should extract the question number into a no field and the student's response into a ans_student field in JSON format. provide your response as ans_ai in JSON format. \
        #     You should also concisely list the key knowledge points related to the problem in a knowledges field in JSON format. \
        #     the data type of conclusion field is a digital number used for indicating student's answer is correct or incorrect, you can set the value to 0 first, \
        #     You must also confirm whether the student's answer is correct, \
        #     if student's answer is correct, the value would be 1, \
        #     if student's answer is incorrect, the value would be -1, \
        #     Sometimes the answer should also conform to common sense and be evaluated based on actual conditions. \
        #         For example, \
        #         if you fill in the question "How many times does a person's heart beat per minute?", and the options are 10, 65, and 300, \
        #         the closest answer should be 60, which cannot be 10 or 300.\
        #         Sometimes, AI needs to give an answer that conforms to common sense based on the meaning of the question. \

        #     If the student’s answer is incorrect, \
        #         you need to analyze the possible reasons behind the wrong answer, and include this in a reason field in JSON format. 
        #         Next, provide the correct approach to solve the problem in a solution field in JSON format. \
        #         Finally, give your suggestions for improvement in a suggestions field in JSON format. \

        #     There are multiple pictures to review at once. \
        #     The file name of each picture corresponds to the order of the homework content, so please check them sequentially. \
        #     The answer to a single question may be spread across two pictures.
        #     You need to provide a summary of your review, \
        #     finally, you will return the results as following format. \ 
        #     {
        #         "summary": "",
        #         "problems": []
        #     } \
        #     please response in Chinese. \
        # """

        prompt_template_str = """\
            You are a talented teacher who diligently reviews students' homework every day, \
            providing a comprehensive summary and offering constructive suggestions to help them improve their scores in the curriculum. \

            here is a json exmaple that is the data item you will use for each problem review\
            {
                "no": "", 
                "ans_student": "",
                "ans_ai": "",
                "conclusion": "", 
                "reason": "", 
                "knowledges": "",
                "solution": "",
                "suggestions": ""
            }\

            For each item, \
            You should extract the question number into a no field and the student's response into a ans_student field in JSON format, \
            You should also concisely list the key knowledge points related to the problem in a knowledges field in JSON format. \
            after you read each problem carefully, \
            you must give your answer based on the meaning of the question, \
            which conforms to common sense in a ans_ai field in JSON format, don't try to copy the student's answer.\
            Sometimes both of you and student's answers should also conform to common sense and be evaluated based on real life situations. \
                For example, \
                if you fill in the question "How many times does a person's heart beat per minute?", and the options are 10, 80, and 300, \
                the closest answer should be 80, which cannot be 10 or 300.\
            if the student's answer has contradicts against the common sense or real life situations, you must point it out in the reason field in JSON. \
            You must also check whether the student's answer is correct or incorrect, and make a conclusion. \
            
            the data type of conclusion field is a digital number used for indicating student's answer is correct or incorrect, \
            you can set it's value to 0 first, \
            if student's answer is correct, the value would be 1, \
            if student's answer is incorrect, the value would be -1, \
                        If the student’s answer is incorrect, \
                you need to analyze the possible reasons behind the wrong answer, and include this in a reason field in JSON format. 
                Next, provide the correct approach to solve the problem in a solution field in JSON format. \
                Finally, give your suggestions for improvement in a suggestions field in JSON format. \

            There are multiple pictures to review at once. \
            The file name of each picture corresponds to the order of the homework content, so please check them sequentially. \
            The answer to a single question may be spread across two pictures.
            You need to provide a summary of your review, \
            finally, you will return the results as following format. \ 
            {
                "summary": "",
                "problems": []
            } \
            please response in Chinese. \
        """

        mm_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(AssignmentChecking),
            image_documents=images,
            prompt_template_str=prompt_template_str,
            multi_modal_llm=self.llm,
            verbose=True,
        )
        review =  mm_program()
        problems = review.problems

        total = len(problems)
        if total > 0:
            correct = len(list(filter(lambda x: x.conclusion == 1, problems)))
            incorrect = len(list(filter(lambda x: x.conclusion == -1, problems)))
            uncertain = len(list(filter(lambda x: x.conclusion == 0, problems)))
            review.correct = correct
            review.total = total
            review.incorrect = incorrect
            review.uncertain = uncertain
        print(f'{total}, {review.correct}, {review.incorrect}, {review.uncertain}')
        return review

