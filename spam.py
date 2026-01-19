import os
import time
import subprocess
import random
import sys

def setup_repo():
    """Inicjalizuje repozytorium jeśli nie istnieje"""
    if not os.path.exists('spam_file.txt'):
        with open('spam_file.txt', 'w') as f:
            f.write("Initial commit\n")
        
        subprocess.run(['git', 'add', '.'], capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], capture_output=True)
        print("Initial commit created")

def make_single_commit(counter):
    """Tworzy pojedynczy commit"""
    try:
        # Zmień zawartość pliku
        with open('spam_file.txt', 'a') as f:
            f.write(f"\nCommit #{counter} at {time.ctime()}\n")
        
        # Git commands
        subprocess.run(['git', 'add', '.'], capture_output=True, timeout=10)
        subprocess.run(['git', 'commit', '-m', f"Auto commit #{counter} - {time.ctime()}"], 
                      capture_output=True, timeout=10)
        
        return True
    except Exception as e:
        print(f"Commit error: {e}")
        return False

def push_commits():
    """Pushuje commity na GitHub"""
    try:
        result = subprocess.run(['git', 'push', 'origin', 'main'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("Push successful")
            return True
        else:
            print(f"Push failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Push timeout")
        return False
    except Exception as e:
        print(f"Push error: {e}")
        return False

def main():
    print("=== GITHUB COMMIT SPAMMER ===")
    print("UWAGA: Używaj tylko na prywatnym repozytorium testowym!")
    print("Naciśnij Ctrl+C aby zatrzymać\n")
    
    # Potwierdzenie
    confirm = input("Czy na pewno chcesz kontynuować? (tak/NIE): ")
    if confirm.lower() != 'tak':
        print("Anulowano.")
        return
    
    setup_repo()
    
    counter = 0
    push_counter = 0
    
    while True:
        try:
            counter += 1
            
            # Stwórz commit
            if make_single_commit(counter):
                print(f"Commit #{counter} created")
            else:
                time.sleep(30)  # Czekaj przy błędzie
                continue
            
            # Push co 5 commitów (aby nie spamować za mocno)
            push_counter += 1
            if push_counter >= 5:
                if push_commits():
                    push_counter = 0
                else:
                    # Jeśli push się nie udał, czekaj dłużej
                    time.sleep(60)
            
            # Losowe opóźnienie (30-120 sekund)
            delay = random.uniform(30, 120)
            print(f"Next commit in {delay:.1f}s...")
            time.sleep(delay)
            
        except KeyboardInterrupt:
            print("\n\nZatrzymywanie...")
            # Ostatni push przed zamknięciem
            push_commits()
            break
        except Exception as e:
            print(f"Critical error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()