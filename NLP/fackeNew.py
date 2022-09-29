from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd

# Get model after train
model_patch = "./NLP/model/fake-news-dataset-mee-model"

model = AutoModelForSequenceClassification.from_pretrained(model_patch)
tokenizer = AutoTokenizer.from_pretrained(model_patch)
max_length = 512

# TEXT
# real_news = """
# Tim Tebow Will Attempt Another Comeback, This Time in Baseball -
# The New York Times",Daniel Victor,"If at first you don't
# succeed, try a different sport. Tim Tebow, who was a
# Heisman quarterback at the University of Florida but was
# unable to hold an N. F. L. job, is pursuing a career in Major
# League Baseball. <SNIPPED>
# """


def get_prediction(text, convert_to_label=False):
    # prepare our text into tokenized sequence
    inputs = tokenizer(text, padding=True, truncation=True, max_length=max_length,
                       return_tensors="pt")

    # perform inference to our model
    outputs = model(**inputs)
    # get output probabilities by doing softmax
    probs = outputs[0].softmax(1)
    # executing argmax function to get the candidate label
    d = {
        0: "reliable",
        1: "fake"
    }
    if convert_to_label:
        return d[int(probs.argmax())]
    else:
        return int(probs.argmax())


# predict = get_prediction(real_news, convert_to_label=True)
# print(predict)
