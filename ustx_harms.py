import yaml
from colorama import Fore, Style

def colored_print(text, color=Fore.WHITE, style=Style.NORMAL):
    print(style + color + text + Style.RESET_ALL)

def get_ustx_data(file_path):
    if not file_path.lower().endswith(".ustx"):
        file_path += ".ustx"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f), False
    except FileNotFoundError:
        return None, "FileNotFoundError"
    except yaml.YAMLError as e:
        return None, f"YAMLError: {e}"
    return yaml.safe_load(f), False

def save_ustx_data(ustx_data, output_file_path):
    if not output_file_path.lower().endswith(".ustx"):
        output_file_path += ".ustx"
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(ustx_data, f, allow_unicode=True, indent=2, sort_keys=False)
    except Exception as e:
        return f"Error saving file: {e}"
    return None

def get_track_names(ustx_data):
    return [track.get('track_name', f"Track {i+1}") for i, track in enumerate(ustx_data.get('tracks', []))]

key_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

def get_key_from_notes(notes):
    note_counts = {}
    for note in notes:
        tone = note['tone'] % 12
        note_counts[tone] = note_counts.get(tone, 0) + 1

    if not note_counts:
        return 0, key_names[0], "major"

    major_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 3.78, 2.14, 4.04, 2.0, 3.5]
    minor_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 2.53, 4.48, 2.42, 3.17, 2.35]

    best_key_index = 0
    best_mode = "major"
    max_score = -float('inf')
    scores = []

    for key_tone_index in range(12):
        major_score = 0
        for i in range(12):
            note_index = (key_tone_index + i) % 12
            major_score += note_counts.get(note_index, 0) * major_profile[i]

        scores.append({'key': key_names[key_tone_index] + " Major", 'score': major_score})

        minor_score = 0
        for i in range(12):
            note_index = (key_tone_index + i) % 12
            minor_score += note_counts.get(note_index, 0) * minor_profile[i]
        scores.append({'key': key_names[key_tone_index] + " Minor", 'score': minor_score})

    scores.sort(key=lambda x: x['score'], reverse=True)

    best_key_index = key_names.index(scores[0]['key'].split(" ")[0])
    best_mode = scores[0]['key'].split(" ")[1].lower()
    max_score = scores[0]['score']

    print(f"{Fore.CYAN}Key Detection Scores (Top 5):{Style.RESET_ALL}")
    for i in range(min(5, len(scores))):
        print(f"  {scores[i]['key']}: {scores[i]['score']:.2f}", Fore.WHITE if i > 0 else Fore.GREEN)

    return best_key_index, key_names[best_key_index], best_mode

def get_scale_intervals(key_tone_index, mode):
    major_intervals = [0, 2, 4, 5, 7, 9, 11]
    minor_intervals = [0, 2, 3, 5, 7, 8, 10]

    key_tone = key_tone_index

    if mode == "major":
        return [(key_tone + interval) % 12 for interval in major_intervals]
    elif mode == "minor":
        return [(key_tone + interval) % 12 for interval in minor_intervals]
    return []

def is_note_in_key(note_tone, key_tone_index, mode):
    scale_intervals = get_scale_intervals(key_tone_index, mode)
    note_class = note_tone % 12
    return note_class in scale_intervals

def generate_harmony_notes(original_notes_for_track, semitone_interval, harmony_type, key_tone_index, key_mode):
    harmony_tracks_notes = []

    if harmony_type in (1, 3):
        lower_harmony_notes = []
        for note in original_notes_for_track:
            harmony_tone = note['tone'] - semitone_interval
            original_tone = harmony_tone

            correction_attempts = 0
            while not is_note_in_key(harmony_tone, key_tone_index, key_mode) and correction_attempts < 3:
                harmony_tone += 1
                correction_attempts += 1

            if not is_note_in_key(harmony_tone, key_tone_index, key_mode):
                harmony_tone = original_tone

            lower_harmony_notes.append({**note, 'tone': harmony_tone})
        harmony_tracks_notes.append(lower_harmony_notes)

    if harmony_type in (2, 3):
        upper_harmony_notes = []
        for note in original_notes_for_track:
            harmony_tone = note['tone'] + semitone_interval
            original_tone = harmony_tone

            correction_attempts = 0
            while not is_note_in_key(harmony_tone, key_tone_index, key_mode) and correction_attempts < 3:
                harmony_tone -= 1
                correction_attempts += 1

            if not is_note_in_key(harmony_tone, key_tone_index, key_mode):
                harmony_tone = original_tone

            upper_harmony_notes.append({**note, 'tone': harmony_tone})
        harmony_tracks_notes.append(upper_harmony_notes)

    return harmony_tracks_notes

def add_harmony_tracks_to_ustx(ustx_data, selected_track_indices, harmony_type, track_names, semitone_interval, key_tone_index, key_mode):
    new_tracks = []
    harmony_names = ["Lower Harmony", "Upper Harmony"]

    for track_index in selected_track_indices:
        original_track = ustx_data['tracks'][track_index]
        original_track_name = original_track['track_name']
        original_notes_for_track = []
        for voice_part in ustx_data.get('voice_parts', []):
            if int(voice_part.get('track_no', 0)) == track_index:
                original_notes_for_track.extend(voice_part.get('notes', []))

        harmony_tracks_notes = generate_harmony_notes(original_notes_for_track, semitone_interval, harmony_type, key_tone_index, key_mode)

        if harmony_type in (1, 3):
            lower_harmony_notes = harmony_tracks_notes[0] if harmony_tracks_notes else []
            new_track = original_track.copy()
            new_track_name = f"{original_track_name} - {harmony_names[0]}"
            new_track['track_name'] = new_track_name

            new_voice_part = {
                'duration': ustx_data['voice_parts'][0]['duration'] if ustx_data['voice_parts'] else 0,
                'name': f"{new_track_name} Part",
                'comment': "",
                'track_no': len(ustx_data['tracks']) + len(new_tracks),
                'position': 0,
                'notes': lower_harmony_notes,
                'curves': []
            }
            ustx_data['voice_parts'].append(new_voice_part)
            new_tracks.append(new_track)


        if harmony_type in (2, 3):
            upper_harmony_notes = harmony_tracks_notes[1] if harmony_type == 3 and len(harmony_tracks_notes) > 1 else harmony_tracks_notes[0] if harmony_type == 2 and harmony_tracks_notes else []
            new_track = original_track.copy()
            new_track_name = f"{original_track_name} - {harmony_names[1]}"
            new_track['track_name'] = new_track_name

            new_voice_part = {
                'duration': ustx_data['voice_parts'][0]['duration'] if ustx_data['voice_parts'] else 0,
                'name': f"{new_track_name} Part",
                'comment': "",
                'track_no': len(ustx_data['tracks']) + len(new_tracks),
                'position': 0,
                'notes': upper_harmony_notes,
                'curves': []
            }
            ustx_data['voice_parts'].append(new_voice_part)
            new_tracks.append(new_track)

    ustx_data['tracks'].extend(new_tracks)
    return ustx_data