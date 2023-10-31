
from janome.tokenizer import Tokenizer
import json

tokenizer = Tokenizer()

def split_and_adjust_segments_by_janome(segments, max_token_count=25):
    new_segments = []
    
    for segment in segments:
        text = segment['text']
        tokens = [token.surface for token in tokenizer.tokenize(text)]
        words = segment.get('words')
        
        start_time = segment['start']
        token_idx = 0  # Index for tokens
        word_idx = 0  # Index for words

        while token_idx < len(tokens):
            sub_text = []
            sub_words = []
            token_count = 0

            while token_count < max_token_count and token_idx < len(tokens):
                token = tokens[token_idx]
                
                # Skip to the word that matches the token
                while word_idx < len(words) and words[word_idx]['word'] not in token:
                    word_idx += 1

                if word_idx < len(words):
                    word_info = words[word_idx].copy()  # Create a copy to modify

                    # Update word_info if the token is longer than one character
                    if len(token) > 1:
                        word_info['word'] = token
                        word_info['end'] = words[word_idx + len(token) - 1]['end']
                    
                    sub_text.append(token)
                    sub_words.append(word_info)
                    token_count += 1
                    word_idx += 1

                # Increment token_idx regardless to avoid infinite loop
                token_idx += 1

            # Handle segments with up to 25 tokens
            if token_count <= max_token_count:
                end_time = sub_words[-1].get('end', start_time) if sub_words else start_time  # Check if 'end' exists
                new_segments.append({
                    'start': start_time,
                    'end': end_time,
                    'text': ''.join(sub_text),
                    'words': sub_words
                })

                # Update start_time for the next sub-segment
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
