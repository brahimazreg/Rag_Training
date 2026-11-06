from rag_chain import ask_question

#question = "Who can purchase licenses?"

question = "What is the population of Japan?"
answer = ask_question(question)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)