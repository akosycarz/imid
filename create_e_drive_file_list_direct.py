#!/usr/bin/env python3
"""
Create BAM file list and sample annotation from /mnt/e/bams only.
"""

import os
import sys

def create_e_drive_file_list_direct(folder_path=None):
    """
    Create file list from BAM files found in /mnt/e/bams only.
    Outputs:
      - bams+path_windows.txt (BAMs, WSL and Windows path)
      - sample_annotation.tsv (DROP sample annotation)
    """
    # Always use /mnt/e/bams/ as the folder path
    if folder_path is None:
        folder_path = "/mnt/e/bams/"
    if not folder_path.startswith("/mnt/e/bams"):
        print("❌ Only /mnt/e/bams path is supported. Please use /mnt/e/bams/")
        return False
    if not folder_path.endswith("/"):
        folder_path += "/"

    print(f"🔍 Scanning folder: {folder_path}")

    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        print("Please check the path and make sure the folder exists")
        return False

    print(f"✅ Found folder: {folder_path}")

    bam_files = []
    try:
        print("🔍 Searching for BAM files in the specified folder...")
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and file.lower().endswith('.bam'):
                bam_files.append(file_path)

        print(f"✅ Found {len(bam_files)} BAM files")

        # 1. BAMs+path_windows.txt
        output_file = "bams+path_windows.txt"
        with open(output_file, 'w') as f:
            f.write("# BAM files: WSL path and Windows path\n")
            f.write("# Format: <WSL_path>\t<Windows_path>\n")
            for bam_file in sorted(bam_files):
                # WSL path
                wsl_path = bam_file
                # Windows path: /mnt/e/bams/SAMPLE.bam -> E:/bams/SAMPLE.bam
                windows_path = wsl_path.replace('/mnt/e/', 'E:/').replace('/', '\\')
                windows_path = windows_path.replace('\\', '/')
                f.write(f"{wsl_path}\t{windows_path}\n")
        print(f"✅ Created BAM+Windows path file: {output_file}")

        # 2. sample_annotation.tsv
        sample_annotation_output = "sample_annotation.tsv"
        with open(sample_annotation_output, 'w') as f:
            header = "RNA_ID\tRNA_BAM_FILE\tDROP_GROUP\tPAIRED_END\tSTRAND\tCOUNT_MODE\tCOUNT_OVERLAPS\tDNA_VCF_FILE\tDNA_ID\tHPO_TERMS\tGENOME\tGENE_COUNTS_FILE\tGENE_ANNOTATION\tSPLICE_COUNTS_DIR\n"
            f.write(header)
            for bam_file in sorted(bam_files):
                filename = os.path.basename(bam_file)
                sample_id = filename.replace('.bam', '')
                # Windows path for annotation
                windows_path = bam_file.replace('/mnt/e/', 'E:/').replace('/', '\\')
                windows_path = windows_path.replace('\\', '/')
                line = f"{sample_id}\t{windows_path}\toutrider,fraser,mae,batch_0\tTRUE\tno\tIntersectionStrict\tFALSE\tNA\t{sample_id}\tNA\thg19\tNA\tNA\tNA\n"
                f.write(line)
        print(f"✅ Created sample annotation file: {sample_annotation_output}")

        print(f"\n📊 Summary:")
        print(f"   - BAM files: {len(bam_files)}")
        print(f"   - Files created:")
        print(f"     * {output_file} (BAMs with WSL and Windows path)")
        print(f"     * {sample_annotation_output} (DROP pipeline sample annotation)")

        print(f"\n📄 Example BAM files found:")
        for i, bam_file in enumerate(sorted(bam_files)[:5]):
            filename = os.path.basename(bam_file)
            print(f"   - {filename}")
        if len(bam_files) > 5:
            print(f"   ... and {len(bam_files) - 5} more")

        return True

    except PermissionError:
        print("❌ Permission denied accessing /mnt/e/bams")
        return False
    except Exception as e:
        print(f"❌ Error accessing /mnt/e/bams: {e}")
        return False

def main():
    """
    Main function
    """
    print("🎯 BAM File List Creator - /mnt/e/bams only")
    print("=" * 50)

    folder_path = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage:")
            print("  python create_e_drive_file_list_direct.py                # Use /mnt/e/bams/")
            print("  python create_e_drive_file_list_direct.py --help         # Show this help")
            return True
        else:
            folder_path = sys.argv[1]

    success = create_e_drive_file_list_direct(folder_path)

    if success:
        print("\n✅ Successfully created BAM file list and sample annotation from /mnt/e/bams!")
        print("\n💡 You can now use these files for downstream analysis.")
    else:
        print("\n❌ Failed to create file lists from /mnt/e/bams!")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure /mnt/e/bams/ exists and is accessible")
        print("   2. Only /mnt/e/bams/ is supported in this script")

if __name__ == "__main__":
    main()