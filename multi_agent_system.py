# multi_agent_system.py

import random
from typing import List, Dict
import json

# -------------------------
# 模拟代码库数据
# -------------------------
CODEBASE = [
    {"file": "user.py", "content": "def login(): pass"},
    {"file": "order.py", "content": "def create_order(): pass"},
    {"file": "payment.py", "content": "def pay(): pass"},
    {"file": "product.py", "content": "def add_product(): pass"}
]

# -------------------------
# Base Agent 类
# -------------------------
class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.token_consumed = 0  # 模拟 Token 消耗

    def consume_token(self, amount: int):
        self.token_consumed += amount

# -------------------------
# 代码审查 Agent
# -------------------------
class CodeReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("CodeReviewAgent")

    def review(self, code: Dict) -> str:
        self.consume_token(random.randint(50, 150))
        issues = ["None", "Minor style issue", "Missing docstring", "Potential bug"]
        issue = random.choice(issues)
        return f"File: {code['file']} - Review: {issue}"

# -------------------------
# 自动测试 Agent
# -------------------------
class TestAgent(BaseAgent):
    def __init__(self):
        super().__init__("TestAgent")

    def generate_tests(self, code: Dict) -> str:
        self.consume_token(random.randint(30, 80))
        return f"Generated tests for {code['file']}"

    def run_tests(self, code: Dict) -> str:
        self.consume_token(random.randint(20, 100))
        result = random.choice(["PASS", "FAIL"])
        return f"Test result for {code['file']}: {result}"

# -------------------------
# 文档生成 Agent
# -------------------------
class DocAgent(BaseAgent):
    def __init__(self):
        super().__init__("DocAgent")

    def generate_doc(self, code: Dict) -> str:
        self.consume_token(random.randint(40, 120))
        return f"Auto-doc for {code['file']}: Function overview."

# -------------------------
# 多 Agent 协作调度器
# -------------------------
class AgentOrchestrator:
    def __init__(self, codebase: List[Dict]):
        self.codebase = codebase
        self.review_agent = CodeReviewAgent()
        self.test_agent = TestAgent()
        self.doc_agent = DocAgent()
        self.total_token = 0

    def run_pipeline(self):
        reports = []
        for code in self.codebase:
            # 多 Agent 协作处理
            review = self.review_agent.review(code)
            test_script = self.test_agent.generate_tests(code)
            test_result = self.test_agent.run_tests(code)
            doc = self.doc_agent.generate_doc(code)

            # 汇总单文件报告
            report = {
                "file": code["file"],
                "review": review,
                "test_script": test_script,
                "test_result": test_result,
                "doc": doc
            }
            reports.append(report)

        # 计算总 Token 消耗
        self.total_token = (
            self.review_agent.token_consumed +
            self.test_agent.token_consumed +
            self.doc_agent.token_consumed
        )
        return reports

    def generate_summary(self):
        summary = {
            "agents": {
                "CodeReviewAgent": self.review_agent.token_consumed,
                "TestAgent": self.test_agent.token_consumed,
                "DocAgent": self.doc_agent.token_consumed
            },
            "total_token": self.total_token,
            "files_processed": len(self.codebase)
        }
        return summary

# -------------------------
# 主程序
# -------------------------
if __name__ == "__main__":
    orchestrator = AgentOrchestrator(CODEBASE)
    reports = orchestrator.run_pipeline()
    summary = orchestrator.generate_summary()

    print("=== Pipeline Reports ===")
    for report in reports:
        print(json.dumps(report, indent=2))

    print("\n=== Summary ===")
    print(json.dumps(summary, indent=2))
