
from janome.tokenizer import Tokenizer
import json

tokenizer = Tokenizer()

def split_and_adjust_segments_by_janome(segments, max_token_count=25):
    new_segments = []
    
    for segment in segments:
        text = segment['text']
        tokens = [token.surface for token in tokenizer.tokenize(text)]
        words = segment.get('words', [])
        
        start_time = segment['start']
        token_idx = 0  # Index for tokens
        word_idx = 0  # Index for words

        print(f"Processing segment: {segment}")  # デバッグ：処理中のセグメント

        while token_idx < len(tokens):
            sub_text = []
            sub_words = []
            token_count = 0

            print(f"Initial token_idx: {token_idx}, word_idx: {word_idx}")  # デバッグ：初期のtoken_idxとword_idx

            while token_count < max_token_count and token_idx < len(tokens):
                token = tokens[token_idx]
                
                # Try to match the token with a word
                matched = False
                while word_idx < len(words) and not matched:
                    if words[word_idx]['word'] in token:
                        matched = True
                        word_info = words[word_idx]
                        sub_words.append(word_info)
                        word_idx += 1
                    else:
                        word_idx += 1  # Only advance word_idx if the current word does not match

                sub_text.append(token)
                token_idx += 1
                token_count += 1

            end_time = sub_words[-1]['end'] if sub_words else start_time

            new_segment = {
                'start': start_time,
                'end': end_time,
                'text': ''.join(sub_text),
                'words': sub_words
            }
            
            print(f"Appending segment: {new_segment}")  # デバッグ：追加するセグメント

            new_segments.append(new_segment)
            start_time = end_time

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
