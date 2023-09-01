import subprocess

from celery import shared_task
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True)
def download(self, url, path):
    q = 'ffmpeg -loglevel warning -stats -y -i {0} -c copy -bsf:a aac_adtstoasc "{1}.mp4"'
    progress_recorder = ProgressRecorder(self)
    process = subprocess.Popen(
        q.format(url, path),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        encoding='utf-8',
        errors='replace'
    )
    while True:
        realtime_output = process.stdout.readline()

        if realtime_output == '' and process.poll() is not None:
            break

        if realtime_output:
            realtime_output = realtime_output.strip()
            start = realtime_output.find('frame=') + 6
            end = realtime_output.find("fps")
            progress_recorder.set_progress(int(realtime_output[start:end].strip()), 0, description=" Кадров")
    return "ok"
