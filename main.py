from labeltext import TextAnnotation

task = TextAnnotation(
    ["Albert Einstein", "Stephen King", "Marie Curie"], ["male", "female"]
)
print(task)
task.annotate(user_name="@dataBiryani", update_freq=2)

task = TextAnnotation()("annotations.pkl")
task.annotate(user_name="@dataBiryani")
