from bertviz import head_view, model_view
from bertviz.neuron_view import show
from transformers import BertTokenizer, BertModel

def run_bertviz_model(sentence_a, sentence_b, visualization_mode):
    model_version = 'bert-base-uncased'
    model = BertModel.from_pretrained(model_version, output_attentions=True, attn_implementation="eager")
    tokenizer = BertTokenizer.from_pretrained(model_version)
    inputs = tokenizer.encode_plus(sentence_a, sentence_b, return_tensors='pt')
    input_ids = inputs['input_ids']
    token_type_ids = inputs['token_type_ids']
    attention = model(input_ids, token_type_ids=token_type_ids)[-1]
    sentence_b_start = token_type_ids[0].tolist().index(1)
    input_id_list = input_ids[0].tolist()
    tokens = tokenizer.convert_ids_to_tokens(input_id_list)

    if visualization_mode == 'head_view':
        head_view(attention, tokens)
    elif visualization_mode == 'model_view':
        model_view(attention, tokens, sentence_b_start)
    else:
        model_type = 'bert'
        show(model, model_type, tokenizer, sentence_a, sentence_b, display_mode='dark', layer=1, head=1, html_action='embed')

run_bertviz_model(sentence_a, sentence_b, visualization_mode)