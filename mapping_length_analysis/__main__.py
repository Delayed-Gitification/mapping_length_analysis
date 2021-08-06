import dnaio
import pandas as pd
import argparse
import pysam


def analyse_bam(bam_name):
    d = {}
    with pysam.AlignmentFile(bam_name, "rb") as samfile:
        for read in samfile:
            l = int(read.query_length)
            if l in d.keys():
                d[l] += 1
            else:
                d[l] = 1
    return d


def analyse_fq(fq_name):
    d = {}
    with dnaio.open(fq_name) as f:
        for record in f:
            l = len(record.sequence)
            if l in d.keys():
                d[l] += 1
            else:
                d[l] = 1
    return d


def write_dict(d, name, d2={}):
    for_df = {'length': d.keys(), 'n': d.values()}
    df = pd.DataFrame.from_dict(for_df)
    print(df)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bam", default="None", help="A bam file to analyse")
    parser.add_argument("-f", "--fastq", default="None", help="A fastq to analyse")
    parser.add_argument("-o", "--output", required=True, help="Output filename")
    args = parser.parse_args()

    n_inputs = 2
    if args.bam == "None":
        n_inputs += -1
    if args.fastq == "None":
        n_inputs += -1
    assert n_inputs > 0, "Provide at least one input file!"

    if args.bam != "None":
        bam_stats = analyse_bam(args.bam)
        if n_inputs == 1:
            write_dict(bam_stats, args.output)

    if args.fastq != "None":
        fq_stats = analyse_fq(args.fastq)
        if n_inputs == 1:
            write_dict(fq_stats, args.output)

    if n_inputs == 2:
        write_dict(fq_stats, args.output, bam_stats)
    

if __name__ == '__main__':
    main()
    