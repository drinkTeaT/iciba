from scrapy import cmdline

name = 'iciba_ielts'  # prooperations
cmd = 'scrapy crawl {0} -a course={1} -a class_id={2}'.format(name, 1, 15)
print(cmd)
cmdline.execute(cmd.split())
