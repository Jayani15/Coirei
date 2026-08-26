from backend.rag import (
    add_job_description,
    search_job_description
)


result = add_job_description(
    "data/job_descriptions/job.txt",
    "job_1"
)

print(result)


results = search_job_description(
    "What programming language is required?",
    "job_1"
)

print("\nRetrieved chunks:")

for chunk in results:
    print("\n---")
    print(chunk)