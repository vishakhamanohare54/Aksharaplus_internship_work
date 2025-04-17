from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Stack ADT syllabus
stack_topics = {
    "Stack ADT": {
        "subtopics": {
            "Introduction": {
                "Level 1": [
                    "What is a {topic} and its basic operations?",
                    "How does a {topic} differ from a {model} in terms of {aspect}?",
                    "What is the LIFO principle in a {topic}?",
                    "What are the real-world applications of a {topic} in {application}?",
                    "What is the time complexity of {operation} in a {topic}?"
                ],
                "Level 2": [
                    "Explain the LIFO principle in a {topic} with an example.",
                    "Compare {topic} and {model} based on {dimension}.",
                    "What are the limitations of a {topic} in {scenario}?",
                    "How does a {topic} handle {problem} in {context}?",
                    "What is the role of a {topic} in {application}?"
                ],
                "Level 3": [
                    "Analyze the use of a {topic} in {application}.",
                    "Critique the efficiency of a {topic} for {task}.",
                    "How does a {topic} handle {problem} in {scenario}?",
                    "Prove the time complexity of {operation} in a {topic}.",
                    "Why is a {topic} preferred over {alternative} for {task}?"
                ],
                "Level 4": [
                    "Design a {topic} to solve {problem} in {scenario}.",
                    "Prove the correctness of {operation} in a {topic}.",
                    "Analyze the space complexity of a {topic} in {context}.",
                    "Critique the use of a {topic} in {application}.",
                    "Derive the full implementation of a {topic} for {task}."
                ]
            },
            "Operations": {
                "Level 1": [
                    "What is the purpose of the {operation} operation in a {topic}?",
                    "How does the {operation} operation work in a {topic}?",
                    "What happens if you {operation} an empty {topic}?",
                    "What is the time complexity of {operation} in a {topic}?",
                    "What is the role of {operation} in {application}?"
                ],
                "Level 2": [
                    "Explain the {operation} operation in a {topic} with an example.",
                    "Compare {operation} in {topic} and {model} based on {dimension}.",
                    "What are the edge cases for {operation} in a {topic}?",
                    "How does {operation} handle {problem} in {scenario}?",
                    "What is the role of {operation} in {context}?"
                ],
                "Level 3": [
                    "Analyze the use of {operation} in a {topic} for {task}.",
                    "Critique the efficiency of {operation} in a {topic}.",
                    "How does {operation} handle {problem} in {scenario}?",
                    "Prove the time complexity of {operation} in a {topic}.",
                    "Why is {operation} preferred over {alternative} for {task}?"
                ],
                "Level 4": [
                    "Design a {topic} to optimize {operation} for {problem}.",
                    "Prove the correctness of {operation} in a {topic}.",
                    "Analyze the space complexity of {operation} in a {topic}.",
                    "Critique the use of {operation} in {application}.",
                    "Derive the full implementation of {operation} in a {topic}."
                ]
            },
            "Implementation": {
                "Level 1": [
                    "What is the simplest way to implement a {topic}?",
                    "What data structures can be used to implement a {topic}?",
                    "What is the role of {data_structure} in implementing a {topic}?",
                    "What is the time complexity of {operation} in a {topic}?",
                    "What is the space complexity of a {topic}?"
                ],
                "Level 2": [
                    "Explain the implementation of a {topic} using {data_structure}.",
                    "Compare the implementation of {topic} and {model} based on {dimension}.",
                    "What are the trade-offs of using {data_structure} for a {topic}?",
                    "How does the implementation of a {topic} handle {problem}?",
                    "What is the role of {data_structure} in {context}?"
                ],
                "Level 3": [
                    "Analyze the implementation of a {topic} for {task}.",
                    "Critique the efficiency of a {topic} implemented with {data_structure}.",
                    "How does the implementation of a {topic} handle {problem} in {scenario}?",
                    "Prove the time complexity of {operation} in a {topic}.",
                    "Why is {data_structure} preferred over {alternative} for implementing a {topic}?"
                ],
                "Level 4": [
                    "Design an optimized implementation of a {topic} for {problem}.",
                    "Prove the correctness of the implementation of a {topic}.",
                    "Analyze the space complexity of a {topic} implemented with {data_structure}.",
                    "Critique the use of {data_structure} in implementing a {topic}.",
                    "Derive the full implementation of a {topic} for {task}."
                ]
            },
            "Applications": {
                "Level 1": [
                    "What are the real-world applications of a {topic}?",
                    "How is a {topic} used in {application}?",
                    "What is the role of a {topic} in {context}?",
                    "What are the advantages of using a {topic} in {scenario}?",
                    "What are the limitations of using a {topic} in {application}?"
                ],
                "Level 2": [
                    "Explain the use of a {topic} in {application} with an example.",
                    "Compare the use of {topic} and {model} in {application} based on {dimension}.",
                    "What are the edge cases for using a {topic} in {scenario}?",
                    "How does a {topic} handle {problem} in {context}?",
                    "What is the role of a {topic} in {task}?"
                ],
                "Level 3": [
                    "Analyze the use of a {topic} in {application} for {task}.",
                    "Critique the efficiency of a {topic} in {scenario}.",
                    "How does a {topic} handle {problem} in {context}?",
                    "Prove the time complexity of {operation} in a {topic}.",
                    "Why is a {topic} preferred over {alternative} for {task}?"
                ],
                "Level 4": [
                    "Design a {topic} to solve {problem} in {scenario}.",
                    "Prove the correctness of using a {topic} in {application}.",
                    "Analyze the space complexity of a {topic} in {context}.",
                    "Critique the use of a {topic} in {application}.",
                    "Derive the full implementation of a {topic} for {task}."
                ]
            }
        }
    }
}

