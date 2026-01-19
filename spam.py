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
        
        subprocess.run(['git', 'add', '.'], capture_output=True, check=False)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], capture_output=True, check=False)
        print("Initial commit created")
    
    # Upewnij się że mamy branch master/main
    result = subprocess.run(['git', 'branch', '--show-current'], 
                          capture_output=True, text=True, check=False)
    branch = result.stdout.strip()
    print(f"Current branch: {branch}")
    
    # Jeśli to pierwszy push, ustaw upstream
    result = subprocess.run(['git', 'push', '--set-upstream', 'origin', branch], 
                          capture_output=True, text=True, check=False)
    print("Upstream set")

def make_single_commit(counter):
    """Tworzy pojedynczy commit"""
    try:
        # Zmień zawartość pliku
        with open('spam_file.txt', 'a') as f:
            f.write(f"\nCommit #{counter} at {time.ctime()}\n")
        
        # Git commands
        subprocess.run(['git', 'add', '.'], capture_output=True, timeout=10, check=False)
        subprocess.run(['git', 'commit', '-m', f"Auto commit #{counter} - {time.ctime()}"], 
                      capture_output=True, timeout=10, check=False)
        
        return True
    except Exception as e:
        print(f"Commit error: {e}")
        return False

def push_force():
    """Pushuje commity na GitHub Z FORCEM (nadpisuje remote)"""
    try:
        # Najpierw spróbuj normalny push
        result = subprocess.run(['git', 'push', 'origin', 'master'], 
                              capture_output=True, text=True, timeout=30, check=False)
        
        if result.returncode == 0:
            print("Push successful")
            return True
        else:
            # Jeśli normalny push się nie uda, użyj force
            print("Normal push failed, trying force push...")
            result = subprocess.run(['git', 'push', '--force', 'origin', 'master'], 
                                  capture_output=True, text=True, timeout=30, check=False)
            
            if result.returncode == 0:
                print("Force push successful")
                return True
            else:
                print(f"Force push failed: {result.stderr}")
                return False
                
    except subprocess.TimeoutExpired:
        print("Push timeout")
        return False
    except Exception as e:
        print(f"Push error: {e}")
        return False

def push_with_lease():
    """Bezpieczniejsza wersja force push"""
    try:
        result = subprocess.run(['git', 'push', '--force-with-lease', 'origin', 'main'], 
                              capture_output=True, text=True, timeout=30, check=False)
        
        if result.returncode == 0:
            print("Push successful")
            return True
        else:
            print(f"Push failed: {result.stderr}")
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
                time.sleep(30)
                continue
            
            # Push co 3 commity
            push_counter += 1
            if push_counter >= 200:
                # Użyj force-with-lease zamiast zwykłego force
                if push_with_lease():
                    push_counter = 0
                else:
                    # Przy błędzie czekaj dłużej
                    print("Waiting 60s after error...")
                    time.sleep(60)
                    push_counter = 0  # Reset counter
            
        except KeyboardInterrupt:
            print("\n\nZatrzymywanie...")
            # Ostatni push
            push_with_lease()
            break
        except Exception as e:
            print(f"Critical error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()