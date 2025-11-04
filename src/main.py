from unstructured.partition.auto import partition


elements = partition(filename="../files/climbing-report.pdf")
with open("../files/output.txt", "w") as f:
    f.write("\n\n".join([str(el) for el in elements]))