import streamlit as st
import random
import json
import operator
import sys
import re

sys.set_int_max_str_digits(10000)

# ----- CONFIG -----
subtopics = ["Introduction", "Operations", "Implementation", "Applications", "Code Tracing", "Expression Evaluation"]
levels = ["Level 1", "Level 2", "Level 3"]
question_types = ["Long Answer", "MCQ", "True/False", "One Word", "Fill in the Blanks"]

# ----- PLACEHOLDERS AND TEMPLATES -----
placeholders = {
    "topic": ["stack", "call stack", "expression stack", "execution stack"],
    "operation": ["push", "pop", "peek", "isEmpty", "isFull", "size", "clear", "traverse"],
    "model": ["queue", "array", "linked list", "tree", "graph", "deque"],
    "aspect": ["structure", "behavior", "memory usage", "efficiency", "execution time"],
    "dimension": ["performance", "complexity", "usability", "data access", "scalability"],
    "application": [
        "browser history", "undo functionality", "expression evaluation", "backtracking",
        "language parsing", "function call tracking", "XML parsing", "balanced parentheses",
        "DFS traversal", "syntax parsing"
    ],
    "scenario": ["large datasets", "multithreading", "limited memory", "real-time systems",
                 "concurrent execution", "cloud deployment", "data streaming"],
    "problem": ["overflow", "underflow", "memory leak", "data corruption", "stack crash"],
    "context": ["recursion", "system design", "low-level memory operations", "compiler design"],
    "task": ["parsing expressions", "reversing strings", "evaluating expressions", "tracking calls"],
    "alternative": ["queue", "list", "dictionary", "set", "deque"],
}

# ----- NEW QUESTION TEMPLATES -----
new_template_bank = {
    "MCQ": [
        "What is the primary function of a {topic}? \nA) {option1} \nB) {option2} \nC) {option3} \nD) {option4}",
        "Which of the following operations is NOT associated with a {topic}? \nA) {operation1} \nB) {operation2} \nC) {operation3} \nD) {operation4}",
        "In which scenario would a {topic} be most beneficial? \nA) {scenario1} \nB) {scenario2} \nC) {scenario3} \nD) {scenario4}",
        "What is the time complexity of the {operation} operation in a {topic}? \nA) O(1) \nB) O(n) \nC) O(log n) \nD) O(n^2)",
        "Which of the following best describes the behavior of a {topic}? \nA) FIFO \nB) LIFO \nC) Random \nD) Sorted",
        "What is a common use case for a {topic}? \nA) {use_case1} \nB) {use_case2} \nC) {use_case3} \nD) {use_case4}",
    ],
    "True/False": [
        "True or False: A {topic} follows the LIFO principle.",
        "True or False: The {operation} operation can be performed on an empty {topic}.",
        "True or False: A {topic} can be implemented using an array.",
        "True or False: The size of a {topic} is fixed once it is created.",
        "True or False: The {operation} operation is more efficient than {alternative_operation} in all cases.",
        "True or False: A {topic} can be used to evaluate expressions in programming languages.",
    ],
    "One Word": [
        "What is the term for the last element added to a {topic}?",
        "What is the primary data structure used to implement a {topic}?",
        "What is the term for the operation that adds an element to a {topic}?",
        "What is the term for the operation that retrieves the top element from a {topic}?",
        "What is the maximum number of elements a {topic} can hold called?",
        "What is the term for the condition when a {topic} cannot accept more elements?",
    ],
    "Fill in the Blanks": [
        "A {topic} is used to manage __________ in programming.",
        "The operation __________ is used to remove the top element from a {topic}.",
        "In a {topic}, the last element added is the first one to be removed, following the __________ principle.",
        "The __________ operation checks if a {topic} is empty.",
        "To prevent overflow, a {topic} must be checked for __________ before adding a new element.",
        "The __________ operation retrieves the top element without removing it from a {topic}.",
    ]
}

# ----- FUNCTION TO GENERATE MCQ QUESTIONS -----
def generate_mcq_questions(subtopic, count):
    templates = new_template_bank["MCQ"]
    results = []
    for _ in range(count):
        template = random.choice(templates)
        keys = set(re.findall(r'\{(\w+)\}', template))
        
        values = {}
        for key in keys:
            if key.startswith("option"):
                if "option_values" not in values:
                    values["option_values"] = random.sample(placeholders["operation"], 4)
                try:
                    index = int(key[len("option"):]) - 1
                    values[key] = values["option_values"][index]
                except (ValueError, IndexError):
                    values[key] = "{UNKNOWN_OPTION}"
            elif key.startswith("operation"):
                if "operation_values" not in values:
                    values["operation_values"] = random.sample(placeholders["operation"], 4)
                try:
                    index = int(key[len("operation"):]) - 1
                    values[key] = values["operation_values"][index]
                except (ValueError, IndexError):
                    values[key] = "{UNKNOWN_OPERATION}"
            elif key.startswith("scenario"):
                if "scenario_values" not in values:
                    values["scenario_values"] = random.sample(placeholders["scenario"], 4)
                try:
                    index = int(key[len("scenario"):]) - 1
                    values[key] = values["scenario_values"][index]
                except (ValueError, IndexError):
                    values[key] = "{UNKNOWN_SCENARIO}"
            elif key.startswith("use_case"):
                if "use_case_values" not in values:
                    values["use_case_values"] = random.sample(placeholders["application"], 4)
                try:
                    index = int(key[len("use_case"):]) - 1
                    values[key] = values["use_case_values"][index]
                except (ValueError, IndexError):
                    values[key] = "{UNKNOWN_USE_CASE}"
            else:
                if key in placeholders:
                    values[key] = random.choice(placeholders[key])
                else:
                    values[key] = "{UNKNOWN}"
        
        for k in ["option_values", "operation_values", "scenario_values", "use_case_values"]:
            if k in values:
                del values[k]

        question = template.format(**values)
        results.append({"type": "MCQ", "subtopic": subtopic, "question": question})
    return results

