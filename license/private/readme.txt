ssh-keygen -t rsa -C "chenyongbing2008@163.com"

在Windows上安装Git
在Windows上使用Git，可以从Git官网直接下载安装程序，然后按默认选项安装即可。
安装完成后，还需要最后一步设置，在命令行输入：
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"

创建版本库
git init

添加远程库
首先，登陆GitHub，然后，在右上角找到“Create a new repo”按钮，创建一个新的仓库：

$ git remote add origin git@github.com:michaelliao/learngit.git
把本地库的内容推送到远程，用git push命令，实际上是把当前分支master推送到远程。
由于远程库是空的，我们第一次推送master分支时，加上了-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令。

查看分支：git branch
创建分支：git branch <name>
切换分支：git checkout <name>或者git switch <name>
创建+切换分支：git checkout -b <name>或者git switch -c <name>
合并某分支到当前分支：git merge <name>
删除分支：git branch -d <name>