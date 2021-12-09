#Final Project Repository

You need to provide us access to your code repository.

If you did not use a github repository during your development, you can simply copy your files into this repository and commit those files as you would normally do.

If you already used a git repository, you can add this repository as an extra "remote" repository. For example, lets say that your final-project repository that you checked out through Github Classroom is `final-project-xyzzy`. You would execute the following steps:

```
$ git remote add final-project git@github.com:cu-csci-4253-datacenter-fall-2021/final-project-xyzzy.git

$ git push -u final-project master
Enter passphrase for key '/Users/grunwald/.ssh/id_rsa':
Enumerating objects: 155, done.
Counting objects: 100% (155/155), done.
Delta compression using up to 16 threads
Compressing objects: 100% (76/76), done.
Writing objects: 100% (155/155), 1.49 MiB | 5.44 MiB/s, done.
Total 155 (delta 78), reused 155 (delta 78), pack-reused 0
remote: Resolving deltas: 100% (78/78), done.
To github.com:cu-csci-4253-datacenter-fall-2021/final-project-xyzzy.git
 * [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'final-project'.
```

Note that this example uses branch `master` as the master branch; more recent git repos would use the branch `main`. This example also assumes you're using SSH-based authentication.

You can add this remote repository link right away and then continue to push updated to it using the the `git push final-project master` command. For more details on using multiple remote repoositories [see the documenation](https://git-scm.com/book/ms/v2/Git-Basics-Working-with-Remotes).


<br> Example to try the endpoints 
<br> curl http://localhost:80/api/getSpecificRouteWeather/Boulder/Denver/example_id@gmail.com
<br> curl http://localhost:80/api/subscribe/example_id@gmail.com/Boulder/Denver
<br> curl http://localhost:80/api/unsubscribe/example_id@gmail.com