# ----- FUNCTION TO GENERATE TRUE/FALSE QUESTIONS -----
def generate_true_false_questions(subtopic, count):
    templates = new_template_bank["True/False"]
    results = []
    for _ in range(count):
        template = random.choice(templates)
        values = {k: random.choice(v) for k, v in placeholders.items() if f"{{{k}}}" in template}
        question = template.format(**values)
        results.append({"type": "True/False", "subtopic": subtopic, "question": question})
    return results

# ----- FUNCTION TO GENERATE ONE WORD QUESTIONS -----
def generate_one_word_questions(subtopic, count):
    templates = new_template_bank["One Word"]
    results = []
    for _ in range(count):
        template = random.choice(templates)
        values = {k: random.choice(v) for k, v in placeholders.items() if f"{{{k}}}" in template}
        question = template.format(**values)
        results.append({"type": "One Word", "subtopic": subtopic, "question": question})
    return results

# ----- FUNCTION TO GENERATE FILL IN THE BLANKS QUESTIONS -----
def generate_fill_in_the_blanks_questions(subtopic, count):
    templates = new_template_bank["Fill in the Blanks"]
    results = []
    for _ in range(count):
        template = random.choice(templates)
        values = {k: random.choice(v) for k, v in placeholders.items() if f"{{{k}}}" in template}
        question = template.format(**values)
        results.append({"type": "Fill in the Blanks", "subtopic": subtopic, "question": question})
    return results

# ----- FUNCTION TO GENERATE QUESTIONS BY TYPE -----
def generate_questions_by_type(selected_type, subtopic, level, count):
    # For code tracing, ignore question type and always generate code tracing questions
    if subtopic == "Code Tracing":
        return generate_code_tracing_questions(subtopic, level, count)

    if selected_type == "Long Answer":
        return generate_template_questions(subtopic, level, count)
    elif selected_type == "MCQ":
        return generate_mcq_questions(subtopic, count)
    elif selected_type == "True/False":
        return generate_true_false_questions(subtopic, count)
    elif selected_type == "One Word":
        return generate_one_word_questions(subtopic, count)
    elif selected_type == "Fill in the Blanks":
        return generate_fill_in_the_blanks_questions(subtopic, count)
    return []

