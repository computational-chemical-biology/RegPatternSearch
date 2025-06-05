nextflow.enable.dsl = 2

params {
    base_dir = '/temporario2/9877294/extracted_gbff'
    output_base = '/temporario2/9877294/Resultados_AntiSMASH'
}

process {
    executor = 'slurm'
    cpus = 20
    memory = '32 GB'
    time = '40h'
    queue = 'SP2'
}

executor {
    queueSize = 100
    submitRateLimit = '1 sec'
}

timeline.enabled = true
report.enabled = true
trace.enabled = true
dag.enabled = true

timeline.file = 'timeline.html'
report.file = 'report.html'
trace.file = 'trace.txt'
dag.file = 'dag.png'

