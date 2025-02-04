here is a json exmaple that is the data item you will use for each problem review.

{
    "no": "", 
    "ans_student": "",
    "ans_ai": "",
    "conclusion": "", 
    "reason": "", 
    "knowledges": "",
    "solution": "",
    "suggestions": ""
}

For each item, You should extract the question number into a no field and the student's response into a ans_student field in JSON format. provide your response as ans_ai in JSON format.

You should also concisely list the key knowledge points related to the problem in a knowledges field in JSON format.

the data type of conclusion field is a digital number used for indicating student's answer is correct or incorrect, you can set the value to 0 first.

You must also confirm whether the student's answer is correct, if student's answer is correct, the value would be 1, if student's answer is incorrect, the value would be -1.

Sometimes the answer should also conform to common sense and be evaluated based on actual conditions. For example, if you fill in the question "How many times does a person's heart beat per minute?", and the options are 10, 65, and 300, the closest answer should be 60, which cannot be 10 or 300.

Sometimes, AI needs to give an answer that conforms to common sense based on the meaning of the question.

If the student’s answer is incorrect, you need to analyze the possible reasons behind the wrong answer, and include this in a reason field in JSON format.  Next, provide the correct approach to solve the problem in a solution field in JSON format.  Finally, give your suggestions for improvement in a suggestions field in JSON format.

There are multiple pictures to review at once. The file name of each picture corresponds to the order of the homework content, so please check them sequentially. The answer to a single question may be spread across two pictures.

You need to provide a summary of your review, finally, you will return the results as following format. 
{
    "summary": "",
    "problems": []
}

please response in Chinese.