# ----- TEMPLATE BANK -----
template_bank = {
    "Introduction": {
        "Level 1": [
            "Explain the LIFO principle in a {topic} with an example.",
            "Compare {topic} and {model} based on {dimension}.",
            "What are the limitations of a {topic} in {scenario}?",
            "How does a {topic} handle {problem} in {context}?",
            "What is the role of a {topic} in {application}?",
            "Why is the LIFO property important in {application}?",
            "Describe the evolution of {topic} structures in computing.",
            "List basic operations of a {topic} and explain their purpose.",
            "What distinguishes a {topic} from a {alternative} logically and structurally?",
            "In what way does a {topic} optimize {dimension} in applications?",
            "Describe a real-life analogy to explain {topic}.",
            "What are the types of {topic} implementations available?",
            "When should a {topic} not be used in system design?",
            "How does {problem} manifest in basic {topic} structures?",
            "Why is {model} sometimes preferred over {topic} in {scenario}?",
            "How does memory layout differ between {topic} and {alternative}?"
        ],
        "Level 2": [
            "Analyze the use of a {topic} in {application}.",
            "Critique the efficiency of a {topic} for {task}.",
            "How does a {topic} handle {problem} in {scenario}?",
            "Prove the time complexity of {operation} in a {topic}.",
            "Why is a {topic} preferred over {alternative} for {task}?",
            "Discuss the practical limitations of {topic} in multithreaded environments.",
            "Identify and analyze bottlenecks in {topic} usage.",
            "Describe failure scenarios in {application} caused by {topic} misuse.",
            "What trade-offs arise in choosing {topic} over {model} for {application}?",
            "How do changes in {dimension} affect {topic} performance?",
            "What optimizations are available for {topic} in constrained systems?",
            "Explore the behavioral differences between bounded and unbounded stacks.",
            "How does {topic} impact CPU vs memory usage in real-world applications?",
            "Compare worst-case vs average-case performance of {operation} in a {topic}.",
            "Can a {topic} simulate the behavior of a {model} in certain applications?"
        ],
        "Level 3": [
            "Design a {topic} to solve {problem} in {scenario}.",
            "Prove the correctness of {operation} in a {topic}.",
            "Analyze the space complexity of a {topic} in {context}.",
            "Critique the use of a {topic} in {application}.",
            "Derive the full implementation of a {topic} for {task}.",
            "How would you redesign a {topic} for high-frequency {operation} in {scenario}?",
            "Compare and contrast lock-based and lock-free stack implementations.",
            "Evaluate stack behavior under concurrent modifications in a multithreaded system.",
            "What changes would you make to {topic} for optimizing recursion-heavy applications?",
            "Develop a fault-tolerant {topic} implementation for mission-critical systems.",
            "Simulate stack behavior under varying memory and CPU constraints.",
            "Propose an improvement to {operation} performance in memory-limited environments.",
            "Is it possible to parallelize {operation} in a {topic}? Justify your reasoning.",
            "Redesign a {topic} to use persistent memory and analyze implications.",
            "Construct a predictive model to forecast {topic} behavior under large-scale {application}."
        ]
    },
    "Operations": {
        "Level 1": [
            "Explain how {operation} works in a {topic} with an example.",
            "When is it appropriate to use the {operation} operation in a stack?",
            "Describe a real-world application where {operation} is critical in stack usage.",
            "What happens to a stack’s state after performing a {operation}?",
            "Illustrate the {operation} operation using a simple stack and input sequence.",
            "Compare {operation} and another stack operation in terms of their effects.",
            "Describe a scenario where {operation} may result in an error.",
            "Provide a step-by-step explanation of {operation} execution on a stack with five elements.",
            "Why is {operation} fundamental to the stack’s LIFO behavior?",
            "Explain the importance of maintaining stack integrity during {operation}.",
            "What would happen if {operation} is attempted on an empty stack?",
            "How can {operation} be implemented in a stack using arrays?",
            "What is the default behavior of {operation} in most stack implementations?",
            "Can {operation} be safely executed in concurrent systems? Why or why not?",
            "What are common bugs associated with incorrect {operation} usage?"
        ],
        "Level 2": [
            "Analyze the time complexity of performing multiple {operation} operations.",
            "Discuss the importance of error handling in the {operation} operation.",
            "Evaluate the role of {operation} in recursive algorithms that use stacks.",
            "Compare the performance of {operation} in array-based vs. linked-list-based stacks.",
            "Explore edge cases when performing {operation} in dynamic stacks.",
            "How does memory allocation affect the performance of {operation} in large stacks?",
            "Demonstrate the consequences of improper synchronization during {operation} in multithreaded environments.",
            "Prove that {operation} maintains the LIFO property of the stack.",
            "Critically assess stack overflow and underflow risks in relation to {operation}.",
            "Describe a debugging strategy when {operation} fails during runtime.",
            "Why is it crucial to validate stack boundaries before executing {operation}?",
            "Design a monitoring tool to track {operation} frequency and failure rates.",
            "What happens to system performance if {operation} is called excessively without cleanup?",
            "Suggest optimizations for {operation} in high-performance computing environments.",
            "Discuss how {operation} interacts with memory in low-level languages like C/C++."
        ],
        "Level 3": [
            "Design a robust method for handling {operation} in memory-constrained environments.",
            "Implement a custom stack in your preferred language and highlight the {operation} implementation.",
            "Develop a secure stack operation module with safeguards for improper {operation} calls.",
            "Simulate {operation} using a virtual machine-like environment and analyze performance.",
            "Construct a logging system that tracks every {operation} call with timestamps.",
            "Evaluate {operation} impact in the context of a real-time processing system.",
            "How can machine learning be used to predict failures in {operation} usage?",
            "Integrate {operation} into a larger stack-based DSL and explain its semantics.",
            "Optimize the {operation} method for maximum throughput in concurrent stack architectures.",
            "Propose a caching strategy for frequently used stack elements during {operation}.",
            "How would you visualize {operation} impact on stack memory using a dashboard?",
            "Create a stress test that validates {operation} under high load conditions.",
            "Prove formal correctness of {operation} using assertions or invariants.",
            "Implement {operation} with real-time rollback features in case of failure.",
            "Design an educational animation tool to teach {operation} in data structures courses."
        ]
    },
    "Implementation": {
        "Level 1": [
            "Describe how to implement a {topic} using a {model}.",
            "Compare {topic} implementation using {model} and {alternative}.",
            "What are the key components when implementing a {topic} using an {model}?",
            "Explain the steps to implement a static {topic} using an array.",
            "How does a dynamic {topic} differ in implementation compared to a static one?",
            "Illustrate a basic implementation of a {topic} in C/C++.",
            "What are the advantages of implementing a {topic} with a linked list?",
            "How would you initialize a {topic} using an array?",
            "Write pseudocode for implementing a {topic} using a {model}.",
            "Describe error conditions in stack implementation using arrays.",
            "How do you manage overflow in a static {topic} implementation?",
            "Explain memory allocation differences between array-based and linked list {topic}s.",
            "How does index management work in array-based {topic}s?",
            "Explain how you would track the top element in a {topic} implemented with an array.",
            "How do you handle underflow in a basic {topic} implementation?"
        ],
        "Level 2": [
            "Evaluate trade-offs between array and linked list implementations of a {topic}.",
            "What are the challenges in implementing a dynamic {topic}?",
            "Analyze how pointer management works in linked list-based {topic}s.",
            "Design a {topic} implementation that supports dynamic resizing.",
            "How would you modify a static {topic} to support overflow handling?",
            "Discuss garbage collection implications for linked list {topic}s.",
            "Compare fixed-size and resizable stack implementations.",
            "Evaluate the time complexity of {operation} in a linked list vs array stack.",
            "What data structures can be used internally to implement a stack?",
            "Explain implementation differences of a {topic} in Java vs C++.",
            "Design a custom stack with minimum memory overhead.",
            "How can you implement a {topic} that supports rollback (undo feature)?",
            "Propose an implementation plan for an efficient stack for real-time systems.",
            "What are common implementation pitfalls in dynamic stack creation?",
            "How does memory fragmentation affect {topic} implemented with dynamic memory?"
        ],
        "Level 3": [
            "Implement a dynamic stack with overflow protection.",
            "Propose a memory-efficient design for {topic} implementation in {context}.",
            "Design and implement a {topic} that supports multi-threaded access.",
            "Develop a hybrid {topic} using both array and linked list.",
            "Create a stack implementation supporting additional operations like getMin().",
            "Implement a {topic} with O(1) time complexity for all operations.",
            "Design a concurrent {topic} using lock-free data structures.",
            "Write a complete implementation of a stack in a functional programming language.",
            "Create a customizable stack class supporting multiple data types.",
            "Implement a stack with logging capabilities for every operation.",
            "Build a persistent stack using file I/O for storing operations.",
            "Construct a {topic} suitable for memory-constrained embedded systems.",
            "Design a self-balancing stack for ordered data.",
            "Develop an advanced stack system with undo-redo capabilities.",
            "Write a unit-test ready stack module with mocks and stubs."
        ]
    },
    "Applications": {
        "Level 1": [
            "Explain the use of a {topic} in {application}.",
            "Why is a {topic} suitable for {application}?",
            "Describe how a {topic} is applied in {application} with an example.",
            "List real-world scenarios where a {topic} is used in {application}.",
            "What makes a {topic} ideal for handling {application}?",
            "Discuss a situation in software where {topic} is useful for {application}.",
            "How does a {topic} simplify the task of {task} in {application}?",
            "Illustrate with an example how {topic} is used in {application}.",
            "In what way does the LIFO property help in {application}?",
            "Provide an example showing {topic}'s usage in {application}.",
            "Identify the primary function of a {topic} in {application} systems.",
            "Compare the usage of a {topic} and {alternative} in {application}.",
            "When would a {topic} be better than a {alternative} in {application}?",
            "What limitations do you face using {topic} in {application}?",
            "Explain the role of a {topic} in managing {task} during {application}."
        ],
        "Level 2": [
            "Analyze the advantages of a {topic} in {application}.",
            "Evaluate the use of a {topic} in modern {application} systems.",
            "What are the trade-offs when using a {topic} for {application}?",
            "How does a {topic} handle concurrency issues in {application}?",
            "Identify drawbacks of using stacks in {scenario} for {application}.",
            "Compare stack-based vs queue-based solutions in {application}.",
            "Design a scenario where using a {topic} improves {application}.",
            "Examine the effectiveness of a {topic} in implementing {application}.",
            "Why is stack memory allocation important in {application}?",
            "Can a {topic} be replaced by a {alternative} in {application}? Discuss.",
            "Predict how stack behavior affects performance in {application}.",
            "What would go wrong if {topic} is improperly implemented in {application}?",
            "Explain limitations of stacks in large-scale {application} systems.",
            "Discuss stack overflow/underflow impacts in {application} context.",
            "Assess stack behavior under {scenario} during {application} execution."
        ],
        "Level 3": [
            "Design a stack-based system for efficient {application} in {scenario}.",
            "Critique stack suitability for large-scale {application} systems.",
            "Propose an improvement to stack usage in {application} to reduce {problem}.",
            "Design a hybrid system using {topic} and {alternative} for {application}.",
            "Build a stack-driven module to handle {application} in {context}.",
            "Evaluate trade-offs of recursive vs iterative stack-based solutions in {application}.",
            "Optimize stack performance in memory-constrained {application} scenarios.",
            "Simulate {application} using multiple stacks and evaluate efficiency.",
            "Develop an algorithm using stack for {application} under {scenario}.",
            "Illustrate a fault-tolerant stack system for critical {application} tasks.",
            "Propose a new abstraction layer over stacks to support {application}.",
            "Integrate stacks with {model} structures to enhance {application}.",
            "Apply stack principles to solve modern problems in {application} domain.",
            "What changes are required to scale stack operations for {application}?",
            "Evaluate limitations and propose fixes for using {topic} in {scenario}."
        ]
    },
    "Code Tracing": {
        "Level 1": [
            {
                "template": '''A = {arr}
def rev(arr):
    if arr:
        x = arr.pop()
        rev(arr)
        arr.insert(0, x)
rev(A)
print(A)''',
                "answer_fn": lambda arr: list(reversed(arr)),
            },
            {
                "template": '''A, B = [], []
A.extend({vals})
while A:
    B.append(A.pop())
print(B.pop())''',
                "answer_fn": lambda vals: vals[::-1][-1],
            },
            {
                "template": '''from collections import deque
q = deque({vals})
stk = []
while q:
    stk.append(q.popleft())
print(stk.pop())''',
                "answer_fn": lambda vals: vals[-1],
            }
        ],
        "Level 2": [
            {
                "template": '''class Node:
    def __init__(self, val): self.val, self.next = val, None
a = Node({val1}); b = Node({val2}); c = Node({val3})
a.next = b; b.next = c
stk = []
cur = a
while cur:
    stk.append(cur.val)
    cur = cur.next
while stk:
    print(stk.pop(), end=' ')''',
                "answer_fn": lambda v: f"{v[2]} {v[1]} {v[0]}"
            },
            {
                "template": '''stk = []
for val in {vals}:
    if val % 2 == 0:
        stk.append(val)
    else:
        stk.pop()
print(stk)''',
                "answer_fn": lambda vals: [v for v in vals if v % 2 == 0][:1] if vals else []
            }
        ],
        "Level 3": [
            {
                "template": '''exp = {expr}
stk = []
for tok in exp:
    if tok.isdigit():
        stk.append(int(tok))
    else:
        b, a = stk.pop(), stk.pop()
        stk.append(eval(f"{a}{tok}{b}"))
print(stk[0])''',
                "answer_fn": lambda expr: eval_postfix(expr)
            },
            {
                "template": '''num, k = '{num}', {k}
stk = []
for d in num:
    while k and stk and stk[-1] > d:
        stk.pop(); k -= 1
    stk.append(d)
print(''.join(stk[:len(stk)-k]).lstrip('0') or '0')''',
                "answer_fn": lambda num_k: remove_k_digits(num_k[0], num_k[1])
            }
        ]
    }
}

