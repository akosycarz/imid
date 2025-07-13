# Using External BAM Files with DROP Pipeline

This guide explains how to use BAM files from an external directory (like `E:\bams`) without copying them to the repository.

## Setup

### 1. Generate Sample Annotation File

Run the provided script to automatically create a sample annotation file from your BAM files:

```bash
python create_sample_annotation.py
```

This script will:
- Scan the `E:/bams` directory for `.bam` files
- Extract sample IDs from filenames
- Create a properly formatted sample annotation file

### 2. Manual Sample Annotation (Alternative)

If you prefer to create the sample annotation manually, use the template in `sample_annotation.tsv`:

```tsv
RNA_ID	RNA_BAM_FILE	DROP_GROUP	PAIRED_END	STRAND	COUNT_MODE	DNA_VCF_FILE	DNA_ID	KNIME_META	HPO_TERMS	KNOWN_RNA_ID	RNA_VCF_FILE	GENOME
S1504Nr1	E:/bams/S1504Nr1.markdup.sorted.bam	group1	TRUE	NA	IntersectionStrict	NA	NA	NA	NA	NA	NA	hg19
```

### 3. Configuration

The `config.yaml` file has been updated to use your sample annotation file:

```yaml
sampleAnnotation: sample_annotation.tsv
```

## Important Notes

### File Paths
- Use forward slashes (`/`) in paths, even on Windows
- The pipeline will check if BAM files exist before running
- Make sure your BAM files have corresponding `.bai` index files

### Sample Groups
- Modify the `DROP_GROUP` column to organize your samples
- Common groups: `group1`, `group2`, `fraser`, `mae`, etc.
- Different groups can be analyzed separately

### Genome Assembly
- Update the `GENOME` column to match your reference genome
- Common values: `hg19`, `hg38`, `mm10`, etc.

### BAM File Requirements
- BAM files should be sorted and indexed
- Paired-end reads should be marked as `TRUE` in `PAIRED_END` column
- For strand-specific analysis, set `STRAND` to `+` or `-`

## Running the Pipeline

After setting up the sample annotation:

```bash
# Run the entire pipeline
snakemake --cores 4

# Run specific modules
snakemake aberrantExpression --cores 4
snakemake aberrantSplicing --cores 4
snakemake mae --cores 4
```

## Troubleshooting

### File Not Found Errors
- Check that BAM file paths are correct
- Ensure BAM files exist and are accessible
- Verify file permissions

### Index Files Missing
- BAM files need corresponding `.bai` index files
- Create index files: `samtools index sample.bam`

### Path Issues on Windows
- Use forward slashes in paths: `E:/bams/` not `E:\bams\`
- Consider using relative paths if possible

## Customization

### Multiple Groups
If you have different sample groups, modify the sample annotation:

```tsv
RNA_ID	RNA_BAM_FILE	DROP_GROUP	PAIRED_END	STRAND	COUNT_MODE	DNA_VCF_FILE	DNA_ID	KNIME_META	HPO_TERMS	KNOWN_RNA_ID	RNA_VCF_FILE	GENOME
SAMPLE1	E:/bams/SAMPLE1.bam	control	TRUE	NA	IntersectionStrict	NA	NA	NA	NA	NA	NA	hg19
SAMPLE2	E:/bams/SAMPLE2.bam	case	TRUE	NA	IntersectionStrict	NA	NA	NA	NA	NA	NA	hg19
```

### Different File Naming
If your BAM files have different naming patterns, modify the `create_sample_annotation.py` script accordingly. 