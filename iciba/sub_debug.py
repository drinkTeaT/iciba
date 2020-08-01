import subprocess
import time

name = 'iciba_ielts'  # prooperations
# 课程名
class_id = 15
# 课程数
course_count = 229
for i in range(1, course_count):
    if i % 10 == 0:
        time.sleep(20)
    cmd = 'scrapy crawl {0} -a course={1} -a class_id={2}'.format(name, i, class_id)
    subprocess.Popen(cmd)