# Helper functions for answers:
def eval_postfix(exp):
    stk = []
    for tok in exp.split():
        if tok.isdigit():
            stk.append(int(tok))
        else:
            b, a = stk.pop(), stk.pop()
            stk.append(operators[tok][1](a, b))
    return stk[0]

def remove_k_digits(num, k):
    stk = []
    for d in num:
        while k and stk and stk[-1] > d:
            stk.pop()
            k -= 1
        stk.append(d)
    result = ''.join(stk[:len(stk) - k]).lstrip('0') or '0'
    return result

def get_code(level):
    return {
        "Level 1": "stack = []\nfor i in range(3): stack.append(i)\nprint(stack.pop())",
        "Level 2": "stack = []\nfor i in range(5):\n    if i % 2 == 0:\n        stack.append(i)\n    else:\n        stack.pop()\nprint(stack[-1])",
        "Level 3": "stack = []\ndata = [1, 2, 3, 4]\nfor x in data:\n    stack.append(x * 2)\nwhile stack:\n    print(stack.pop())",
    }[level]

def generate_template_questions(subtopic, level, count):
    templates = template_bank.get(subtopic, {}).get(level, [])
    results, used = [], set()
    if not templates:
        return results
    while len(results) < count:
        t = random.choice(templates)
        values = {k: random.choice(v) for k, v in placeholders.items() if f"{{{k}}}" in t}
        if "{code_snippet}" in t:
            values["code_snippet"] = get_code(level)
        q = t.format(**values)
        if q not in used:
            results.append({"type": "template", "subtopic": subtopic, "level": level, "question": q})
            used.add(q)
    return results

