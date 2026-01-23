from scanoss.scanner import Scanner
import io
import sys
import os

class HashManager:

    @staticmethod
    def compute_file_hashes(file_path):
        scanner = Scanner()

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

            hashes = []
            for line in output.split('\n'):
                if line and not line.startswith('file=') and not line.startswith('fh2='):
                    key, value = line.split('=', 1)
                    if "," not in value:
                        hashes.append(value)
                    elif "," in value:
                        temp_hashes = value.split(",")
                        hashes.extend(temp_hashes)

            print("Fragments:")
            for h in hashes:
                print(f"{h}")

            return hashes

        except Exception as e:
            print(f"Error during scanning: {str(e)}")
            return e

    def compute_directory_hashes(directory_path):
        if not os.path.exists(directory_path):
            print(f"Error: Directory '{directory_path}' not found")
            return

        try:
            all_hashes = {}
            print(f"Scanning directory: {directory_path}")
            for root, dirs, files in os.walk(directory_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    file_hashes = HashManager.compute_file_hashes(file_path)
                    if file_hashes:
                        all_hashes[filename] = file_hashes

            return all_hashes

        except Exception as e:
            print(f"Error during scanning: {str(e)}")
            return e

        except Exception as e:
            print(f"Error during scanning: {str(e)}")
            return e

    def compute_similarity_hashes(hashes1, hashes2):

        """
        Calculates the Jaccard Similarity between two sets of hashes.
        
        Args:
            hashes1 (set): The set of hashes from the first document.
            hashes2 (set): The set of hashes from the second document.
            
        Returns:
            float: The similarity score between 0.0 and 1.0.
        """

        # Convert lists to sets for accurate set operations
        hashes1 = set(hashes1)
        hashes2 = set(hashes2)

        # Calculate the intersection of the two sets
        intersection = len(hashes1.intersection(hashes2))
        
        # Calculate the union of the two sets
        union = len(hashes1.union(hashes2))
        
        # Avoid division by zero if both sets are empty
        if union == 0:
            return 0.0
            
        # Return the Jaccard similarity coefficient
        return intersection / union
    
    
    


