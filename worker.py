from PyQt6.QtCore import QRunnable, pyqtSlot

from ustx_harms import get_ustx_data, get_track_names, get_key_from_notes, add_harmony_tracks_to_ustx, save_ustx_data, key_names

class HarmonyGeneratorWorker(QRunnable):

    def __init__(self, ustx_file_path, output_file_path, selected_track_indices, harmony_type, semitone_interval, manual_key_selection, key_name, key_mode):
        super().__init__()
        print(f"Initializing worker with ustx_file_path: {ustx_file_path}, output_file_path: {output_file_path}, selected_track_indices: {selected_track_indices}, harmony_type: {harmony_type}, semitone_interval: {semitone_interval}, manual_key_selection: {manual_key_selection}, key_name: {key_name}, key_mode: {key_mode}")
        self.ustx_file_path = ustx_file_path
        self.output_file_path = output_file_path
        self.selected_track_indices = selected_track_indices
        self.harmony_type = harmony_type
        self.semitone_interval = semitone_interval
        self.manual_key_selection = manual_key_selection
        self.key_name = key_name
        self.key_mode = key_mode

    @pyqtSlot()
    def run(self):
        print(f"HarmonyGeneratorWorker.run() started, ustx_file_path: {self.ustx_file_path}, output_file_path: {self.output_file_path}")
        try:
            ustx_data, error_ustx = get_ustx_data(self.ustx_file_path)
            if error_ustx:
                print(f"Error loading USTx file: {error_ustx}")
                return

            track_names = get_track_names(ustx_data)
            print(f"Loaded track names: {track_names}")

            first_track_notes_for_key_detect = []
            for voice_part in ustx_data.get('voice_parts', []):
                if int(voice_part.get('track_no', 0)) == self.selected_track_indices[0]:
                    first_track_notes_for_key_detect.extend(voice_part.get('notes', []))
                    
            if self.manual_key_selection:
                if self.key_name not in key_names:
                    print(f"Invalid key name: {self.key_name}")
                    return
                key_name = self.key_name
                key_mode = self.key_mode
                key_tone_index, _, _ = get_key_from_notes(first_track_notes_for_key_detect)
            else:
                key_tone_index, key_name, key_mode = get_key_from_notes(first_track_notes_for_key_detect)

            print(f"Detected key: {key_name} {key_mode} {key_tone_index}")

            modified_ustx_data = add_harmony_tracks_to_ustx(
                ustx_data, self.selected_track_indices, self.harmony_type, track_names,
                self.semitone_interval, key_tone_index, key_mode
            )

            save_error = save_ustx_data(modified_ustx_data, self.output_file_path)
            if save_error:
                print(f"Error saving file: {save_error}")
                with open("error_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"Error saving file: {save_error}\n")
            else:
                print(f"Harmony generation complete")

        except Exception as e:
            print(f"Unexpected error: {e}")
            with open("error_log.txt", "a", encoding="utf-8") as f:
                f.write(f"Unexpected error: {e}\n")