import os
import glob
import re

def parse_cluster_count(result_dir):
    genoma = os.path.basename(result_dir)
    cluster_files = glob.glob(os.path.join(result_dir, 'geneclusters', '*.gbk'))
    return genoma, len(cluster_files)

def main():
    root_dir = "."

    results = []
    for d in os.listdir(root_dir):
        full_path = os.path.join(root_dir, d)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "index.html")):
            genoma, count = parse_cluster_count(full_path)
            results.append((genoma, count))

    with open("resultados_final.tsv", "w") as f:
        f.write("Genoma\tNum_Clusters\n")
        for genoma, count in results:
            f.write(f"{genoma}\t{count}\n")

if __name__ == "__main__":
    main()
