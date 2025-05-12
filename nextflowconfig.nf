params.outdir = 'resultados_AS'

process {
    executor = 'slurm'
    cpus = 8
    memory = '16 GB'
    time = '12h'
    queue = 'long'
    scratch = true
    errorStrategy = 'retry'
}

timeline.enabled = true
report.enabled = true
trace.enabled = true
dag.enabled = true

timeline.file = 'timeline.html'
report.file = 'report.html'
trace.file = 'trace.txt'
dag.file = 'dag.png'
