from scanoss.scanner import Scanner
import io
import sys
import os


def main():
    scanner = Scanner()
    
    file_path = './test2.py'
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        return
    
    try:
        print(f"Scanning file: {file_path}")
        
        # Capture stdout from wfp_file()
        captured_output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        scanner.wfp_file(file_path)
        
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        # Extract only fragment hashes (skip "file=" and "fh2=")
        # "file" contains quick file identification + metadata
        # "fh2" contains secondary quick file hash for verification/redundancy

        fragments = {}
        for line in output.split('\n'):
            if line and not line.startswith('file=') and not line.startswith('fh2='):
                key, value = line.split('=', 1)
                fragments[key] = value
        
        print("Fragments:")
        for key, value in fragments.items():
            print(f"{key}={value}")
                
    except Exception as e:
        print(f"Error during scanning: {str(e)}")

if __name__ == "__main__":
    main()