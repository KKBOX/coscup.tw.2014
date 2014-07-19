import subprocess
import time
import sys


def execute_emr_job(label, python_file, input_file, master_type, core_type, num_core_nodes):

    cmd = ['python', python_file, '-r', 'emr', input_file,
            '--label', label,
            '--ec2-master-instance-type', master_type,
            '--ec2-core-instance-type', core_type,
            '--num-ec2-core-instances', str(num_core_nodes),
            '--num_ec2-task-instances', '0',
            '--file', 'play_count.txt',
            '--no-output']

    sys.stderr.write(' '.join(cmd) + '\n')
    sys.stderr.flush()
    subprocess.Popen(cmd, stdin=None, stdout=None, stderr=None, close_fds=True)  # run it in background

    time.sleep(30)


if __name__ == '__main__':
    python_file = 'calc_similarity.py'
    input_file = 's3://research-center/personal/aaronlin/mrjob/data/all/'
    num_core_nodes = 5
    # When you run multiple instances, the master node is just coordinating the
    #   other nodes, so usually the default instance type (m1.small) is fine, and using larger instances is wasteful.
    master_type = 'm1.small'

    # use different configurations
    core_types = ['m1.small', 'm1.medium', 'm1.large', 'm1.xlarge', 'm3.xlarge', 'm3.2xlarge',
            'c1.medium', 'c1.xlarge', 'cc2.8xlarge', 'c3.xlarge', 'c3.2xlarge', 'c3.4xlarge', 'c3.8xlarge',
            'm2.xlarge', 'm2.2xlarge', 'm2.4xlarge', 'cr1.8xlarge', 'r3.xlarge', 'r3.2xlarge', 'r3.4xlarge', 'r3.8xlarge']
    label = 'test'

    # execute emr jobs
    for core_type in core_types:
        label = 'test-%s' % core_type
        execute_emr_job(label, python_file, input_file, master_type, core_type, num_core_nodes)
