import streamlit as st
import random
import json
import sys
import re
from collections import deque

sys.set_int_max_str_digits(10000)

# ----- CONFIG -----
subtopics = [
    "Introduction to Queues",
    "Queue Implementations",
    "Types of Queues",
    "Queue Applications",
    "Queue in Algorithmic Problems",
    "Queue Variants and Implementations",
    "Queue Numericals"
]
levels = ["Level 1", "Level 2", "Level 3"]
question_types = ["Long Answer", "MCQ", "True/False", "One Word", "Fill in the Blanks"]

# ----- PLACEHOLDERS AND TEMPLATES -----
placeholders = {
    "topic": ["queue", "priority queue", "circular queue", "double-ended queue"],
    "operation": ["enqueue", "dequeue", "peek", "isEmpty", "isFull", "size", "clear", "traverse"],
    "model": ["array", "linked list", "heap"],
    "aspect": ["structure", "behavior", "memory usage", "efficiency", "execution time"],
    "dimension": ["performance", "complexity", "usability", "data access", "scalability"],
    "application": [
        "task scheduling", "buffer management", "print queue", "breadth-first search",
        "call center systems", "job scheduling", "network packet management"
    ],
    "scenario": ["large datasets", "multithreading", "limited memory", "real-time systems",
                 "concurrent execution", "cloud deployment", "data streaming"],
    "problem": ["overflow", "underflow", "memory leak", "data corruption", "queue crash"],
    "context": ["recursion", "system design", "low-level memory operations", "compiler design"],
    "task": ["processing tasks", "managing requests", "evaluating expressions", "tracking calls"],
    "alternative": ["stack", "list", "dictionary", "set", "deque"],
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
        "True or False: A {topic} follows the FIFO principle.",
        "True or False: The {operation} operation can be performed on an empty {topic}.",
        "True or False: A {topic} can be implemented using an array.",
        "True or False: The size of a {topic} is fixed once it is created.",
        "True or False: The {operation} operation is more efficient than {alternative_operation} in all cases.",
        "True or False: A {topic} can be used to manage tasks in programming languages.",
    ],
    "One Word": [
        "What is the term for the first element added to a {topic}?",
        "What is the primary data structure used to implement a {topic}?",
        "What is the term for the operation that adds an element to a {topic}?",
        "What is the term for the operation that retrieves the front element from a {topic}?",
        "What is the maximum number of elements a {topic} can hold called?",
        "What is the term for the condition when a {topic} cannot accept more elements?",
    ],
    "Fill in the Blanks": [
        "A {topic} is used to manage __________ in programming.",
        "The operation __________ is used to remove the front element from a {topic}.",
        "In a {topic}, the first element added is the first one to be removed, following the __________ principle.",
        "The __________ operation checks if a {topic} is empty.",
        "To prevent overflow, a {topic} must be checked for __________ before adding a new element.",
        "The __________ operation retrieves the front element without removing it from a {topic}.",
    ]
}

