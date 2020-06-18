#!/usr/bin/env python3
import argparse
import git
import progressbar

from collections import Counter

def analyse_repo(location):
    repo = git.Repo(location)
    pbar = progressbar.ProgressBar()
    return analyse_commits(pbar(list(repo.iter_commits())))

def analyse_commits(commits):
    counter = Counter()
    for commit in commits:
        email = commit.author.email
        if email:
            domain = email.rsplit('@', 1)[-1]
        else:
            domain = ''
        counter[domain] += commit.stats.total['lines']
    return dict(sorted(counter.items(), key=lambda x: -x[1]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Identify which companies contribute to a Git project"
    )
    parser.add_argument(
        'repo_location', default='.', help="Location of repo to analyse"
    )
    args = parser.parse_args()
    for org, count in analyse_repo(args.repo_location).items():
        print(org, count)