def generate_code_tracing_questions(topic, level, count):
    questions = []
    templates = template_bank.get(topic, {}).get(level, [])
    if not templates:
        return questions
    for _ in range(count):
        temp = random.choice(templates)

        if level == "Level 1":
            if "arr" in temp["template"]:
                params = random.sample(range(1, 10), 4)
                q_code = temp["template"].format(arr=params)
                ans = temp["answer_fn"](params)
                expl = explain_code_tracing_lev1(q_code, params)
            elif "vals" in temp["template"]:
                params = random.sample(range(10, 30), 3)
                q_code = temp["template"].format(vals=params)
                ans = temp["answer_fn"](params)
                expl = explain_code_tracing_lev1(q_code, params)
            else:
                q_code = temp["template"]
                ans = temp["answer_fn"]()
                expl = "Explanation not available."
        elif level == "Level 2":
            if "val1" in temp["template"]:
                params = random.sample(range(1, 10), 3)
                q_code = temp["template"].format(val1=params[0], val2=params[1], val3=params[2])
                ans = temp["answer_fn"](params)
                expl = explain_code_tracing_lev2(q_code, params)
            elif "vals" in temp["template"]:
                params = random.sample(range(1, 20), 6)
                q_code = temp["template"].format(vals=params)
                ans = temp["answer_fn"](params)
                expl = explain_code_tracing_lev2(q_code, params)
            else:
                q_code = temp["template"]
                ans = temp["answer_fn"]()
                expl = "Explanation not available."
        elif level == "Level 3":
            if "expr" in temp["template"]:
                digits = [str(random.randint(1, 9)) for _ in range(3)]
                ops_ = random.choices(['+', '-', '*', '/'], k=2)
                expr_list = [digits[0], digits[1], ops_[0], digits[2], ops_[1]]
                expr_str = ' '.join(expr_list)
                template_escaped = temp["template"].replace("{", "{{").replace("}", "}}").replace("{{expr}}", "{expr}")
                q_code = template_escaped.format(expr=expr_str)
                ans = temp["answer_fn"](expr_str)
                expl = explain_code_tracing_lev3(q_code, expr_str)
            elif "num" in temp["template"]:
                num = ''.join(random.choices('123456789', k=7))
                k = random.randint(1, 4)
                q_code = temp["template"].format(num=num, k=k)
                ans = temp["answer_fn"]((num, k))
                expl = explain_code_tracing_lev3_num_k(q_code, num, k)
            else:
                q_code = temp["template"]
                ans = temp["answer_fn"]()
                expl = "Explanation not available."
        else:
            q_code = temp["template"]
            ans = temp["answer_fn"]()
            expl = "Explanation not available."

        if isinstance(ans, (list, tuple)):
            ans = ' '.join(map(str, ans))
        else:
            ans = str(ans)

        questions.append({
            "type": "code_tracing",
            "subtopic": topic,
            "level": level,
            "question": q_code,
            "answer": ans,
            "explanation": expl
        })
    return questions

