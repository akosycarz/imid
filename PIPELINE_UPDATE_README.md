# DROP Pipeline Dynamic Update System

This system allows you to dynamically update the DROP pipeline configuration by reading BAM file paths from `bams_paths_windows.txt`.

## Files Overview

### Core Scripts
- `update_pipeline_from_paths.py` - Main script for updating pipeline from paths file
- `quick_update.py` - Simple one-liner script for quick updates
- `create_e_drive_file_list_direct.py` - Original script that generates paths file

### Configuration Files
- `bams_paths_windows.txt` - Source file containing BAM file paths
- `config.yaml` - DROP pipeline configuration
- `sample_annotation.tsv` - Sample annotation file (auto-generated)

## Usage

### 1. Initial Setup

First, ensure you have your BAM file paths in `bams_paths_windows.txt`:

```bash
# Generate paths file from your BAM folder
python create_e_drive_file_list_direct.py "/mnt/e/bams/"

# Or manually create bams_paths_windows.txt with your BAM paths
```

### 2. Update Pipeline

Run the main update script to process the paths file:

```bash
python update_pipeline_from_paths.py
```

This will:
- Read BAM paths from `bams_paths_windows.txt`
- Create/update `sample_annotation.tsv`
- Update `config.yaml` with correct groups
- Validate the pipeline setup

### 3. Quick Updates

For quick updates when you add new BAM files:

```bash
python quick_update.py
```

### 4. Run Pipeline

After updating, run the DROP pipeline:

```bash
snakemake --cores 4
```

## File Format Requirements

### bams_paths_windows.txt
Should contain one BAM file path per line:
```
\mnt\e\bams\S1504Nr1.markdup.sorted.bam
\mnt\e\bams\S1504Nr2.markdup.sorted.bam
...
```

### sample_annotation.tsv (Auto-generated)
Contains all required columns for DROP pipeline:
- RNA_ID: Sample identifier
- RNA_BAM_FILE: Path to BAM file
- DROP_GROUP: Analysis groups (outrider,fraser,mae,batch_0)
- PAIRED_END: TRUE/FALSE
- STRAND: no/yes/reverse
- COUNT_MODE: IntersectionStrict
- And other required columns...

## Workflow

1. **Add New BAM Files**: Update `bams_paths_windows.txt` with new paths
2. **Update Pipeline**: Run `python update_pipeline_from_paths.py`
3. **Validate**: Check that all files are properly configured
4. **Run Analysis**: Execute `snakemake --cores 4`

## Benefits

- **Dynamic**: Automatically adapts to new BAM files
- **Consistent**: Ensures sample annotation matches paths file
- **Validated**: Checks for missing files and configuration issues
- **Flexible**: Easy to add/remove samples or change groups

## Troubleshooting

### Common Issues

1. **File Not Found**: Ensure `bams_paths_windows.txt` exists
2. **No BAM Files**: Check that paths end with `.bam`
3. **Config Mismatch**: Groups in config.yaml must match sample annotation
4. **Permission Errors**: Ensure write permissions for output files

### Validation

The script automatically validates:
- Required files exist
- Sample annotation has content
- Config file is properly formatted
- BAM paths are accessible

## Example Output

```
🎯 DROP Pipeline Paths Updater
========================================
📁 Reading BAM paths from: bams_paths_windows.txt
Found BAM file: S1504Nr1.markdup.sorted -> E:/bams/S1504Nr1.markdup.sorted.bam
Found BAM file: S1504Nr2.markdup.sorted -> E:/bams/S1504Nr2.markdup.sorted.bam
...

📊 Found 32 BAM files

📝 Creating sample annotation file...
✅ Created sample annotation file: sample_annotation.tsv
✅ Added 32 samples

⚙️  Updating config file...
✅ Updated config.yaml with correct groups

🔍 Validating pipeline setup...
✅ Found: bams_paths_windows.txt
✅ Found: config.yaml
✅ Found: sample_annotation.tsv
✅ Sample annotation has 32 samples

✅ Successfully updated DROP pipeline!

📋 Summary:
   - BAM files processed: 32
   - Sample annotation: sample_annotation.tsv
   - Config file: config.yaml
   - Groups configured: outrider, fraser, mae, batch_0

🚀 You can now run the DROP pipeline with:
   snakemake --cores 4
``` 