# ----- FUNCTION TO GENERATE QUEUE NUMERICAL QUESTIONS -----
def generate_queue_numerical_questions(level, count, used_questions):
    questions = []

    for _ in range(count):
        q_type = random.choice(["circular_index", "deque_simulation", "fcfs_schedule", "bfs_queue", "priority_order"])
        question = ""
        answer = ""
        explanation = []

        if q_type == "circular_index":
            size = 5
            ops = ["ENQUEUE(10)", "ENQUEUE(20)", "DEQUEUE()", "ENQUEUE(30)", "ENQUEUE(40)", "DEQUEUE()", "ENQUEUE(50)"]
            front, rear = 0, -1
            queue = [None] * size
            for op in ops:
                if "ENQUEUE" in op:
                    rear = (rear + 1) % size
                    queue[rear] = int(op.split("(")[1].split(")")[0])
                    explanation.append(f"Operation: {op} -> Rear moved to {rear}, Queue State: {queue}")
                elif "DEQUEUE" in op:
                    explanation.append(f"Operation: {op} -> Front moved from {front} to {(front + 1) % size}, Queue State: {queue}")
                    queue[front] = None
                    front = (front + 1) % size
            answer = f"Front Index: {front}, Rear Index: {rear}, Queue State: {queue}"
            question = f"A circular queue of size {size} undergoes the following operations:\n{', '.join(ops)}\nWhat will be the front and rear indices and the state of the queue?"

        elif q_type == "deque_simulation":
            dq = deque()
            ops = ["appendleft(3)", "append(5)", "pop()", "appendleft(7)", "popleft()"]
            for op in ops:
                eval(f"dq.{op}")
                explanation.append(f"Operation: {op} -> Deque State: {dq}")
            answer = str(dq)
            question = f"Perform the following deque operations:\n{', '.join(ops)}\nWhat is the final state of the deque?\nExplanation:\n" + "\n".join(explanation)

        elif q_type == "fcfs_schedule":
            arrival = [0, 2, 4]
            burst = [3, 2, 1]
            start_time = [0]
            for i in range(1, len(arrival)):
                start_time.append(max(start_time[i-1] + burst[i-1], arrival[i]))
                explanation.append(f"Task {i}: Arrival Time: {arrival[i]}, Burst Time: {burst[i]}, Start Time: {start_time[i]}")
            answer = f"Start Times: {start_time}"
            question = f"Given task arrival times: {arrival} and burst times: {burst}, simulate FCFS and report the start times.\nExplanation:\n" + "\n".join(explanation)

        elif q_type == "bfs_queue":
            edges = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
            start = 'A'
            visited, queue, result = set(), [start], []
            while queue:
                node = queue.pop(0)
                if node not in visited:
                    visited.add(node)
                    result.append(node)
                    queue.extend(edges[node])
                    explanation.append(f"Visited: {node}, Queue State: {queue}")
            answer = f"BFS Order: {' -> '.join(result)}"
            question = f"Perform BFS traversal on graph starting from node {start}. Edges: {edges}. What is the order of traversal?\nExplanation:\n" + "\n".join(explanation)

        elif q_type == "priority_order":
            jobs = [('A', 2), ('B', 1), ('C', 3), ('D', 2)]
            sorted_jobs = sorted(jobs, key=lambda x: x[1])
            explanation = [f"Job {j[0]} with priority {j[1]}" for j in sorted_jobs]
            answer = f"Execution Order: {', '.join([j[0] for j in sorted_jobs])}"
            question = f"Given jobs with priorities: {jobs}, what is the execution order in a priority queue?\nExplanation:\n" + "\n".join(explanation)

        # Create a unique identifier for the question
        question_id = f"{q_type}_{question}"

        if question_id not in used_questions:
            questions.append({
                "type": "queue_numerical",
                "subtopic": "Queue Numericals",
                "level": level,
                "question": question,
                "answer": answer,
                "explanation": explanation
            })
            used_questions.add(question_id)  # Add the unique identifier to the set

    return questions

# ----- FUNCTION TO GENERATE TEMPLATE QUESTIONS -----
def generate_template_questions(subtopic, level, count, used_questions):
    templates = template_bank.get(subtopic, {}).get(level, [])
    results, used = [], set()
    if not templates:
        return results
    while len(results) < count:
        t = random.choice(templates)
        values = {k: random.choice(v) for k, v in placeholders.items() if f"{{{k}}}" in t}
        question = t.format(**values)
        if question not in used and question not in used_questions:
            results.append({"type": "template", "subtopic": subtopic, "level": level, "question": question})
            used.add(question)
            used_questions.add(question)
    return results

# ----- FUNCTION TO GENERATE QUESTIONS BY TYPE -----
def generate_questions_by_type(selected_type, subtopic, level, count):
    used_questions = set()  # Track used questions to avoid duplicates
    if selected_type == "Long Answer":
        return generate_template_questions(subtopic, level, count, used_questions)
    elif selected_type == "MCQ":
        return generate_mcq_questions(subtopic, count, used_questions)
    elif selected_type == "True/False":
        return generate_true_false_questions(subtopic, count, used_questions)
    elif selected_type == "One Word":
        return generate_one_word_questions(subtopic, count, used_questions)
    elif selected_type == "Fill in the Blanks":
        return generate_fill_in_the_blanks_questions(subtopic, count, used_questions)
    return []