def explain_code_tracing_lev1(code, params):
    explanation = "**Stepwise Execution Explanation:**\n\n"
    if 'rev' in code:
        explanation += "1. The function 'rev' recursively pops the last element from the list and then inserts it at the front after the recursive call.\n"
        explanation += f"2. Starting with list: {params}\n"
        explanation += "3. This results in reversing the list.\n"
        explanation += f"4. Final reversed list: {list(reversed(params))}\n"
    elif 'B.append(A.pop())' in code:
        explanation += f"1. Initialize two lists A and B. A starts with {params}.\n"
        explanation += "2. While A is not empty, pop from A and append to B, reversing the order.\n"
        explanation += f"3. The last pop from B gives the first element from the original A: {params[0]}\n"
    elif 'deque' in code:
        explanation += f"1. Initialize a queue q with elements {params}.\n"
        explanation += "2. Pop elements from q (FIFO) and push them to a stack (LIFO).\n"
        explanation += "3. Popping from the stack returns the last element added which is last element of q.\n"
        explanation += f"4. Thus, output is: {params[-1]}\n"
    else:
        explanation += "Stepwise explanation not implemented for this code."
    return explanation

def explain_code_tracing_lev2(code, params):
    explanation = "**Stepwise Execution Explanation:**\n\n"
    if 'Node' in code:
        explanation += f"1. Create a linked list nodes with values {params}.\n"
        explanation += "2. Traverse the list, pushing node values onto a stack.\n"
        explanation += "3. Pop all elements from the stack to print in reverse order.\n"
        explanation += f"4. Output order: {params[2]} {params[1]} {params[0]}\n"
    elif 'if val % 2 == 0' in code:
        explanation += f"1. Iterate over values {params}.\n"
        explanation += "2. Append even numbers to stack and pop on odd numbers.\n"
        explanation += "3. Result is stack with last even number left.\n"
        filtered = [v for v in params if v % 2 == 0]
        explanation += f"4. Final stack contents: {filtered[:1] if filtered else []}\n"
    else:
        explanation += "Stepwise explanation not available."
    return explanation

def explain_code_tracing_lev3(code, expr):
    explanation = "**Stepwise Execution Explanation:**\n\n"
    explanation += f"1. Expression: {expr}\n"
    explanation += "2. Iterate through each token in the expression:\n"
    explanation += "   - If digit, push to stack.\n"
    explanation += "   - If operator, pop two elements, apply operation, push result.\n"
    tokens = expr.split()
    stack_vals = []
    for i, t in enumerate(tokens):
        explanation += f"Token {i + 1}: '{t}' - "
        if t.isdigit():
            stack_vals.append(int(t))
            explanation += f"Pushed {t} onto stack. Stack: {stack_vals}\n"
        else:
            b = stack_vals.pop()
            a = stack_vals.pop()
            op = operators[t][1]
            res = op(a, b)
            stack_vals.append(res)
            explanation += f"Popped {a} and {b}, performed '{a} {t} {b}' = {res}, pushed result. Stack: {stack_vals}\n"
    explanation += f"3. Final value on stack is {stack_vals[0]}, which is the result."
    return explanation

