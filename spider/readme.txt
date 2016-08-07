BAE3.0新增了worker类型的应用，那么到底该如何使用worker类型？它能用在什么地方了？

传统的WEB类型，主要用来创建WEB应用；这种应用的特点是通过HTTP请求来驱动应用逻辑；但有时候我们需要长期在后台跑一些任务，例如爬虫，不停的去爬取各种网络资源，通过WEB类型就不好实现了。

worker类型最适合的就是用来创建需要长期在后台运行任务的应用。


BAE3.0里面，通过 supervisor 来管理worker类型的应用；在你的应用的根目录下，需要放置一个名字为 ‘supervisord.conf’ 的配置文件，supervisor守护进程会按照这个配置文件来启动进程，并在进程出现异常退出的情况下进行重启。下面举个例子来看下这个配置文件有哪些配置项：

[program: spider]
command = python /home/bae/app/spider.py
numprocess = 2
autorestart = true
stdout_logfile = /home/bae/logs/spider.stdout.log
stderr_logfile = /home/bae/logs/spider.stderr.log

[program: foo]
command = python /home/bae/app/foo.py
numprocess = 1
autorestart = true
stdout_logfile = /home/bae/logs/foo.stdout.log
stderr_logfile = /home/bae/logs/foo.stderr.log
在上面这个例子中，我们指定了两个后台任务 ‘spider’ 和 ‘foo’：

第一个任务是执行 /home/bae/app/spider.py 这个脚本，并将标准输出和标准出错重定向到 /home/bae/logs 下；’numprocess’ 指定了要创建两个进程， 而 ‘autorestart’ 则表示当进程退出后，会被重新启动。

第二个任务是执行 /home/bae/app/foo.py 这个脚本，并将标准输出和标准出错重定向到 /home/bae/logs 下；’numprocess’ 指定了要创建一个进程， 而 ‘autorestart’ 则表示当进程退出后，会被重新启动。

以上是 supervisor.conf 中主要用到的配置项，更完整的配置项请参看 完整的配置文件格式请参看 http://supervisord.org/configuration.html#program-x-section-settings

在 spider.py 或  foo.py 中，我们通常应该实现一个长期循环的任务，例如  foo.py：

import time
import sys

while True:
		time.sleep(3)
		sys.stdout.write("hello python world\n")
		sys.stdout.flush()