template_bank = {
    "Introduction to Queues": {
        "Level 1": [
            "Explain the FIFO principle in a {topic} with an example.",
            "Compare {topic} and {model} based on {dimension}.",
            "What are the limitations of a {topic} in {scenario}?",
            "How does a {topic} handle {problem} in {context}?",
            "What is the role of a {topic} in {application}?",
            "Why is the FIFO property important in {application}?",
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
            "Explore the behavioral differences between bounded and unbounded queues.",
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
            "Compare and contrast lock-based and lock-free queue implementations.",
            "Evaluate queue behavior under concurrent modifications in a multithreaded system.",
            "What changes would you make to {topic} for optimizing recursion-heavy applications?",
            "Develop a fault-tolerant {topic} implementation for mission-critical systems.",
            "Simulate queue behavior under varying memory and CPU constraints.",
            "Propose an improvement to {operation} performance in memory-limited environments.",
            "Is it possible to parallelize {operation} in a {topic}? Justify your reasoning.",
            "Redesign a {topic} to use persistent memory and analyze implications.",
            "Construct a predictive model to forecast {topic} behavior under large-scale {application}."
        ]
    },
    "Queue Implementations": {
        "Level 1": [
            "Explain how to implement a {topic} using a {model}.",
            "Compare {topic} implementation using {model} and {alternative}.",
            "What are the key components when implementing a {topic} using an {model}?",
            "Explain the steps to implement a static {topic} using an array.",
            "How does a dynamic {topic} differ in implementation compared to a static one?",
            "Illustrate a basic implementation of a {topic} in C/C++.",
            "What are the advantages of implementing a {topic} with a linked list?",
            "How would you initialize a {topic} using an array?",
            "Write pseudocode for implementing a {topic} using a {model}.",
            "Describe error conditions in queue implementation using arrays.",
            "How do you manage overflow in a static {topic} implementation?",
            "Explain memory allocation differences between array-based and linked list {topic}s.",
            "How does index management work in array-based {topic}s?",
            "Explain how you would track the front element in a {topic} implemented with an array.",
            "How do you handle underflow in a basic {topic} implementation?"
        ],
        "Level 2": [
            "Evaluate trade-offs between array and linked list implementations of a {topic}.",
            "What are the challenges in implementing a dynamic {topic}?",
            "Analyze how pointer management works in linked list-based {topic}s.",
            "Design a {topic} implementation that supports dynamic resizing.",
            "How would you modify a static {topic} to support overflow handling?",
            "Discuss garbage collection implications for linked list {topic}s.",
            "Compare fixed-size and resizable queue implementations.",
            "Evaluate the time complexity of {operation} in a linked list vs array queue.",
            "What data structures can be used internally to implement a queue?",
            "Explain implementation differences of a {topic} in Java vs C++.",
            "Design a custom queue with minimum memory overhead.",
            "How can you implement a {topic} that supports rollback (undo feature)?",
            "Propose an implementation plan for an efficient queue for real-time systems.",
            "What are common implementation pitfalls in dynamic queue creation?",
            "How does memory fragmentation affect {topic} implemented with dynamic memory?"
        ],
        "Level 3": [
            "Implement a dynamic queue with overflow protection.",
            "Propose a memory-efficient design for {topic} implementation in {context}.",
            "Design and implement a {topic} that supports multi-threaded access.",
            "Develop a hybrid {topic} using both array and linked list.",
            "Create a queue implementation supporting additional operations like getMin().",
            "Implement a {topic} with O(1) time complexity for all operations.",
            "Design a concurrent {topic} using lock-free data structures.",
            "Write a complete implementation of a queue in a functional programming language.",
            "Create a customizable queue class supporting multiple data types.",
            "Implement a queue with logging capabilities for every operation.",
            "Build a persistent queue using file I/O for storing operations.",
            "Construct a {topic} suitable for memory-constrained embedded systems.",
            "Design a self-balancing queue for ordered data.",
            "Develop an advanced queue system with undo-redo capabilities.",
            "Write a unit-test ready queue module with mocks and stubs."
        ]
    },
    "Types of Queues": {
        "Level 1": [
            "What distinguishes a simple queue from a circular queue?",
            "Explain the concept of a double-ended queue (Deque).",
            "What are the key differences between a priority queue and a regular queue?",
            "Provide examples of real-world applications for each type of queue.",
            "How does the implementation of a circular queue differ from a linear queue?",
            "What are the advantages of using a priority queue over a simple queue?",
            "Describe the operations available for a double-ended queue.",
            "When would you choose to use a circular queue instead of a linear queue?",
            "What are the limitations of a simple queue compared to other types?",
            "How can a priority queue be implemented using a heap?"
        ],
        "Level 2": [
            "Analyze the time complexity of operations in a priority queue.",
            "Discuss the use cases for circular queues in real-time systems.",
            "Evaluate the performance differences between a linked list-based queue and an array-based queue.",
            "How do double-ended queues facilitate more complex data management?",
            "What are the trade-offs when implementing a priority queue using different data structures?",
            "Compare the memory usage of different queue implementations.",
            "How does the choice of queue type affect algorithm efficiency in BFS?",
            "What are the challenges in implementing a circular queue?",
            "Describe scenarios where a double-ended queue is more beneficial than a simple queue.",
            "How can priority queues be used in scheduling algorithms?"
        ],
        "Level 3": [
            "Design a multi-level queue system for task scheduling.",
            "Propose an implementation for a priority queue that supports dynamic priorities.",
            "Evaluate the impact of using a circular queue in a producer-consumer scenario.",
            "How can a double-ended queue be used to optimize a sliding window algorithm?",
            "Implement a priority queue using a binary heap and analyze its performance.",
            "Discuss the implications of using queues in operating systems and networks.",
            "Design a system that utilizes multiple types of queues for managing different tasks in a job scheduling application.",
            "Analyze the space complexity of various queue implementations in a memory-constrained environment.",
            "Propose a hybrid queue system that combines features of both circular and priority queues.",
            "How would you implement a blocking queue for multithreading applications?"
        ]
    },
    "Queue Applications": {
        "Level 1": [
            "Explain how queues are used in CPU scheduling, specifically in the Round Robin algorithm.",
            "What role do queues play in job scheduling systems?",
            "Describe how a queue can manage print tasks in a printer queue.",
            "How do queues facilitate real-time data buffering in streaming applications?",
            "Provide examples of applications that utilize queues for task management.",
            "What are the benefits of using queues in managing concurrent tasks?",
            "How does a queue help in organizing tasks in a call center system?",
            "Illustrate with an example how queues are used in network packet management.",
            "What makes queues suitable for handling asynchronous data processing?",
            "Discuss the importance of queues in implementing breadth-first search (BFS) in graphs."
        ],
        "Level 2": [
            "Analyze the advantages of using queues in CPU scheduling algorithms.",
            "Evaluate the effectiveness of queues in managing print jobs in a multi-user environment.",
            "What are the trade-offs when using queues for real-time data buffering?",
            "How do queues improve the efficiency of job scheduling in operating systems?",
            "Discuss the impact of queue size on performance in task management systems.",
            "Compare the use of queues versus stacks in managing tasks in software applications.",
            "What challenges arise when implementing queues in high-load scenarios?",
            "How can queues be optimized for better performance in network applications?",
            "Describe the role of queues in implementing LRU cache designs.",
            "What are the limitations of using queues in certain algorithmic problems?"
        ],
        "Level 3": [
            "Design a queue-based system for efficient CPU scheduling in a multi-core processor environment.",
            "Propose an advanced job scheduling system that utilizes multiple types of queues.",
            "Evaluate the performance of a queue in managing real-time data streams under varying loads.",
            "How can queues be integrated into a distributed system for task management?",
            "Implement a queue system that supports priority-based task execution in a cloud environment.",
            "Discuss the implications of using queues in the design of multi-level queue systems.",
            "Analyze the scalability of queue implementations in large-scale applications.",
            "Design a fault-tolerant queue system for critical applications in operating systems.",
            "How would you implement a queue that supports both blocking and non-blocking operations?",
            "Propose a solution for managing queues in a high-frequency trading system."
        ]
    },
    "Queue in Algorithmic Problems": {
        "Level 1": [
            "Explain how queues are utilized in breadth-first search (BFS) algorithms.",
            "What is the role of queues in solving sliding window problems?",
            "Describe how queues can be used to implement an LRU cache.",
            "How do queues facilitate multi-level queue systems in scheduling?",
            "Provide examples of algorithmic problems that can be solved using queues.",
            "What are the advantages of using queues in graph traversal algorithms?",
            "How can queues be applied in managing tasks in a breadth-first search?",
            "Discuss the importance of queues in implementing algorithms that require FIFO behavior.",
            "What are the limitations of using queues in certain algorithmic contexts?",
            "How do queues help in managing state in recursive algorithms?"
        ],
        "Level 2": [
            "Analyze the time complexity of BFS when implemented using a queue.",
            "Evaluate the effectiveness of queues in solving sliding window problems.",
            "What are the trade-offs when using queues for implementing an LRU cache?",
            "How do multi-level queues improve scheduling efficiency in operating systems?",
            "Discuss the impact of queue size on performance in algorithmic problem-solving.",
            "Compare the use of queues versus stacks in algorithmic implementations.",
            "What challenges arise when using queues in complex algorithmic problems?",
            "How can queues be optimized for better performance in algorithmic contexts?",
            "Describe the role of queues in implementing breadth-first search in trees.",
            "What are the limitations of using queues in certain algorithmic problems?"
        ],
        "Level 3": [
            "Design an algorithm that utilizes queues for efficient graph traversal.",
            "Propose a solution for managing sliding window problems using a queue.",
            "Evaluate the performance of a queue in implementing an LRU cache under high load.",
            "How can queues be integrated into a multi-level queue scheduling algorithm?",
            "Implement a queue-based solution for managing tasks in a complex algorithmic problem.",
            "Discuss the implications of using queues in the design of advanced algorithmic solutions.",
            "Analyze the scalability of queue implementations in solving large-scale algorithmic problems.",
            "Design a fault-tolerant queue system for critical algorithmic applications.",
            "How would you implement a queue that supports both blocking and non-blocking operations in algorithms?",
            "Propose a solution for managing queues in a high-frequency trading algorithm."
        ]
    },
    "Queue Variants and Implementations": {
        "Level 1": [
            "What is a queue using a stack and how does it work?",
            "Explain how a stack can be implemented using two queues.",
            "What is a blocking queue and where is it used?",
            "Describe the role of queues in operating systems.",
            "How do queues function in network applications?",
            "What are the differences between blocking and non-blocking queues?",
            "Provide examples of real-world applications for blocking queues.",
            "How can queues be used to implement a producer-consumer problem?",
            "What are the advantages of using queues in multithreading?",
            "Discuss the importance of queues in managing resources in operating systems."
        ],
        "Level 2": [
            "Analyze the time complexity of operations in a queue implemented using stacks.",
            "Evaluate the effectiveness of using queues in multithreading applications.",
            "What are the trade-offs when implementing a stack using queues?",
            "How do blocking queues improve resource management in concurrent systems?",
            "Discuss the impact of queue size on performance in multithreaded applications.",
            "Compare the use of blocking queues versus regular queues in task management.",
            "What challenges arise when implementing queues in high-load scenarios?",
            "How can queues be optimized for better performance in network applications?",
            "Describe the role of queues in implementing synchronization in multithreading.",
            "What are the limitations of using queues in certain operating system contexts?"
        ],
        "Level 3": [
            "Design a queue-based system for efficient resource management in a multithreaded environment.",
            "Propose an advanced implementation of a blocking queue for high-performance applications.",
            "Evaluate the performance of a queue in managing resources in a distributed system.",
            "How can queues be integrated into a system for managing network traffic?",
            "Implement a queue system that supports both blocking and non-blocking operations in multithreading.",
            "Discuss the implications of using queues in the design of advanced operating systems.",
            "Analyze the scalability of queue implementations in large-scale applications.",
            "Design a fault-tolerant queue system for critical applications in operating systems.",
            "How would you implement a queue that supports dynamic resizing?",
            "Propose a solution for managing queues in a high-frequency trading system."
        ]
    }
}
# ----- STREAMLIT APP UI -----
st.set_page_config(page_title="Queue Question Generator", layout="centered")

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

st.title("🧠 Queue Question Generator")

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
    used_questions = set(q["question"] for q in st.session_state.all_questions)  # Initialize with already generated questions
    if selected_subtopic == "Queue Numericals":
        new_questions = generate_queue_numerical_questions(selected_level, question_count, used_questions)
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
        st.code(q["question"])
        if show_answers and "answer" in q:
            st.markdown("**Answer:**")
            st.code(q["answer"])
            if show_explanations:
                explanation = "Step-by-step explanation:\n" + "\n".join(q.get("explanation", ["No explanation available."]))
                st.markdown(f'<div class="explanation">{ explanation}</div>', unsafe_allow_html=True)

    json_data = json.dumps(st.session_state.all_questions, indent=2)
    st.download_button("📥 Download Questions (JSON)", data=json_data, file_name="questions.json")

    if st.button("❌ Clear All"):
        st.session_state.all_questions = []
        st.experimental_rerun()