def explain_code_tracing_lev3_num_k(code, num, k):
    explanation = "**Stepwise Execution Explanation:**\n\n"
    explanation += f"1. Number string: {num}\n"
    explanation += f"2. Remove {k} digits to get smallest possible number.\n"
    stk = []
    remaining = k
    for d in num:
        while remaining and stk and stk[-1] > d:
            explanation += f"   - Pop '{stk[-1]}' because it's larger than '{d}' and digits to remove remain.\n"
            stk.pop()
            remaining -= 1
        stk.append(d)
        explanation += f"   - Push '{d}', current stack: {''.join(stk)}\n"
    if remaining > 0:
        explanation += f"3. Remove last {remaining} digits from stack as no smaller digits found.\n"
    result = ''.join(stk[:len(stk) - remaining]).lstrip('0') or '0'
    explanation += f"4. Final number after removal: {result}\n"
    return explanation

def generate_expression_question():
    ops = [random.choice(list(operators)) for _ in range(random.randint(2, 3))]
    operands = [str(random.randint(1, 10)) for _ in range(len(ops) + 1)]
    infix = ' '.join(sum(zip(operands, ops), ()) + (operands[-1],))
    postfix = infix_to_postfix(infix)
    prefix = infix_to_prefix(infix)
    return [
        {"type": "expression", "subtopic": "Expression Evaluation", "level": "Auto",
         "question": f"Evaluate postfix: {postfix}",
         "answer": evaluate_postfix(postfix),
         "explanation": explain_expression_postfix(postfix)},
        {"type": "expression", "subtopic": "Expression Evaluation", "level": "Auto",
         "question": f"Convert infix to prefix: {infix}",
         "answer": prefix,
         "explanation": explain_expression_infix_to_prefix(infix)},
        {"type": "expression", "subtopic": "Expression Evaluation", "level": "Auto",
         "question": f"Convert infix to postfix: {infix}",
         "answer": postfix,
         "explanation": explain_expression_infix_to_postfix(infix)}
    ]

# ----- OPERATORS AND FUNCTIONS FOR EXPRESSION EVALUATION -----
operators = {
    '+': (1, operator.add),
    '-': (1, operator.sub),
    '*': (2, operator.mul),
    '/': (2, operator.floordiv),
    '%': (2, operator.mod),
    '^': (3, operator.pow)
}

def infix_to_postfix(expr):
    prec = {op: p[0] for op, p in operators.items()}
    output, stack = [], []
    for token in expr.split():
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and prec[token] <= prec.get(stack[-1], 0):
                output.append(stack.pop())
            stack.append(token)
    return ' '.join(output + stack[::-1])

def infix_to_prefix(expr):
    reverse_tokens = ['(' if t == ')' else ')' if t == '(' else t for t in expr.split()[::-1]]
    rev_expr = ' '.join(reverse_tokens)
    postfix_rev = infix_to_postfix(rev_expr)
    prefix = ' '.join(postfix_rev.split()[::-1])
    return prefix

def evaluate_postfix(expr):
    s = []
    for t in expr.split():
        if t.isdigit():
            s.append(int(t))
        elif len(s) >= 2:
            b, a = s.pop(), s.pop()
            s.append(operators[t][1](a, b))
    return s[0] if s else "Invalid"

def explain_expression_postfix(postfix_expr):
    explanation = "**Postfix Expression Evaluation Explanation:**\n\n"
    stack = []
    tokens = postfix_expr.split()
    for i, token in enumerate(tokens):
        if token.isdigit():
            stack.append(int(token))
            explanation += f"Push {token} to stack: {stack}\n"
        else:
            b = stack.pop()
            a = stack.pop()
            op = operators[token][1]
            res = op(a, b)
            stack.append(res)
            explanation += f"Pop {a} and {b}, compute {a} {token} {b} = {res}, push result: {stack}\n"
    explanation += f"Result on stack is {stack[0]} which is the answer."
    return explanation

def explain_expression_infix_to_postfix(infix_expr):
    explanation = "**Infix to Postfix Conversion Explanation:**\n\n"
    precedence = {op: prec for op, (prec, _) in operators.items()}
    stack = []
    output = []
    tokens = infix_expr.split()
    for token in tokens:
        if token.isdigit():
            output.append(token)
            explanation += f"Add operand {token} to output: {' '.join(output)}\n"
        elif token == '(':
            stack.append(token)
            explanation += f"Push '(' to stack: {stack}\n"
        elif token == ')':
            while stack and stack[-1] != '(':
                popped = stack.pop()
                output.append(popped)
                explanation += f"Pop {popped} from stack to output: {' '.join(output)}\n"
            stack.pop()  # Pop '('
            explanation += f"Pop '(' from stack\n"
        else:
            while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], 0):
                popped = stack.pop()
                output.append(popped)
                explanation += f"Pop {popped} from stack to output due to precedence: {' '.join(output)}\n"
            stack.append(token)
            explanation += f"Push operator {token} to stack: {stack}\n"
    while stack:
        popped = stack.pop()
        output.append(popped)
        explanation += f"Pop remaining {popped} from stack to output: {' '.join(output)}\n"
    explanation += f"Final postfix expression: {' '.join(output)}"
    return explanation