# Options for theoretical placeholders
stack_options = {
    "goal": ["data storage", "algorithm optimization", "problem solving"],
    "application": ["undo operations", "expression evaluation", "backtracking", "memory management", "parsing"],
    "model": ["Queue", "Linked List", "Array", "Tree", "Graph"],
    "aspect": ["data access", "memory usage", "time complexity", "implementation complexity"],
    "operation": ["push", "pop", "peek", "isEmpty", "isFull"],
    "data_structure": ["array", "linked list", "dynamic array", "vector"],
    "dimension": ["efficiency", "scalability", "simplicity", "flexibility"],
    "task": ["undo operations", "expression evaluation", "backtracking", "memory management"],
    "scenario": ["real-time systems", "large datasets", "low memory environments", "high-performance systems"],
    "alternative": ["Queue", "Linked List", "Array", "Tree", "Graph"],
    "context": ["theory", "practice", "real-world"],
    "problem": ["stack overflow", "underflow", "memory leaks", "inefficient operations"],
    "theory": ["data structures", "algorithms", "computational complexity", "memory management"],
    "practice": ["implementation", "optimization", "debugging", "testing"]
}

# Function to generate a unique question
def generate_unique_question(topic, subtopic, difficulty, used_questions):
    templates = stack_topics[topic]["subtopics"][subtopic][difficulty]
    while True:
        template = random.choice(templates)
        params = {
            "x": random.randint(-10, 10),
            "n": random.randint(5, 20),
            "m": random.randint(5, 10),
            "t": random.randint(1, 10),
            "s": random.uniform(0.1, 2)
        }
        params.update({key: random.choice(values) for key, values in stack_options.items() if f"{{{key}}}" in template})
        question = template.format(topic=topic, subtopic=subtopic, **params)
        if question not in used_questions:
            used_questions.add(question)
            return question

# Flask routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    topic = request.form.get("topic")
    subtopic = request.form.get("subtopic")
    difficulty = request.form.get("difficulty")
    used_questions = set()
    question = generate_unique_question(topic, subtopic, difficulty, used_questions)
    return jsonify({"question": question})

if __name__ == "__main__":
    app.run(debug=True)