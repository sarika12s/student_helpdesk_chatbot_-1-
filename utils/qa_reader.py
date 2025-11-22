from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch


class QAReader:
    def __init__(self, model_name="distilbert-base-uncased-distilled-squad"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    # ---------------- ANSWER EXTRACTION ----------------
    def answer(self, question, context):
        if not context.strip():
            return "", 0.0

        inputs = self.tokenizer(
            question,
            context,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        start_logits = outputs.start_logits
        end_logits = outputs.end_logits

        start_idx = torch.argmax(start_logits)
        end_idx = torch.argmax(end_logits)

        confidence = (torch.max(start_logits).item() + torch.max(end_logits).item()) / 2

        # Extract answer tokens
        answer_tokens = inputs.input_ids[0][start_idx:end_idx + 1]
        answer = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)

        # Clean answer
        answer = answer.replace("[CLS]", "").replace("[SEP]", "").strip()

        # Remove incomplete fragment answers
        if len(answer.split()) <= 2:
            return "", 0.0

        return answer, confidence
