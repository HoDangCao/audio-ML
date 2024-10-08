from lib import *

note_frequencies = np.load('../data/note_frequencies.npy', allow_pickle=True).item()
sample_rate = 44100
pressed_notes = {}

# Initialize Pygame
pygame.init()

# Generate a tone for the note
def generate_tone(frequency, duration=10):
    num_samples = int(sample_rate * duration)
    amplitude = np.linspace(1.5, 0, num_samples, endpoint=False)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    tone = amplitude * np.sin(2 * np.pi * frequency * t)
    return tone.astype(np.float32)

current_pos = 0
# Play a sound in a loop
def play_sound(note_interval):
    print(note_interval)
    frequency = note_frequencies[note_interval]
    tone = generate_tone(frequency)
    
    def callback(outdata, frames, time, status):
        global current_pos
        if status:
            print(status)
        
        # Calculate the end position
        end_pos = current_pos + frames
        if end_pos >= len(tone):
            end_pos = len(tone)
        
        # Fill the buffer with audio data
        outdata[:end_pos-current_pos] = tone[current_pos:end_pos].reshape(-1, 1)
        
        # Update the current position
        current_pos = end_pos
        
        # Loop the sound
        if current_pos >= len(tone):
            current_pos = 0

    # # Play sound if not already playing
    # if note_interval not in pressed_notes:
    pressed_notes[note_interval] = sd.OutputStream(samplerate=sample_rate, channels=1, callback=callback, blocksize=1024, latency='low')
    pressed_notes[note_interval].start()
    
    # sd.wait()

# Stop sound playback
def stop_sound(note_interval):
    pressed_notes[note_interval].stop()
    pressed_notes[note_interval].close()
    del pressed_notes[note_interval]

# Map keys to notes (without octave numbers)
key_note = {
    'A': 'C', 'W': 'C#', 'S': 'D', 'E': 'D#', 'D': 'E', 'F': 'F', 
    'T': 'F#', 'G': 'G', 'Y': 'G#', 'H': 'A', 'U': 'A#', 'J': 'B'
}

# Main function to handle key events
def main():
    screen_width = 200
    screen_height = 150
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Play Piano')

    interval = '4'

    running = True
    while running:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).upper()
                if key.isdigit():
                    interval = key
                
                note = key_note[key] if key in key_note else ' '
                note_interval = note + interval
                if note_interval in note_frequencies:
                    play_sound(note_interval)

            if event.type == pygame.KEYUP:
                key = pygame.key.name(event.key).upper()
                note = key_note[key] if key in key_note else ''
                note_interval = note + interval
                if note_interval in pressed_notes:
                    stop_sound(note_interval)
                    
    pygame.quit()

if __name__ == "__main__":
    # background_thread1 = threading.Thread(target=play_note, args=('G4', 5, True), daemon=True)
    # background_thread2 = threading.Thread(target=play_note, args=('F4', 3, True), daemon=True)
    # background_thread1.start()
    # background_thread2.start()

    main()
