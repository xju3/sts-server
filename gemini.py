import os
from ai.llm.gemini import GeminiLLM, GeminiModel
from ai.agent.assignment import AssignmentAgent


if __name__ == '__main__':
    llm = GeminiLLM(GeminiModel.GEMINI_2_0_FLASH)
    agent = AssignmentAgent(llm.gemini)
    agent.check_assignments_gemini('/Users/tju/Workspace/projects/sts/server/files/uploads')