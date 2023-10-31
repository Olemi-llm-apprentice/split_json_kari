
from janome.tokenizer import Tokenizer
import json

tokenizer = Tokenizer()

def split_and_adjust_segments_by_janome(segments, max_token_count=25):
    new_segments = []
    
    for idx, segment in enumerate(segments):
        text = segment['text']
        tokens = [token.surface for token in tokenizer.tokenize(text)]
        words = segment.get('words', [])
        
        textdebug = f"textdebug_{idx}.json"
        with open(textdebug, 'w', encoding='utf-8') as g:
            json.dump(text, g, ensure_ascii=False, indent=4)
        
        start_time = segment['start']
        token_idx = 0
        word_idx = 0

        while token_idx < len(tokens):
            sub_text = []
            sub_words = []
            token_count = 0

            while token_count < max_token_count and token_idx < len(tokens):
                token = tokens[token_idx]
                
                while word_idx < len(words) and words[word_idx]['word'] not in token:
                    word_idx += 1

                if word_idx < len(words):
                    word_info = words[word_idx].copy()
                    
                    if len(token) > 1:
                        word_info['word'] = token
                        word_info['end'] = words[word_idx + len(token) - 1]['end']
                    
                    sub_text.append(token)
                    sub_words.append(word_info)
                    token_count += 1
                    word_idx += 1

                token_idx += 1

            if token_count <= max_token_count:
                end_time = sub_words[-1].get('end', start_time) if sub_words else start_time
                new_segments.append({
                    'start': start_time,
                    'end': end_time,
                    'text': ''.join(sub_text),
                    'words': sub_words
                })

                if word_idx < len(words):
                    start_time = words[word_idx].get('start', end_time)
            
    return new_segments

# Load the original JSON (replace with the actual path)
with open('pawahara.json', 'r', encoding='utf-8') as f:
    json_content = json.load(f)

# Apply the function to all segments
new_segments_all = split_and_adjust_segments_by_janome(json_content['segments'])

# Replace the 'segments' in the original JSON
json_content['segments'] = new_segments_all

# Save the modified JSON (replace with the desired output path)
with open('pawahara_modified_by_janome.json', 'w', encoding='utf-8') as f:
    json.dump(json_content, f, ensure_ascii=False, indent=4)
