import json
import datetime
class Note:
    def __init__(self, note_id, title, body, timestamp):
        self.note_id = note_id
        self.title = title
        self.timestamp = timestamp
        self.body = body


class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.file_path, 'r') as file:
                notes_data = json.load(file)
                notes = [Note(note['note_id'], note['title'], note['body'], note['timestamp']) for note in notes_data]
                return notes
        except FileNotFoundError:
            return []

    def save_notes(self):
        notes_data = [{'note_id': note.note_id, 'title': note.title, 'body': note.body, 'timestamp': note.timestamp} for
                      note in self.notes]
        with open(self.file_path, 'w') as file:
            json.dump(notes_data, file)

    def add_note(self, title, body):
        note_id = len(self.notes) + 1
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        note = Note(note_id, title, body, timestamp)
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, note_id, new_title, new_body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = new_title
                note.body = new_body
                note.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return True
        return False

    def delete_note(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                self.save_notes()
                return True
        return False

    def get_notes(self, filter_date=None):
        if filter_date:
            filtered_notes = [note for note in self.notes if note.timestamp.startswith(filter_date)]
            return filtered_notes
        return self.notes


def main():
    note_manager = NoteManager("notes.json")
    note_manager.add_note("Кошки", "домашнее животное, одно из наиболее популярных «животных-компаньонов»")
    note_manager.add_note("Собаки", "Собаки могут улыбаться")
    note_manager.edit_note(2, "Котята", "Котята рождаются не только слепыми, но и глухими")
    note_manager.delete_note(1)
    notes = note_manager.get_notes()

    for note in notes:
        print(f"Заметка {note.note_id}: {note.title}")
        print(note.body)
        print(note.timestamp)
        print("-------------------------")

if __name__ == "__main__":
    main()