def explain_expression_infix_to_prefix(infix_expr):
    explanation = "**Infix to Prefix Conversion Explanation:**\n\n"
    precedence = {op: prec for op, (prec, _) in operators.items()}
    stack = []
    output = []
    tokens = infix_expr.split()[::-1]  # Reverse tokens for prefix conversion
    for token in tokens:
        if token.isdigit():
            output.append(token)
            explanation += f"Add operand {token} to output: {' '.join(output)}\n"
        elif token == ')':
            stack.append(token)
            explanation += f"Push ')' to stack: {stack}\n"
        elif token == '(':
            while stack and stack[-1] != ')':
                popped = stack.pop()
                output.append(popped)
                explanation += f"Pop {popped} from stack to output: {' '.join(output)}\n"
            stack.pop()  # Pop ')'
            explanation += f"Pop ')' from stack\n"
        else:
            while stack and stack[-1] != ')' and precedence[token] < precedence.get(stack[-1], 0):
                popped = stack.pop()
                output.append(popped)
                explanation += f"Pop {popped} from stack to output due to precedence: {' '.join(output)}\n"
            stack.append(token)
            explanation += f"Push operator {token} to stack: {stack}\n"
    while stack:
        popped = stack.pop()
        output.append(popped)
        explanation += f"Pop remaining {popped} from stack to output: {' '.join(output)}\n"
    explanation += f"Final prefix expression: {' '.join(output[::-1])}"  # Reverse output
    return explanation

# ----- STREAMLIT APP UI -----
st.set_page_config(page_title="Stack Question Generator", layout="centered")

st.markdown("""
<style>
body {
    background-color: #ffffff;
    color: #6b7280;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0 2rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}
h1, h2, h3, h4 {
    font-weight: 700;
    color: #111827;
    line-height: 1.2;
}
h1 {
    font-size: 3rem;
    margin: 2rem 0 1rem 0;
    font-weight: 800;
}
.explanation {
    background-color: #f9fafb;
    border-radius: 0.75rem;
    padding: 1rem 1.25rem;
    margin-top: 1rem;
    color: #374151;
    font-size: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    white-space: pre-wrap;
}
.stButton>button {
    background-color: #111827 !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 0.5rem !important;
    padding: 0.6rem 1.2rem !important;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #374151 !important;
}
.stSelectbox>div>div>div>select {
    color: #374151;
    font-weight: 500;
}
.stSlider>div>input[type="range"] {
    accent-color: #111827;
}
.stCheckbox>div>label {
    color: #374151;
    font-weight: 500;
}
code {
    font-family: 'Source Code Pro', monospace;
    background-color: #f3f4f6;
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    color: #111827;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Stack Question Generator")

if "all_questions" not in st.session_state:
    st.session_state.all_questions = []

with st.form("question_form"):
    selected_subtopic = st.selectbox("Select Subtopic", subtopics, key="subtopic")
    selected_level = st.selectbox("Select Level", levels, key="level")
    selected_type = st.selectbox("Select Question Type", question_types, key="type")
    question_count = st.slider("Number of Questions", 1, 100, 10, key="count")
    show_answers = st.checkbox("Show Answers", value=True, key="show_answers")
    show_explanations = st.checkbox("Show Answer Explanations", value=True, key="show_explanations")
    submit = st.form_submit_button("Generate Questions")

if submit:
    new_questions = []
    if selected_subtopic == "Expression Evaluation":
        for _ in range(question_count):
            new_questions += generate_expression_question()
    elif selected_subtopic == "Code Tracing":
        # Always use code tracing question generator, ignoring question type
        new_questions = generate_code_tracing_questions(selected_subtopic, selected_level, question_count)
    else:
        new_questions = generate_questions_by_type(selected_type, selected_subtopic, selected_level, question_count)
    if not new_questions:
        st.warning("No questions generated for the selected subtopic and level.")
    else:
        st.session_state.all_questions.extend(new_questions)
        st.success(f"{len(new_questions)} questions generated.")

if st.session_state.all_questions:
    st.markdown("### 📋 All Questions")
    for i, q in enumerate(st.session_state.all_questions, 1):
        st.markdown(f"**Q{i} [{q.get('subtopic', '')} - {q.get('type', '')}]**:")
        language = "python" if q.get("subtopic", "") == "Code Tracing" else None
        st.code(q["question"], language=language)
        if show_answers and "answer" in q:
            st.markdown("**Answer:**")
            st.code(q["answer"])
            if show_explanations and "explanation" in q:
                st.markdown(f'<div class="explanation">{q["explanation"]}</div>', unsafe_allow_html=True)

    json_data = json.dumps(st.session_state.all_questions, indent=2)
    st.download_button("📥 Download Questions (JSON)", data=json_data, file_name="questions.json")

    if st.button("❌ Clear All"):
        st.session_state.all_questions = []
        st.experimental_rerun()

