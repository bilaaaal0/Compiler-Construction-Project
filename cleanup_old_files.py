"""
Cleanup script to remove old .tac and .asm files
These files are no longer needed as all output goes to *_output folders
"""

import os
import glob

def cleanup():
    """Remove old .tac and .asm files from root directory"""
    
    # Find all .tac and .asm files in current directory (not in subdirectories)
    patterns = ['*.tac', '*.asm']
    removed_files = []
    
    for pattern in patterns:
        for file in glob.glob(pattern):
            # Only remove if it's in the current directory (not in output folders)
            if os.path.isfile(file):
                try:
                    os.remove(file)
                    removed_files.append(file)
                    print(f"Removed: {file}")
                except Exception as e:
                    print(f"Could not remove {file}: {e}")
    
    if removed_files:
        print(f"\nTotal files removed: {len(removed_files)}")
    else:
        print("No old files found to remove.")

if __name__ == '__main__':
    print("Cleaning up old .tac and .asm files...")
    print("=" * 60)
    cleanup()
    print("=" * 60)
    print("\nCleanup complete!")
    print("\nNote: All compilation output now goes to *_output folders.")
