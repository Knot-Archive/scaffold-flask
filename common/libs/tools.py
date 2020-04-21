"""
summary:
a old project install package with requirements,
trans requirements to poetry-project.

ref:
https://python-poetry.org/docs/cli/#add

req:
poetry
"""
import subprocess


def req2poetry(fp):
    # fp = requirements.txt path
    with open(fp, 'r') as file:
        deps = text.split('\n')
        for dep in deps:
            if dep != '':
                d = dep.split('==')
                subprocess.call(['poetry', 'add', '{}=={}'.format(d[0], d[1])])


if __name__ == '__main__':
    req2poetry('/Users/conor/Code/360FinancialRisk/requirements.txt')
